"""Zoom.us REST API Python Client -- Chat Messages component"""

from zoomapi import util
from zoomapi.components import base


class ChatMessagesComponentV2(base.BaseComponent):
    """Component dealing with all chat messages related matters"""

    def list(self, **kwargs):
        util.require_keys(kwargs, "user_id")
        return self.get_request(
                "/chat/users/{}/messages".format(kwargs.get("user_id")), params=kwargs
        )

    def post(self, **kwargs):
        util.require_keys(kwargs, "message")
        return self.post_request("/chat/users/me/messages", data=kwargs)

    def put(self, **kwargs):
        util.require_keys(kwargs, "message_id")
        return self.put_request("/chat/users/me/messages/{}".format(kwargs.get("message_id")), data=kwargs)

    def delete(self, **kwargs):
        util.require_keys(kwargs, "message_id")
        return self.delete_request("/chat/users/me/messages/{}".format(kwargs.get("message_id")), params=kwargs)
