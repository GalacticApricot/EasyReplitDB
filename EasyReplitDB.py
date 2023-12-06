import json
import sqlite3
import atexit

class _EventDict(dict):
  def __init__(self, cursor):
      self.cursor = cursor
      super(_EventDict, self).__init__()

  def prefix(self, prefix):
      query = "SELECT key FROM data WHERE key LIKE ?;"
      self.cursor.execute(query, (f'{prefix}%',))
      result = self.cursor.fetchall()
      keys_with_prefix = [item[0] for item in result]
      return keys_with_prefix

  def __setitem__(self, key, value):
      super(_EventDict, self).__setitem__(key, value)
      self.update({key: value})
      self.commit()

  def __delitem__(self, key):
      super(_EventDict, self).__delitem__(key)
      self.cursor.execute("DELETE FROM data WHERE key = ?;", (key,))
      self.commit()

  def update(self, *args, **kwargs):
      super(_EventDict, self).update(*args, **kwargs)
      for key, value in dict(*args, **kwargs).items():
          self.cursor.execute("INSERT OR REPLACE INTO data (key, value) VALUES (?, ?);", (key, value))
      self.commit()

  def keys(self):
      query = "SELECT key FROM data;"
      self.cursor.execute(query)
      result = self.cursor.fetchall()
      keys = [item[0] for item in result]
      return keys

  def commit(self):
      self.cursor.connection.commit()


with open('configs.json') as configs:
    config = json.loads(configs.read())
db_path = config["database path"]
connection = sqlite3.connect(db_path)
cursor = connection.cursor()
db = _EventDict(cursor)


create_table_query = '''CREATE TABLE IF NOT EXISTS data (
  key TEXT PRIMARY KEY,
  value TEXT
);
'''
cursor.execute(create_table_query)
connection.commit()


@atexit.register
def close_connection():
    global connection, cursor
    cursor.close()
    connection.close()

