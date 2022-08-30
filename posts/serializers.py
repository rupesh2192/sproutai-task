import logging

from django.db import transaction
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from posts.constants import TASK_RETRY_DELAY
from posts.models import Sentence, Post
from posts.tasks import moderation_check_task

logger = logging.getLogger(__name__)


class SentenceSerializer(ModelSerializer):
    class Meta:
        model = Sentence
        fields = "__all__"


class PostSerializer(ModelSerializer):
    paragraphs = serializers.ListField(required=True)

    class Meta:
        model = Post
        fields = "__all__"

    def create(self, validated_data) -> Post:
        """
        Processes the Post related data and stores it into Post, Paragraph and Sentence models.
        Also runs moderation check for the newly added post.
        Returns:
            Post instance
        """
        # with transaction.atomic():
        paragraphs = validated_data.pop("paragraphs", [])
        post = super(PostSerializer, self).create(validated_data)

        for paragraph in paragraphs:
            paragraph_instance = post.paragraphs.create()
            sentence_order = 0
            for sentence in paragraph.split("."):
                if sentence:
                    sentence_serializer = SentenceSerializer(
                        data={"text": sentence.strip(), "paragraph": paragraph_instance.id, "order": sentence_order})
                    sentence_serializer.is_valid(raise_exception=True)
                    sentence_serializer.save()
                    sentence_order += 1
        try:
            moderation_check_task(post_id=post.id)
            post.refresh_from_db(fields=['has_foul_language'])
        except Exception as e:
            logger.exception(f"exception while checking moderation for post_id: {post.id}, queuing task")
            moderation_check_task.s(post_id=post.id).apply_async(countdown=TASK_RETRY_DELAY)
        return post

    def to_representation(self, instance):
        """
        Custom representation of the Post data for REST APIs.
        """
        paragraphs = list()
        for paragraph in instance.paragraphs.all():
            paragraphs.append(
                ". ".join(paragraph.sentences.order_by("order").values_list("text", flat=True))
            )
        return {
            "id": instance.id,
            "title": instance.title,
            "paragraphs": [
                paragraphs
            ],
            "has_foul_language": instance.has_foul_language,
            "moderation_check_status": instance.moderation_check_status,
        }
