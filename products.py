from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel): #Usando BaseModel, crea por debajo toda la estructura de una clase como el constructor
    id: int
    name: str
    surname: str
    url: str
    age: int

users_list = [User(id=1, name = "Bibi", surname= "Ruiz", url ="bruiz.es", age=39 ),
           User(id=2, name = "Cristina", surname= "Usero", url ="cusero.es", age=36 ),
           User(id=3, name = "Alvaro", surname= "Ruiz", url ="aruiz.es", age=8 ),
           User(id=4, name = "Martin", surname= "Ruiz", url ="mruiz.es", age=4 )]


@app.get("/products")
async def products():
    return ["Producto 1", "Producto 2", "Producto 3", "Producto 4", "Producto 5"]