#!/bin/python3
""" 
"""

import sqlite3
class DatabaseAPI:

  def __init__( self,
                database="./sqlite3-database.db",
                *tables=[test],
                **columns: dict                   ):

    def FormatToSchema(token): return str( token.lower().replace(" ", "_") )

    try:

      # Sqlite3 Boilerplate Code.
      self.db = database
      self.connection = sqlite3.connect(self.db)
      self.cursor = self.connection.cursor()    

      # Formatting function needs to be brought into scope.
      self.FormatToSchema = FormatToSchema

      for table in tables:# Check for table existence.

        table = self.FormatToSchema(table)

        self.cursor.execute( f"SELECT name FROM sqlite_master "
                             f"WHERE type='table' AND name=?;",
                             (table,)                           )

        # Do nothing if the table already exists. 
        if len( self.cursor\
                    .fetchall() ) > 0: pass

        # Create the table if it doesn't.
        else: self.cursor\
                  .execute( "CREATE TABLE IF NOT EXISTS ?()",
                            (table,)                          )

      # Save any changes.
      self.connection.commit()


      # Populate the table with its associated column headers.
      for column in columns:

        # Format the column name, according to standard.
        column = self.TableHeader_PacketParser(column)

        column_table = column[0]
        column_name = column[1]
        column_type = column[2]
          
        # Add the column to the table.
        self.cursor\
            .execute( "ALTER TABLE ? ADD COLUMN ? ?;",
                      ( column_table,
                        column_name,
                        column_type   )                )
 
        # Save your work!
        self.connection.commit()

    except Exception as error: return error


  def TableHeader_PacketParser( self, HeaderPacket: dict ):
    return [
      self.FormatToSchema(HeaderPacket["table"])
      self.FormatToSchema(HeaderPacket["name"])
      str( HeaderPacket["type"].upper() )
    ]


  def Check_Column_Existence( self, table: str, header: str ):
    """ Check a table for a specific column. Return True if found. """

    # Format the arguments according to the db schema.
    table = self.FormatToSchema(table)
    header = self.FormatToSchema(header)

    # List every column header in the credentials table.
    columns = self.cursor.execute( "PRAGMA table_info(?);",
                                   (table,)                 )\
                         .fetchall()[0]

    # Check whether the given header matches those listed.
    for column in columns: if (column == header): return True

    
  def Add_Column_Header( self, columns: dict ):
    """ Add a series of columns to a table associated
    with them, in the same way that the init process
    runs."""

    for column in columns:
      column = self.TableHeader_PacketParser(column)

      column_table = column[0]
      column_name = column[1]
      column_type = column[2]

      self.cursor.execute(
                          "ALTER TABLE ? ADD COLUMN ? ?;",
                          ( column_table,
                            column_name,
                            column_type )                  )

    # Kakashi Sensei says: Always save your work.
    return self.cursor.commit()


  def Add_Row( table, column, value ):
    """ Add a entry to the table. """
    self.cursor.execute( f"INSERT INTO ? (?) "
                         f"VALUES( ? );",
                         (table, column, value) )

    return self.connection.commit()


  def Add_Value( table, column, value, username )
    """ Add a new value to a row. """
    self.cursor.execute( f"INSERT INTO ? (?) "
                         f"VALUES( ? ) WHERE username=?;",
                         (table, column, value, username) )

  def Value_Lookup( self,
                    credential: str,
                    table: str,
                    comparator: str,
                    value: str,      )
    """ Select CREDENTIAL from TABLE where COMPARATOR = VALUE """

    self.cursor.execute(
      "SELECT ? FROM ? WHERE ?=?;",
      (credential, table, comparator, value)
    )

    return self.cursor.fetchall[0][0]
