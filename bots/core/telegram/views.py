from rest_framework import status, views

from slack.core.alerts import send_exception
from . import factory
from .exceptions import PermissionException


class APIHookProcessing(views.APIView):
    def post(self, request, token_key):
        handler = factory.get_handler_by_token(token_key)
        try:
            handler.parse_message(request.data['message'])
            handler.run()
        except PermissionException as exc:
            handler.client.send_message(
                chat_id=handler.message['chat'].chat_id,
                prepared_message=exc.args[0]
            )
        except Exception as exc:
            send_exception(exc, details={'request': request.data})
        return views.Response(status=status.HTTP_200_OK)
