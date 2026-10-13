from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3,os
app=FastAPI(title='User Service'); DB=os.getenv('DB_PATH','/data/users.db'); os.makedirs(os.path.dirname(DB),exist_ok=True)
with sqlite3.connect(DB) as c:c.execute('CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT,email TEXT UNIQUE)')
class UserIn(BaseModel): name:str; email:str
@app.get('/health')
def health():return {'service':'user-service','status':'ok'}
@app.get('/api/users')
def users():
 with sqlite3.connect(DB) as c:c.row_factory=sqlite3.Row;return [dict(r) for r in c.execute('SELECT * FROM users ORDER BY id DESC')]
@app.post('/api/users',status_code=201)
def create_user(u:UserIn):
 with sqlite3.connect(DB) as c:
  try:cur=c.execute('INSERT INTO users(name,email) VALUES(?,?)',(u.name,u.email));return {'id':cur.lastrowid,'name':u.name,'email':u.email}
  except sqlite3.IntegrityError:return {'error':'Email already exists'}
