from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from reviews.models import Review, Title
from .serializers import ReviewSerializer, CommentSerializer
from .permissions import IsAuthorModeratorAdminOrReadOnly

# ЗАМЕТКА ДЛЯ РАЗРАБОТЧИКА №2 (Titles):
# В твоем TitleSerializer обязательно добавь поле 'rating'.
# ТЗ требует среднюю оценку. Сделай это через:
# queryset = Title.objects.annotate(rating=Avg('reviews__score'))
# .order_by('name')


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorModeratorAdminOrReadOnly,)

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorModeratorAdminOrReadOnly,)

    def get_review(self):
        return get_object_or_404(
            Review,
            pk=self.kwargs.get('review_id'),
            title_id=self.kwargs.get('title_id')
        )

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())
