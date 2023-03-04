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
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer

    
    def get_queryset(self):

        if self.request.user.is_anonymous:
            return self.queryset.exclude(status='DRAFT')
        
        if self.action == 'favourites':
            if self.request.user.is_anonymous:
                return Advertisement.objects.none()
            return self.request.user.favourites.all()
        
        if self.request.user.is_authenticated:
            if self.request.user.is_staff:
                return self.queryset
            queryset1 = self.queryset.exclude(status='DRAFT')
            queryset2 = Advertisement.objects.all().filter(creator=self.request.user, status='DRAFT')
            return queryset1 | queryset2
        
        return super().get_queryset()
    
    @action(methods=['get'], detail=False)
    def favourites(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    @action(methods=['post'], detail=True, url_path='mark-as-favourite')
    def mark_as_favourite(self, request, *args, **kwargs):
        obj = self.get_object()
        if self.request.user == obj.creator:
            return response({'status':'FAIL'})
        self.request.user.favourites.add(obj)
        return response({'status':'OK'})

    filterset_fields = ['creator',]

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = AdvertisementFilter
    
    def perform_create (self, serializer):
        # serializer.save
        serializer.save(creator=self.request.user)
    
    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ["create"]:
            return [IsAuthenticated()]
        elif self.action in ["update", "partial_update", "destroy"]:
            return [IsAuthenticated(), IsOwnerOrReadOnly()]
        return []