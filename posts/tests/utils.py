from posts.models import Post, Paragraph, Sentence
from posts.tests import fake


def create_post(title="Test Post title"):
    return Post.objects.create(title=title)


def create_paragraph(post):
    return Paragraph.objects.create(post=post)


def create_sentences(paragraph: Paragraph, sentences: list = list(), count: int = 5, has_foul_language: bool = False):
    sentence_objects = list()
    if sentences:
        for sentence in sentences:
            sentence_objects.append(Sentence(text=sentence, paragraph=paragraph))
    else:
        for _ in range(count):
            sentence_objects.append(
                Sentence(text=fake.sentence(nb_words=10), paragraph=paragraph, has_foul_language=has_foul_language))
    Sentence.objects.bulk_create(sentence_objects)
    return sentence_objects
