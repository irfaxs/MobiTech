from django.contrib import admin
from .models import Service

from .models import CarouselImage
# Register your models here.
admin.site.register(CarouselImage)


admin.site.register(Service)