from fastapi import FastAPI, HTTPException
import uvicorn
import logging

from src.api.routers.auth.router import router as auth_router

app = FastAPI()


app.include_router(auth_router)

@app.on_event("startup")
async def startup_event():
    logging.warning("Application started")






