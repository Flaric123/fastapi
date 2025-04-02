from fastapi import FastAPI, Path, Query, HTTPException
from typing import Optional, Annotated
from pydantic import BaseModel 
import json
app = FastAPI()

class Item(BaseModel):
    name:str
    description: str|None=None
    price: float
    id: int

@app.get("/items")
async def get_items(
    name: Optional[str] = Query(None, min_length=2),
    min_price: Optional[float] = Query(None, ge=0),
    max_price: Optional[float] = Query(None),
    limit: Optional[int] = Query(10, ge=1, le=100)
    ):

    with open('items.json','r') as items:
        data=json.load(items)

    if name:
        data = [item for item in data if name.lower() in item.get("name",'').lower()]
    
    if min_price:
        data = [item for item in data if item.get("price", 0) >= min_price]
    
    if max_price:
        data = [item for item in data if item.get("price", 0) <= max_price]
    
    if min_price and max_price and min_price > max_price:
        return {"error": "Min price cannot be greater than max price."}
    
    return data[:limit]

@app.get("/items/{item_id}")
async def get_item_by_id(item_id: Annotated[int, Path(title="The ID of the item to get", ge=1)]):
    with open('items.json','r') as items:
        data=json.load(items)

    response=list(filter(lambda item:item["id"]==item_id,data))

    if response:
        return response
    else:
        return HTTPException(404, 'Товар с таким id не найден')
    
@app.post("/items/")
async def create_item(item:Item):
    with open('items.json','r') as items:
        data=json.load(items)
    if len(list(filter(lambda x:x["id"]==item.id,data)))>0:
        return HTTPException(400, 'Товар с таким id уже существует')
    else:
        item.id=data[-1]["id"]
        return item