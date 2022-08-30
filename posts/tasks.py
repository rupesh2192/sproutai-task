import logging
from concurrent.futures import ThreadPoolExecutor

from moderation_worker.celery import app
from posts.constants import TASK_RETRY_DELAY
from posts.exceptions import RetryError
from posts.models import Post, Sentence
from posts.services.moderation import ModerationService

logger = logging.getLogger(__name__)


@app.task()
def moderation_check_task(post_id: int):
    """
    Fetches Post using the given `post_id` and runs moderation check for all the sentences related to the Post.
    Queues the task for retry in case if the Moderation API fails.
    Args:
        post_id: The primary key of the Post instance.
    """
    post = Post.objects.get(id=post_id)
    try:
        with ThreadPoolExecutor(max_workers=5) as executor:
            results = executor.map(check_sentence_moderation,
                                   post.sentences.filter(has_foul_language=None).values_list("id", flat=True))
            for result in results:
                logger.info(f"{result}")
        post.update_foul_language()
        logger.info(f"moderation check successful for post_id: {post.id}")
    except RetryError as e:
        logger.warning(
            f"moderation service failed for post id {post.id}, queuing for retry in {TASK_RETRY_DELAY} seconds")
        moderation_check_task.s(post_id=post_id).apply_async(countdown=TASK_RETRY_DELAY)


def check_sentence_moderation(sentence_id: int):
    """
    Fetches the Sentence instance using the given `sentence_id` and runs moderation check on the text.
    Updates the `has_foul_language` column based on the value received in the response.
    Args:
        sentence_id: The primary key of the Sentence instance
    """
    sentence = Sentence.objects.get(id=sentence_id)
    sentence.has_foul_language = ModerationService().check_sentence(sentence.text)
    sentence.save()
    return True
