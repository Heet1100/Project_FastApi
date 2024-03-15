import uvicorn
from fastapi import FastAPI
from src.api.routes import route
from src.core.config import Settings as s

app = FastAPI()

app.include_router(route.route)






