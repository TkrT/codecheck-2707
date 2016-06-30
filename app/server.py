#!/usr/bin/env python

import json
from threading import Thread
import asyncio

import netifaces
from bottle import static_file, route, run
import websockets

import users
from bot import Bot

# Get own IP Address
def get_ipaddress():
  for iface_name in netifaces.interfaces():
    iface_data = netifaces.ifaddresses(iface_name).get(netifaces.AF_INET)
    for item in iface_data or []:
      for key, value in item.items():
        if ((key == 'addr') and (value != '127.0.0.1')):
          return value
  return '127.0.0.1'

# HTTP Handler using bottle
def httpHandler(HOST, PORT):
  while True:
    @route('/')
    def index():
      return static_file("index.html", root='./static')

    @route('/<filename>')
    def server_static(filename):
      return static_file(filename, root='./static')

    run(host=HOST, port=PORT)

# Generate JSON data from message
# Then send data to all connected client
@asyncio.coroutine
def send_message(message):
  jsoncontents = {"data": message}
  jsondata = json.dumps(jsoncontents)
  yield from asyncio.wait([ws.send(jsondata) for ws in users.connected])

# Websocket Handler using websockets
@asyncio.coroutine
def receive_send(websocket, path):
  # Please write your code here

  bot = Bot()

  # Add connection to list
  users.connected.add(websocket)

  try:
    # Loop until connection close or Ctrl-C
    while True:
      # Receive message
      message = yield from websocket.recv()

      print("Receiving ...")

      # Echo message
      yield from send_message(message)

      # Send hash when receive three words starts with "bot"
      wordlist = message.split(" ")
      botmessage = bot.exec(wordlist)
      if (botmessage != ""):
        yield from send_message(botmessage)

      # Sleep 1 second
      yield from asyncio.sleep(1)

  except websockets.ConnectionClosed:
    print('disconnected')

  except KeyboardInterrupt:
    print('\nCtrl-C (SIGINT) caught. Exiting...')  

  finally:
    # Remove connection from list
    users.connected.remove(websocket)

if __name__ == '__main__':
  HOST = get_ipaddress()

  loop = asyncio.get_event_loop()
  start_server = websockets.serve(receive_send, HOST, 3000)
  server = loop.run_until_complete(start_server)
  print('Listen')

  t = Thread(target=httpHandler, args=(HOST, 9000))
  t.daemon = True
  t.start()

  try:
    loop.run_forever()
  finally:
    server.close()
    start_server.close()
    loop.close()
