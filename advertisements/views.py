from urllib import response
from rest_framework.permissions import IsAuthenticated
from advertisements.permissions import IsOwnerOrReadOnly
from rest_framework.viewsets import ModelViewSet
from advertisements.models import Advertisement
from advertisements.serializers import AdvertisementSerializer

from advertisements.filters import AdvertisementFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from rest_framework.decorators import action


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""
    queryset = Advertisement.objects.all().exclude(status='DRAFT')
    serializer_class = AdvertisementSerializer
    # permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    
    def get_queryset(self):
        if self.action == 'favourites':
            if self.request.user.is_anonymous:
                return Advertisement.objects.none()
            return self.request.user.favourites.all()
        if self.request.user.is_authenticated:
            return Advertisement.objects.all().filter(creator=self.request.user.is_authenticated)
        return super().get_queryset()
    #     current_user = self.request.user
    #     current_user_authorization = self.request.user.is_authenticated
        
    #     if current_user_authorization == 'True':
    #         return Advertisement.objects.all().filter(creator=current_user)
    #     return Advertisement.objects.all().exclude(status='DRAFT')

    @action(methods=['get'], detail=False)
    def favourites(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    @action(methods=['post'], detail=True, url_path='mark-as-favourite')
    def mark_as_favourite(self, request, *args, **kwargs):
        obj = self.get_object()
        if self.request.user == obj.author:
            return response({'status':'FAIL'})
        self.request.user.favourites.add(obj)
        return response({'status':'OK'})

    filterset_fields = ['creator',]

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = AdvertisementFilter
    
    def perform_create (self, serializer):
        # serializer.save
        serializer.save(creator=self.request.user)
    
    # TODO: настройте ViewSet, укажите атрибуты для кверисета,
    #   сериализаторов и фильтров

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ["create"]:
            return [IsAuthenticated()]
        elif self.action in ["update", "partial_update", "destroy"]:
            # return [IsAuthenticated()]
            return [IsAuthenticated(), IsOwnerOrReadOnly()]
        return []