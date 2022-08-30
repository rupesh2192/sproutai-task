# Create your views here.
from rest_framework import viewsets
from rest_framework.decorators import action

from posts.serializers import PostSerializer
from posts.tasks import moderation_check_task


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = PostSerializer.Meta.model.objects.all().prefetch_related('paragraphs', 'paragraphs__sentences')

    @action(methods=['GET'], detail=True)
    def check(self, request, *args, **kwargs):
        """
        Detail action endpoint to run an ad-hoc moderation check on a Post.
        """
        instance = self.get_object()
        moderation_check_task(post_id=instance.id)
        instance.refresh_from_db(fields=['has_foul_language'])
        return super(PostViewSet, self).retrieve(request, *args, **kwargs)
