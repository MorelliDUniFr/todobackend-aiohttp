from aiohttp.web import Response, View, json_response
from aiohttp_cors import CorsViewMixin

from .models import Task, Tag

class IndexView(View, CorsViewMixin):
    async def get(self):
        # Fetch all tasks from MongoDB
        tasks = await Task.all_objects(self.request.app['db'])
        return json_response(tasks)

    async def post(self):
        # Create a new task and store it in MongoDB
        content = await self.request.json()
        todo = await Task.create_object(self.request.app['db'], content, self.request.app.router['todo'].url_for)

        return json_response(todo, status=201)

    async def delete(self):
        # Delete all tasks from MongoDB
        await Task.delete_all_objects(self.request.app['db'])
        return Response(status=204)


class TodoView(View, CorsViewMixin):
    async def get(self):
        # Fetch a task by UUID from MongoDB
        uuid = self.request.match_info.get('uuid')
        todo = await Task.get_object(self.request.app['db'], uuid)
        if todo:
            return json_response(todo)
        return json_response({'error': 'Todo not found'}, status=404)

    async def patch(self):
        # Update a task by UUID in MongoDB
        uuid = self.request.match_info.get('uuid')
        content = await self.request.json()
        await Task.update_object(self.request.app['db'], uuid, content)
        updated_todo = await Task.get_object(self.request.app['db'], uuid)
        return json_response(updated_todo)

    async def delete(self):
        # Delete a task by UUID from MongoDB
        uuid = self.request.match_info.get('uuid')
        await Task.delete_object(self.request.app['db'], uuid)
        return Response(status=204)


class TodoTagsView(View, CorsViewMixin):
    async def get(self):
        # Fetch all tags from MongoDB
        response = await Tag.get_tags(self.request.app['db'])
        return json_response(response)

    async def post(self):
        # Add a tag to a task in MongoDB
        content = await self.request.json()
        uuid = self.request.match_info.get('uuid')
        tag_id = content.get('id')
        todo = await Task.add_tag(self.request.app['db'], uuid, tag_id)
        if todo:
            return json_response(todo)
        return json_response({'error': 'Todo not found'}, status=404)

    async def delete(self):
        # Delete all tags from a task in MongoDB
        uuid = self.request.match_info.get('uuid')
        await Task.delete_tags(self.request.app['db'], uuid)
        return Response(status=204)


class TodoTagView(View, CorsViewMixin):
    async def delete(self):
        # Delete a specific tag by ID from MongoDB
        tag_id = self.request.match_info.get('tag_id')
        await Tag.delete_tag(self.request.app['db'], tag_id)
        return Response(status=204)


class TagView(View, CorsViewMixin):
    # Get all tags from MongoDB
    async def get(self):
        tags = await Tag.get_tags(self.request.app['db'])
        return json_response(tags)

    # Create a new tag and save it in MongoDB
    async def post(self):
        content = await self.request.json()
        task_id = content.get('task_id')
        tag = await Tag.create_tag(self.request.app['db'], content, self.request.app.router['tag'].url_for, task_id=task_id)
        return json_response(tag, status=201)

    # Delete all tags from MongoDB
    async def delete(self):
        await Tag.delete_all_tags(self.request.app['db'])
        return Response(status=204)


class TagDetailView(View, CorsViewMixin):
    async def get(self):
        # Fetch a specific tag by ID from MongoDB
        tag_id = self.request.match_info.get('tag_id')
        tag = await Tag.get_tag(self.request.app['db'], tag_id)
        if tag:
            return json_response(tag)
        return json_response({'error': 'Tag not found'}, status=404)

    async def patch(self):
        # Update a specific tag by ID in MongoDB
        tag_id = self.request.match_info.get('tag_id')
        content = await self.request.json()
        updated_tag = await Tag.update_tag(self.request.app['db'], tag_id, content)
        return json_response(updated_tag)

    async def delete(self):
        # Delete a specific tag by ID from MongoDB
        tag_id = self.request.match_info.get('tag_id')
        await Tag.delete_tag(self.request.app['db'], tag_id)
        return Response(status=204)


class TagTodosView(View, CorsViewMixin):
    async def get(self):
        # Fetch todos associated with a specific tag from MongoDB
        tag_id = self.request.match_info.get('tag_id')
        todos = await Task.find_by_tag(self.request.app['db'], tag_id)
        return json_response(todos)
