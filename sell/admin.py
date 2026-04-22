from django.contrib import admin
from .models import Variant

from .models import Brand, Device
from .models import SellRequest

admin.site.register(Brand)
admin.site.register(Device)
admin.site.register(Variant)
admin.site.register(SellRequest)