from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings

from app.routers import auth_router

from app.database import Base, engine

Base.metadata.create_all(bind=engine)

settings = get_settings()

main = FastAPI(title='WebRTC-360',
               version='0.0.1',
               servers=[{
                   'url': settings.server_url
               }],
               redoc_url=None)

origins = ["http://localhost:3000"]
main.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

main.include_router(auth_router.router, prefix="/auth")


@main.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket) -> None:
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")
