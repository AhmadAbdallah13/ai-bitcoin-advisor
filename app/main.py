from contextlib import asynccontextmanager

from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler

from app import websocket

# Create scheduler
scheduler = BackgroundScheduler()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    scheduler.add_job(websocket.periodic_task, "interval", minutes=60) # change to seconds if needed for testing
    scheduler.start()
    print("Scheduler started")

    yield  # Application runs here

    # Shutdown logic
    scheduler.shutdown()
    print("Scheduler shut down")

# Create FastAPI app
app = FastAPI(lifespan=lifespan)

app.include_router(websocket.router)
