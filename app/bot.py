#!/usr/bin/env python
# -*- coding: utf-8 -*-
import dbcontrol
import users

class Bot():
  # Initialize
  def __init__(self):
    self.db = dbcontrol.DB()

  # Execute command
  def exec(self, command):
    if (command[0] != "bot"):
      return ""

    if (command[1] == "ping"):
      return self.__ping(command)
    elif (command[1] == "todo"):
      return self.__todo(command)
    elif (command[1] == "activeuser"):
      return self.__activeuser(command)
    elif (command[1] == "help"):
      return self.__help(command)
    else:
      return ""

  # Handle "ping"
  def __ping(self, command):
    return "pong"

  # Handle "todo"
  def __todo(self, command):
    if (len(command) < 3):
      return ""

    try:
      if (command[2] == "add"):
        return self.__todo_add(command)
      elif (command[2] == "delete"):
        return self.__todo_delete(command)
      elif (command[2] == "list"):
        return self.__todo_list(command)
      else:
        return ""
    except (pyodbc.Error) as e:
      print (e)
      print (e.args[1])
      return ""

  # Handle "todo add"
  def __todo_add(self, command):
    if (len(command) >= 5):
      name = command[3]

      description = ""
      i = 4
      while (i < len(command)):
        description += command[i] + " "
        i = i + 1
      description.rstrip(" ")

      self.db.OpenDB()
      self.db.AddToDo(name, description)
      self.db.CloseDB()

      return "todo added"

    return ""

  # Handle "todo delete"
  def __todo_delete(self, command):
    if (len(command) >= 4):
      name = command[3]

      self.db.OpenDB()
      self.db.DeleteToDo(name)
      self.db.CloseDB()

      return "todo deleted"

    return ""

  # Handle "todo list"
  def __todo_list(self, command):
    self.db.OpenDB()
    data = self.db.ListToDo()
    self.db.CloseDB()

    if (data != ""):
      return data
    else:
      return "todo empty"

  # Handle "activeuser"
  def __activeuser(self, command):
    return str(len(users.connected))

  # Handle "help"
  def __help(self, command):
    if (len(command) < 3):
      help = "commandlist: ping, todo, activeuser, help"
    elif (command[2] == "ping"):
      help = "ping: Return 'pong'"
    elif (command[2] == "todo"):
      if (len(command) < 4):
        help = "todo commandlist: add, delete, list"
      elif (command[3] == "add"):
        help = "todo add [name] [description]: Add todo"
      elif (command[3] == "delete"):
        help = "todo delete [name]: Delete todo which name is [name]"
      elif (command[3] == "list"):
        help = "todo list: Return list all todo"
      else:
        help = "invalid command: " + command[2] + " " + command[3]
    elif (command[2] == "activeuser"):
      help = "activeuser: Return number of active user"
    elif (command[2] == "help"):
      help = "help [command]: Show help"
    else:
      help = "invalid command: " + command[2]

    return help
