from unittest import mock
from unittest.mock import patch

import requests
from django.test import TransactionTestCase

from posts.exceptions import RetryError
from posts.services.moderation import ModerationService
from posts.tests.utils import create_post, create_paragraph


def mock_json(*args, **kwargs):
    return {"has_foul_language": True}


class PostsServicesTestCase(TransactionTestCase):
    def setUp(self):
        self.post = create_post()
        self.paragraph = create_paragraph(post=self.post)

    @patch("requests.post")
    def test_moderation_service_check_sentence(self, mocked_post):
        """Test if ModerationService.check_sentence returns expected results"""
        resp = requests.Response()
        resp.status_code = 200
        resp.json = mock_json
        mocked_post.return_value = resp
        temp = ModerationService().check_sentence("test")
        self.assertTrue(temp)

    @patch("requests.post")
    @patch("requests.Response.text")
    @patch("posts.services.moderation.logger.error")
    def test_moderation_service_check_sentence_failure(self, mocked_logger, mocked_response_text, mocked_post):
        """Test if ModerationService.check_sentence logs error and raises RetryError"""
        mocked_response_text.__get__ = mock.Mock(return_value="test")
        resp = requests.Response()
        resp.status_code = 400
        temp = f"Moderation service API request failed response code:{resp.status_code}, text: {resp.text}"
        mocked_post.return_value = resp
        with self.assertRaises(RetryError):
            ModerationService().check_sentence("test sentence")
        mocked_logger.assert_called_with(temp)
