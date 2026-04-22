from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Brand, Device, Variant, SellRequest

from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import UserPassesTestMixin


# 🔹 SELECT BRAND
def select_brand(request):
    brands = Brand.objects.all()
    return render(request, 'sell/select_brand.html', {'brands': brands})


# 🔹 SELECT MODEL
def select_model(request, brand_name):
    brand = get_object_or_404(Brand, name__iexact=brand_name)
    devices = Device.objects.filter(brand=brand)

    return render(request, 'sell/select_model.html', {
        'brand': brand,
        'devices': devices
    })


# 🔹 DEVICE DETAIL
def device_detail(request, brand_name, device_name):
    brand = get_object_or_404(Brand, name__iexact=brand_name)
    device = get_object_or_404(Device, name__iexact=device_name, brand=brand)
    variants = device.variants.all()

    return render(request, 'sell/device_detail.html', {
        'device': device,
        'variants': variants
    })


# 🔹 QUESTIONS PAGE
def questions(request, brand_name, device_name):
    brand = get_object_or_404(Brand, name__iexact=brand_name)
    device = get_object_or_404(Device, name__iexact=device_name, brand=brand)

    variant_id = request.GET.get('variant_id')

    if not variant_id:
        return redirect('select_brand')

    variant = get_object_or_404(Variant, id=variant_id, device=device)

    return render(request, 'sell/questions.html', {
        'device': device,
        'variant': variant
    })


# 🔹 RESULT PAGE
def result(request, brand_name, device_name):
    brand = get_object_or_404(Brand, name__iexact=brand_name)
    device = get_object_or_404(Device, name__iexact=device_name, brand=brand)

    variant_id = request.GET.get('variant_id')
    price = request.GET.get('price')

    if not variant_id or not price:
        return redirect('select_brand')

    variant = get_object_or_404(Variant, id=variant_id, device=device)

    return render(request, 'sell/result.html', {
        'device': device,
        'variant': variant,
        'price': int(price)
    })


# 🔹 BOOKING PAGE (FIXED + SECURE)
@login_required
def booking(request, brand_name, device_name):
    brand = get_object_or_404(Brand, name__iexact=brand_name)
    device = get_object_or_404(Device, name__iexact=device_name, brand=brand)

    variant_id = request.GET.get('variant_id')
    price = request.GET.get('price')

    if not variant_id or not price:
        return redirect('select_brand')

    variant = get_object_or_404(Variant, id=variant_id, device=device)
    final_price = int(price)

    if request.method == "POST":
        SellRequest.objects.create(
            user=request.user,   # ✅ IMPORTANT
            device=device,
            variant=variant,
            price=final_price,
            name=request.POST.get('name'),
            phone=request.POST.get('phone'),
            address=request.POST.get('address')
        )

        return redirect('sell_success')

    return render(request, 'sell/booking.html', {
        'device': device,
        'variant': variant,
        'price': final_price
    })


# 🔹 SUCCESS PAGE
def sell_success(request):
    return render(request, 'sell/success.html')


# 🔹 STAFF MIXIN
class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff


# 🔹 DEVICE CRUD
class DeviceCreate(StaffRequiredMixin, CreateView):
    model = Device
    fields = '__all__'
    template_name = 'sell/device_form.html'
    success_url = reverse_lazy('select_brand')


class DeviceUpdate(StaffRequiredMixin, UpdateView):
    model = Device
    fields = '__all__'
    template_name = 'sell/device_form.html'
    success_url = reverse_lazy('select_brand')


class DeviceDelete(StaffRequiredMixin, DeleteView):
    model = Device
    template_name = 'sell/device_confirm_delete.html'
    success_url = reverse_lazy('select_brand')


# 🔥 BRAND CRUD (MUST EXIST FOR YOUR UI BUTTONS)
class BrandCreate(StaffRequiredMixin, CreateView):
    model = Brand
    fields = '__all__'
    template_name = 'sell/brand_form.html'
    success_url = reverse_lazy('select_brand')


class BrandUpdate(StaffRequiredMixin, UpdateView):
    model = Brand
    fields = '__all__'
    template_name = 'sell/brand_form.html'
    success_url = reverse_lazy('select_brand')


class BrandDelete(StaffRequiredMixin, DeleteView):
    model = Brand
    template_name = 'sell/brand_confirm_delete.html'
    success_url = reverse_lazy('select_brand')