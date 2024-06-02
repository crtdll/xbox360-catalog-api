import sqlite3, os

def dict_factory(cursor, row):
  d = {}
  for idx, col in enumerate(cursor.description):
    d[col[0]] = row[idx]
  return d

class Database:
  def __init__(self, db_name='data.sqlite') -> None:
    self.db_name = db_name
    self.db = None
    self.cur = None

  def connect(self):
    try:
      if not os.path.exists(self.db_name):
        return False

      self.db = sqlite3.connect(self.db_name)
      self.db.row_factory = dict_factory
      self.cur = self.db.cursor()
      return True
    except Exception as e:
      print(e)
      return False

  def search_full_title(self, query_string):
    query = 'SELECT * FROM games WHERE LOWER(full_title) LIKE ?'
    search_term = f"%{query_string.lower()}%"
    self.cur.execute(query, (search_term,))
    return [{key: row[key] for key in row.keys()} for row in self.cur.fetchall()]
  
  def search_banner_img(self, id):
    query = 'SELECT * FROM images WHERE id = ?'
    self.cur.execute(query, (id,))
    
    results = self.cur.fetchall()
    if results:
      return results[0]['url'] 
     
    return 'No image available'