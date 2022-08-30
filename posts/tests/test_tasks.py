from unittest.mock import patch

from django.test import TransactionTestCase

from posts.tasks import moderation_check_task, check_sentence_moderation
from posts.tests.utils import create_post, create_paragraph, create_sentences


class PostsTasksTestCase(TransactionTestCase):
    def setUp(self):
        self.post = create_post()
        self.paragraph = create_paragraph(post=self.post)
        self.sentences = create_sentences(paragraph=self.paragraph, has_foul_language=None)

    @patch("posts.tasks.check_sentence_moderation", return_value=True)
    def test_moderation_check_task(self, mocked_check_sentence_moderation):
        """Test moderation_check_task"""
        moderation_check_task(post_id=self.post.id)
        sentences = self.post.sentences.filter(has_foul_language=None)
        self.assertEqual(mocked_check_sentence_moderation.call_count, sentences.count())

    @patch("posts.services.moderation.ModerationService.check_sentence", return_value=True)
    def test_check_sentence_moderation(self, mocked_check_sentence_moderation):
        """Test check_sentence_moderation"""
        sentence = self.post.sentences.last()
        sentence.has_foul_language = False
        sentence.save()
        check_sentence_moderation(sentence.id)
        sentence.refresh_from_db()
        self.assertTrue(sentence.has_foul_language)
