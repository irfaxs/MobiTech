from django.urls import path


from . views import(
homeView,
ServiceCreate,
ServiceUpdate,
ServiceDelete,
CarouselCreate,
CarouselUpdate,
CarouselDelete

)
from . import views


urlpatterns = [
    path ('', homeView, name = 'home_page'),
    path('service/add/', ServiceCreate.as_view(), name='service_create'),
   path('service/<int:pk>/edit/', ServiceUpdate.as_view(), name='service_update'),
   path('service/<int:pk>/delete/', ServiceDelete.as_view(), name='service_delete'),
   path('carousel/add/', CarouselCreate.as_view(), name='carousel_create'),
   path('carousel/<int:pk>/edit/', CarouselUpdate.as_view(), name='carousel_update'),
   path('carousel/<int:pk>/delete/', CarouselDelete.as_view(), name='carousel_delete'),
    
    
    
]