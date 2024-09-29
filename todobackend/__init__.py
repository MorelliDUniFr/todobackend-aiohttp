from logging import getLogger, basicConfig, INFO
from os import getenv

import motor.motor_asyncio
from aiohttp import web
import aiohttp_cors
from aiohttp_swagger import setup_swagger

from .views import (
    IndexView,
    TodoView, TagView, TagDetailView, TodoTagView, TodoTagsView, TagTodosView
)

IP = getenv('IP', '0.0.0.0')
PORT = getenv('PORT', '8000')

basicConfig(level=INFO)
logger = getLogger(__name__)

MONGO_URI = getenv('MONGO_URI', 'mongodb://localhost:27017')
DB_NAME = getenv('DB_NAME', 'todoapp')

async def init(loop):
    client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
    db = client[DB_NAME]

    app = web.Application(loop=loop)
    app['db'] = db

    # Configure default CORS settings.
    cors = aiohttp_cors.setup(app, defaults={
        "*": aiohttp_cors.ResourceOptions(
                allow_credentials=True,
                expose_headers="*",
                allow_headers="*",
                allow_methods="*",
            )
    })

    # Routes
    cors.add(app.router.add_view('/todos/', IndexView, name='index'))  # GET, POST, DELETE
    cors.add(app.router.add_view('/todos/{uuid}', TodoView, name='todo'))  # GET, DELETE, PATCH
    cors.add(app.router.add_view('/todos/{uuid}/tags/', TodoTagsView, name='todo_tags'))  # GET, POST, DELETE
    cors.add(app.router.add_view('/todos/{uuid}/tags/{tag_id}', TodoTagView, name='todo_tag'))  # DELETE
    cors.add(app.router.add_view('/tags/', TagView, name='tags'))  # GET, POST, DELETE
    cors.add(app.router.add_view('/tags/{tag_id}', TagDetailView, name='tag'))  # GET, DELETE, PATCH
    cors.add(app.router.add_view('/tags/{tag_id}/todos/', TagTodosView, name='todos_by_tag'))  # GET

    # Config
    setup_swagger(app, swagger_url="/api/v1/doc", swagger_from_file="swagger.yaml")
    logger.info("Starting server at %s:%s", IP, PORT)
    srv = await loop.create_server(app.make_handler(), IP, PORT)
    return srv
