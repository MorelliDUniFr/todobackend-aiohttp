from os import getenv
from uuid import uuid4

class Task:

    @classmethod
    def get_collection(cls, db):
        return db['tasks']

    @classmethod
    async def create_object(cls, db, content, url_for, tag_id=None):
        uuid = str(uuid4())
        HOST = getenv('HOST', 'localhost:8000')

        obj = {
            '_id': uuid,
            'id': uuid,
            'completed': False,
            'tags': [],
            'length': 0,
            'url': 'http://{HOST}{}'.format(
                url_for(uuid=uuid).path, **locals())
        }
        obj.update(content)

        if tag_id:
            obj['tags'].append(tag_id)

        await cls.get_collection(db).insert_one(obj)
        return obj

    @classmethod
    async def all_objects(cls, db):
        tasks = await cls.get_collection(db).find().to_list(length=None)
        return tasks

    @classmethod
    async def delete_all_objects(cls, db):
        await cls.get_collection(db).delete_many({})

    @classmethod
    async def get_object(cls, db, uuid):
        task = await cls.get_collection(db).find_one({'_id': uuid})
        if task:
            task['id'] = task['_id']
        return task

    @classmethod
    async def delete_object(cls, db, uuid):
        await cls.get_collection(db).delete_one({'_id': uuid})

    @classmethod
    async def update_object(cls, db, uuid, value):
        await cls.get_collection(db).update_one({'_id': uuid}, {'$set': value})

    @classmethod
    async def find_by_tag(cls, db, tag_id):
        # Get a list of all tasks
        tasks = await cls.get_collection(db).find().to_list(length=None)

        for task in tasks:
            task['id'] = task['_id']

        return tasks

    @classmethod
    async def add_tag(cls, db, uuid, tag_id):
        task = await cls.get_object(db, uuid)
        tag = await Tag.get_tag(db, tag_id)

        if task and tag:
            task['tags'].append(tag)
            task['length'] = len(task['tags'])
            await cls.update_object(db, uuid, {'tags': task['tags'], 'length': task['length']})

            tag['todos'].append(uuid)
            tag['length'] = len(tag['todos'])
            await Tag.update_tag(db, tag_id, {'todos': tag['todos'], 'length': tag['length']})

            return task
        return None

    @classmethod
    async def delete_tags(cls, db, uuid):
        task = await cls.get_object(db, uuid)
        tags = task.get('tags', [])

        for tag in tags:
            tag_id = tag.get('id')
            await Tag.delete_tag(db, tag_id)

        task['tags'].clear()
        task['length'] = len(task['tags'])
        await cls.update_object(db, uuid, task)

        return task


class Tag:

    @classmethod
    def get_collection(cls, db):
        return db['tags']

    @classmethod
    async def create_tag(cls, db, content, url_for, task_id=None):
        tag_id = str(uuid4())
        HOST = getenv('HOST', 'localhost:8000')

        obj = {
            '_id': tag_id,
            'id': tag_id,
            'title': content.get('title'),
            'todos': [],
            'url': 'http://{HOST}{}'.format(
                url_for(tag_id=tag_id).path, **locals())
        }
        obj.update(content)

        await cls.get_collection(db).insert_one(obj)
        return obj

    @classmethod
    async def get_tags(cls, db):
        tags = await cls.get_collection(db).find().to_list(length=None)
        for tag in tags:
            tag['id'] = tag['_id']
        return tags

    @classmethod
    async def get_tag(cls, db, tag_id):
        tag = await cls.get_collection(db).find_one({'_id': tag_id})
        if tag:
            tag['id'] = tag['_id']
        return tag

    @classmethod
    async def delete_tag(cls, db, tag_id):
        await cls.get_collection(db).delete_one({'_id': tag_id})

        await Task.get_collection(db).update_many(
            {'tags': tag_id}, {'$pull': {'tags': tag_id}}
        )

    @classmethod
    async def delete_all_tags(cls, db):
        await cls.get_collection(db).delete_many({})

    @classmethod
    async def update_tag(cls, db, tag_id, content):
        await cls.get_collection(db).update_one({'_id': tag_id}, {'$set': content})
        tag = await cls.get_tag(db, tag_id)
        return tag
