from fastapi import FastAPI
import uvicorn
from app import models
from app.db import engine
from app.routes import router
from dotenv import load_dotenv
import os
load_dotenv()


app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(router)


if __name__ == "__main__":
    uvicorn.run(app=app, host=os.getenv("host"), port=int(os.getenv("port")))
