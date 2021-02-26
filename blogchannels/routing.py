from django.conf.urls import url
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from channels.auth import AuthMiddlewareStack

from blogapp.consumers import CommentConsumer

application = ProtocolTypeRouter({
        'websocket' : AllowedHostsOriginValidator(
           AuthMiddlewareStack(
              URLRouter([
                 url(r'post/(?P<slug>[-\w]+)/$', CommentConsumer)
              ])
           )
        )

   })