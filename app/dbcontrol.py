#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pyodbc

class DB():
  # Initialize
  def __init__(self):
    self.connection = 0
    self.cursor = 0

  # Open DB
  def OpenDB(self):
    self.connection = pyodbc.connect("DRIVER={SQL Server};SERVER=TT-Sprint\SQLEXPRESS;UID=sa;PWD=SQLToDo123;DATABASE=ToDo")
    self.cursor = self.connection.cursor()

  # Close DB
  def CloseDB(self):
    self.cursor.close()
    self.connection.close()

  # Insert record
  def AddToDo(self, name, description):
    self.cursor.execute("INSERT INTO Data(name, description) VALUES (?, ?)" , name, description)
    self.connection.commit()

  # Delete records
  def DeleteToDo(self, name):
    self.cursor.execute("DELETE FROM Data WHERE name = ?", name)
    self.connection.commit()

  # List records
  def ListToDo(self):
    self.cursor.execute("SELECT name,description FROM Data")
    records = self.cursor.fetchall()

    # Format records
    data = ""
    for record in records:
        data += record[0] + " " + record[1] + "\n"
    data = data.rstrip()
    return data
