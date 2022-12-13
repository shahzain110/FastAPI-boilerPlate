from fastapi import FastAPI, File, UploadFile, Form, Header, Request
from fastapi.responses import FileResponse
import os 

#Fast API Object
app = FastAPI() 

# origins = ["*"]  
# origins = ["https://user-app.click", "https://user-app.click/", "https://voltox.tech/", "https://voltox.tech" ,"https://voltox.global/", "https://voltox.global","https://super-admin.click/", "https://super-admin.click" ,"http://localhost:3000/","http://localhost:3000"]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"], 
#     # allow_headers=["Content-Type", "Authorization","Access-Control-Allow-Origin", "Access-Control-Allow-Credentials","application/json"]
#     ) 

#ID card scanning API  
@app.post('/PATH_HERE') 
async def face_verification(): 
    try:
        pass
    except Exception as e:
        pass
