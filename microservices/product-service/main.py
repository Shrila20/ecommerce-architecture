from fastapi import FastAPI
app=FastAPI(title='Product Service')
products=[{'id':1,'name':'Everyday Sneakers','category':'Footwear','price':2499,'emoji':'👟','color':'#f0e8dc','description':'Lightweight comfort for everyday miles.'},{'id':2,'name':'Studio Headphones','category':'Audio','price':3299,'emoji':'🎧','color':'#e3e9f5','description':'Immersive sound, all-day comfort.'},{'id':3,'name':'Canvas Tote','category':'Accessories','price':799,'emoji':'👜','color':'#f2e7d8','description':'Roomy, durable and ready to go.'},{'id':4,'name':'Minimal Watch','category':'Accessories','price':1899,'emoji':'⌚','color':'#e6ece4','description':'A clean look for every occasion.'},{'id':5,'name':'Ceramic Mug Set','category':'Home','price':599,'emoji':'☕','color':'#f1e3e3','description':'A little everyday ritual, made better.'},{'id':6,'name':'Travel Backpack','category':'Bags','price':2199,'emoji':'🎒','color':'#e5e6f2','description':'Smart storage for your next adventure.'}]
@app.get('/health')
def health(): return {'service':'product-service','status':'ok'}
@app.get('/api/products')
def get_products(): return products
@app.get('/api/products/{product_id}')
def get_product(product_id:int): return next((p for p in products if p['id']==product_id),{'error':'Not found'})
