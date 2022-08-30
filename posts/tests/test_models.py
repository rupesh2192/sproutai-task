from django.test import TestCase

from posts.models import Sentence
from posts.tests.utils import create_post, create_sentences, create_paragraph


class PostsModelsTestCase(TestCase):
    def setUp(self):
        self.post = create_post()
        self.paragraph = create_paragraph(post=self.post)
        self.sentences = create_sentences(paragraph=self.paragraph)

        self.post_none = create_post()
        self.paragraph_none = create_paragraph(post=self.post_none)
        self.sentences_none = create_sentences(paragraph=self.paragraph_none, has_foul_language=None)

        self.foul_post = create_post()
        self.foul_paragraph = create_paragraph(post=self.foul_post)
        self.foul_sentences = create_sentences(paragraph=self.foul_paragraph, has_foul_language=True)

    def test_post_update_foul_language_true(self):
        """Test if Post.update_foul_language updates the has_foul_language column correctly"""
        self.assertEqual(self.foul_post.has_foul_language, None)
        self.foul_post.update_foul_language()
        self.assertEqual(self.foul_post.has_foul_language, True)

    def test_post_update_foul_language_false(self):
        """Test if Post.update_foul_language updates the has_foul_language column correctly"""
        self.assertEqual(self.post.has_foul_language, None)
        self.post.update_foul_language()
        self.assertEqual(self.post.has_foul_language, False)

    def test_post_update_foul_language_none(self):
        """Test if Post.update_foul_language updates the has_foul_language column correctly"""
        self.assertEqual(self.post_none.has_foul_language, None)
        self.post_none.update_foul_language()
        self.assertEqual(self.post_none.has_foul_language, None)

    def test_property_post_sentences(self):
        """Test if Post.sentences property returns appropriate results"""
        expected = Sentence.objects.filter(paragraph__post=self.post).order_by("order")
        self.assertQuerysetEqual(self.post.sentences, expected)
