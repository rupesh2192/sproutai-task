from unittest.mock import patch

from asgiref.sync import async_to_sync
from django.test import TestCase, TransactionTestCase

from posts.models import Post, Sentence
from posts.serializers import SentenceSerializer, PostSerializer
from posts.tests.utils import create_post, create_paragraph


class PostsSerializersTestCase(TransactionTestCase):
    def setUp(self):
        self.post = create_post()
        self.paragraph = create_paragraph(post=self.post)

    def test_sentence_create(self):
        """Test if SentenceSerializer creates record in the DB"""
        sentence = SentenceSerializer(data={"text": "serializer test create", "paragraph": self.paragraph.id})
        sentence.is_valid()
        instance = sentence.save()
        self.assertEqual(instance, Sentence.objects.get(pk=instance.id))

    def test_sentence_update(self):
        """Test if SentenceSerializer updates record in the DB"""
        new_text = "serializer test update new"
        sentence = SentenceSerializer(data={"text": "serializer test update", "paragraph": self.paragraph.id})
        sentence.is_valid()
        instance = sentence.save()
        new_sentence = SentenceSerializer(instance=instance, partial=True,
                                          data={"text": new_text})
        new_sentence.is_valid()
        new_sentence.save()
        self.assertEqual(Sentence.objects.get(pk=instance.id).text, new_text)

    @patch("posts.tasks.check_sentence_moderation", return_value=True)
    def test_post_create(self, mocked_check_sentence_moderation):
        """Test if PostSerializer creates record in the DB"""
        post = PostSerializer(
            data={
                "title": "Dummy title",
                "paragraphs": [
                    "This is the first paragraph. It contains two sentences.",
                    "This is the second paragraph. It contains two more sentences",
                    "Third paragraph here."
                ],
            }
        )
        post.is_valid()
        instance = post.save()
        mocked_check_sentence_moderation.assert_called()
        self.assertEqual(instance, Post.objects.get(pk=instance.id))

    def test_post_to_representation(self):
        data = PostSerializer(self.post).data
        paragraphs = list()
        for paragraph in self.post.paragraphs.all():
            paragraphs.append(
                ". ".join(paragraph.sentences.order_by("order").values_list("text", flat=True))
            )
        expected = {
            "id": self.post.id,
            "title": self.post.title,
            "paragraphs": [
                paragraphs
            ],
            "has_foul_language": self.post.has_foul_language,
            "moderation_check_status": self.post.moderation_check_status
        }
        self.assertDictEqual(data, expected)
