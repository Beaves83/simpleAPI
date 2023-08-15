from fastapi import FastAPI 
from routers import products, users, basic_auth_users, jwt_auth_users
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Routers
app.include_router(products.router)
app.include_router(users.router)
app.include_router(basic_auth_users.router)
app.include_router(jwt_auth_users.router)



app.mount("/static", StaticFiles(directory="static"), name="static")

#Url local: http://127.0.0.1:8000

@app.get("/") #Esto es para el contexto de fastapi
async def root(): #Esto es una función de python puro
    return "Hello world!" #Todas las funciones al servidor tienes que ser asincronas

@app.get("/url")
async def url():
    return { "url": "https://web.es" }

#Inicia el server: uvicorn main:app --reload

#Documentación con Swagger: http://127.0.0.1:8000/docs
#Documentación con Redocly: http://127.0.0.1:8000/redoc