from django.db import models

# Create your models here.
from shared.utils import BaseModel


class Post(BaseModel):
    """
    Database table to store Post related data.
    """
    title = models.CharField(max_length=255, null=False, blank=False)
    has_foul_language = models.BooleanField(default=None, null=True, blank=True, db_index=True)

    def update_foul_language(self):
        """
        Utility method to update the value of `Post.has_foul_language` column.
        Fetches all the sentences for the Post and updates `has_foul_language` to None if even 1 sentence exists with
         `has_foul_language = None`. else True/False depending on `Sentence.has_foul_language`.
        """
        qs = Sentence.objects.filter(paragraph__post=self)
        if qs.filter(has_foul_language=True).exists():
            self.has_foul_language = True
        elif qs.filter(has_foul_language=None).exists():
            self.has_foul_language = None
        else:
            self.has_foul_language = False
        self.save()

    @property
    def sentences(self):
        """
        Returns queryset of `Sentence` related to the Post.
        """
        return Sentence.objects.filter(paragraph__post=self).order_by("order")


class Paragraph(BaseModel):
    """
    Database table to store Paragraph -> Post mapping. A Post can have multiple Paragraphs.
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="paragraphs")


class Sentence(BaseModel):
    """
    Database table to store sentences related to a Paragraph. A Paragraph can have multiple `Sentences`.
    """
    paragraph = models.ForeignKey(Paragraph, on_delete=models.CASCADE, related_name="sentences")
    text = models.TextField()
    order = models.IntegerField(default=0)
    has_foul_language = models.BooleanField(default=None, null=True, blank=True, db_index=True)
