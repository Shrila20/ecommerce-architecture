from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3, os
app=FastAPI(title='Order Service'); DB=os.getenv('DB_PATH','/data/orders.db')
os.makedirs(os.path.dirname(DB),exist_ok=True)
with sqlite3.connect(DB) as c:c.execute('CREATE TABLE IF NOT EXISTS orders(id INTEGER PRIMARY KEY AUTOINCREMENT, customer TEXT, items TEXT, total REAL, status TEXT DEFAULT "confirmed")')
prices={1:2499,2:3299,3:799,4:1899,5:599,6:2199}
class Item(BaseModel): id:int; qty:int=1
class OrderIn(BaseModel): customer:str='Guest'; items:list[Item]
@app.get('/health')
def health():return {'service':'order-service','status':'ok'}
@app.get('/api/orders')
def get_orders():
 with sqlite3.connect(DB) as c: c.row_factory=sqlite3.Row; return [dict(r) for r in c.execute('SELECT * FROM orders ORDER BY id DESC')]
@app.post('/api/orders',status_code=201)
def create_order(o:OrderIn):
 if not o.items: raise HTTPException(400,'Cart is empty')
 total=0
 for item in o.items:
  if item.id not in prices or item.qty<1: raise HTTPException(400,'Invalid product or quantity')
  total+=prices[item.id]*item.qty
 with sqlite3.connect(DB) as c: cur=c.execute('INSERT INTO orders(customer,items,total) VALUES(?,?,?)',(o.customer,str([i.model_dump() for i in o.items]),total)); oid=cur.lastrowid
 return {'id':oid,'customer':o.customer,'items':o.items,'total':total,'status':'confirmed'}
