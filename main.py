# pylint: disable=C0115:missing-class-docstring,C0114:missing-module-docstring
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
import uvicorn
from app.api.endpoints import index,user
app = FastAPI(docs_url="/docs")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Add your frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
    expose_headers=["*"]
)
app.include_router(index.router)
app.include_router(user.router)

if __name__ == '__main__':
    uvicorn.run('main:app',reload=True,port=8084)
