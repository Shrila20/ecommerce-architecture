from flask import Flask, jsonify, request, send_from_directory
import sqlite3, os
app=Flask(__name__, static_folder='static')
DB=os.getenv('DB_PATH','shop.db')
PRODUCTS=[{'id':1,'name':'Everyday Sneakers','category':'Footwear','price':2499,'emoji':'👟','color':'#f0e8dc','description':'Lightweight comfort for everyday miles.'},{'id':2,'name':'Studio Headphones','category':'Audio','price':3299,'emoji':'🎧','color':'#e3e9f5','description':'Immersive sound, all-day comfort.'},{'id':3,'name':'Canvas Tote','category':'Accessories','price':799,'emoji':'👜','color':'#f2e7d8','description':'Roomy, durable and ready to go.'},{'id':4,'name':'Minimal Watch','category':'Accessories','price':1899,'emoji':'⌚','color':'#e6ece4','description':'A clean look for every occasion.'},{'id':5,'name':'Ceramic Mug Set','category':'Home','price':599,'emoji':'☕','color':'#f1e3e3','description':'A little everyday ritual, made better.'},{'id':6,'name':'Travel Backpack','category':'Bags','price':2199,'emoji':'🎒','color':'#e5e6f2','description':'Smart storage for your next adventure.'}]
def db():
 c=sqlite3.connect(DB); c.row_factory=sqlite3.Row; return c
with db() as c:
 c.execute('CREATE TABLE IF NOT EXISTS orders(id INTEGER PRIMARY KEY AUTOINCREMENT, customer TEXT, items TEXT, total REAL, created_at TEXT DEFAULT CURRENT_TIMESTAMP)')
@app.get('/')
def home(): return send_from_directory('static','index.html')
@app.get('/api/products')
def products(): return jsonify(PRODUCTS)
@app.get('/api/orders')
def orders():
 with db() as c: rows=c.execute('SELECT * FROM orders ORDER BY id DESC').fetchall()
 return jsonify([dict(r) for r in rows])
@app.post('/api/orders')
def create_order():
 data=request.get_json(force=True); items=data.get('items',[]); total=sum(next((p['price']*int(i.get('qty',1)) for p in PRODUCTS if p['id']==i.get('id')),0) for i in items)
 if not items: return jsonify({'error':'Cart is empty'}),400
 with db() as c: cur=c.execute('INSERT INTO orders(customer,items,total) VALUES(?,?,?)',(data.get('customer','Guest'),str(items),total)); oid=cur.lastrowid
 return jsonify({'id':oid,'customer':data.get('customer','Guest'),'items':items,'total':total,'status':'confirmed'}),201
if __name__=='__main__': app.run(host='0.0.0.0',port=5000,debug=True)
