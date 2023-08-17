### Users API ###

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

router = APIRouter(prefix="/users", 
                   tags=["users"],
                   responses={404: {"message": "No encontrado"}})

#Entidad user
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

@router.get("/json")
async def usersjson():
    return [{"name":"Bibi", "surname": "Ruiz", "url": "bruiz.es"},
            {"name":"Cristina", "surname": "Usero", "url": "cusero.es"},
            {"name":"Álvaro", "surname": "Ruiz", "url": "aruiz.es"},
            {"name":"Martín", "surname": "Ruiz", "url": "mruiz.es"}]

@router.get("/class", response_model=User)
async def userclass():
    return User(name = "Bibi", surname= "Ruiz", url ="bruiz.es", age=39 )

@router.get("/")
async def users():
    return users_list

# Path
@router.get("/{id}", response_model=User)
async def user(id: int):
    return search_user(id)
    
# Query
@router.get("/query/", response_model=User)
async def user(id: int):
    return search_user(id)

@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def user(user: User):
    if type(search_user(user.id)) == User:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El usuario ya existe")
    users_list.append(user)
    return user

@router.put("/")
async def user(user: User):  
    found = False
    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[index] = user
            found = True

    if not found:
        return {"error": "No se ha actualizado el usuario"}
    
    return user
    
@router.delete("/{id}")
async def user(id: int):
    found = False
    for index, saved_user in enumerate(users_list):
        if saved_user.id == id:
            del users_list[index]
            found = True

    if not found:
        return {"error": "Ese usuario no existe"}
    
    return user

    
def search_user(id: int):
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return {"error": "No se ha encontrado el usuario"}
    