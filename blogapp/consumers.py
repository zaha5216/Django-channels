import asyncio
import json
from django.contrib.auth.models import User
from blogapp.models import Comment, Post

from channels.db import database_sync_to_async
from channels.consumer import AsyncConsumer



class CommentConsumer(AsyncConsumer):

    async def websocket_connect(self, event):
        print('connection successfull', event)
        await self.send({
                'type': 'websocket.accept'
            })
        post_id = await self.get_post_id(self.scope['url_route']['kwargs']['slug'])
        self.post = 'post' + post_id
        await self.channel_layer.group_add(
            self.post,
            self.channel_name
        )

    async def websocket_receive(self,event):
        print('received: ', event)
        new_comment_data = event.get('text')
        new_comment = json.loads(new_comment_data)
        post_slug = new_comment['post_slug']
        author = new_comment['author']
        comment_text = new_comment['comment_text']
        await self.create_comment(post_slug, author, comment_text)
        comment = {
            'comment_text': comment_text,
            'author': author
        }
        await self.channel_layer.group_send(
            self.post,
            {
                'type': 'show_comment',
                'text': json.dumps(comment)
            }
        )

    @database_sync_to_async
    def create_comment(self, post_slug, author, comment_text):
        author = User.objects.get(username=author)
        post = Post.objects.get(slug=post_slug)
        Comment.objects.create(post=post, author=author, comment_text=comment_text)

    @database_sync_to_async
    def get_post_id(self, post_slug):
        return str(Post.objects.get(slug=post_slug).id)

    async def show_comment(self, event):
        await self.send({
            'type': 'websocket.send',
            'text': event['text']
        })




