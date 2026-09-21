from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from database import InitializeDatabase
from api.router import router as pagesRouter

app:FastAPI = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:5173', 'http://localhost:3000', '*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)
app.mount('/static', StaticFiles(directory='static'), name='static')

app.include_router(pagesRouter)

InitializeDatabase()