import logging

import requests
from django.conf import settings
from rest_framework.status import HTTP_200_OK

from posts.exceptions import RetryError

logger = logging.getLogger(__name__)


class ModerationService:
    def __init__(self):
        self.host = settings.MODERATION_SERVICE_HOST

    def check_sentence(self, sentence):
        response = requests.post(f"{self.host}sentences/", json={"fragment": sentence})
        if response.status_code == HTTP_200_OK:
            return response.json()["has_foul_language"]
        else:
            logger.error(
                f"Moderation service API request failed response code:{response.status_code}, text: {response.text}"
            )
            raise RetryError()
