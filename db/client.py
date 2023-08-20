### MongoDB client ###

# Descarga versión community: https://www.mongodb.com/try/download
# Instalación:https://www.mongodb.com/docs/manual/tutorial
# Módulo conexión MongoDB: pip install pymongo
# Ejecución: sudo mongod --dbpath "/path/a/la/base/de/datos/"
# Conexión: mongodb://localhost

from pymongo import MongoClient

# Conexión BBDD local
# db_client = MongoClient().local


# Conexión BBDD remota
db_client = MongoClient("mongodb+srv://admin:admin@cluster0.xvfnrwc.mongodb.net/").python_fastapi_bbdd.test


