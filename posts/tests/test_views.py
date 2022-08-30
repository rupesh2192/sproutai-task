from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse

from posts.serializers import PostSerializer
from posts.tests.utils import create_post, create_paragraph, create_sentences
from django.test import Client


class PostsViewsTestCase(TestCase):
    def setUp(self):
        self.post = create_post()
        self.paragraph = create_paragraph(post=self.post)
        self.sentences = create_sentences(paragraph=self.paragraph, has_foul_language=None)
        self.client = Client()

    @patch("posts.tasks.check_sentence_moderation", return_value=True)
    def test_check_post_moderation(self, mocked_check_sentence_moderation):
        """Test API posts/{id}/check"""
        response = self.client.get(reverse('posts-check', args=[self.post.id]))
        serializer = PostSerializer(self.post)
        self.assertDictEqual(response.data, serializer.data)