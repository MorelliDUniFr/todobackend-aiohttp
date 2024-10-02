import asyncio
import motor.motor_asyncio
from uuid import uuid4
from os import getenv

MONGO_URI = getenv('MONGO_URI', 'mongodb://localhost:27017')
DB_NAME = getenv('DB_NAME', 'todoapp')

async def populate_db():
    client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
    db = client[DB_NAME]

    task = {
        '_id': str(uuid4()),
        'title': 'Sample Task',
        'completed': False,
        'tags': [],
        'url': 'http://localhost:8000/todos/sample-task'
    }
    tag = {
        '_id': str(uuid4()),
        'title': 'Sample Tag',
        'todos': [task['_id']],
        'url': 'http://localhost:8000/tags/sample-tag'
    }

    task['tags'].append(tag['_id'])

    await db['tasks'].insert_one(task)
    await db['tags'].insert_one(tag)
    print("Database populated with sample data!")


loop = asyncio.get_event_loop()
loop.run_until_complete(populate_db())
