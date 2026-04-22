from django.shortcuts import render
from .models import CarouselImage, Service
from sell.models import Device   
from products.models import Product
from django.urls import reverse_lazy
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import CreateView, UpdateView, DeleteView


def homeView(request):
    template = 'mainapp/home.html'

    context = {
        'carousel_images': CarouselImage.objects.filter(is_active=True),

        # ✅ Phones
        'products': Product.objects.filter(category='phone')[:8],

        # ✅ Laptops
        'laptops': Product.objects.filter(category='laptop')[:4],

        'services': Service.objects.all(), 
    }

    return render(request, template, context)


def aboutView(request):
    template = 'mainapp/about.html'
    context = {}

    return render(
        request=request,
        template_name=template,
        context=context
    )

class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff


class ServiceCreate(StaffRequiredMixin, CreateView):
    model = Service
    fields = '__all__'
    template_name = 'mainapp/service_form.html'
    success_url = reverse_lazy('home_page')


class ServiceUpdate(StaffRequiredMixin, UpdateView):
    model = Service
    fields = '__all__'
    template_name = 'mainapp/service_form.html'
    success_url = reverse_lazy('home_page')


class ServiceDelete(StaffRequiredMixin, DeleteView):
    model = Service
    template_name = 'mainapp/service_confirm_delete.html'
    success_url = reverse_lazy('home_page')


class CarouselCreate(StaffRequiredMixin, CreateView):
    model = CarouselImage
    fields = '__all__'
    template_name = 'mainapp/carousel_form.html'
    success_url = reverse_lazy('home_page')


class CarouselUpdate(StaffRequiredMixin, UpdateView):
    model = CarouselImage
    fields = '__all__'
    template_name = 'mainapp/carousel_form.html'
    success_url = reverse_lazy('home_page')


class CarouselDelete(StaffRequiredMixin, DeleteView):
    model = CarouselImage
    template_name = 'mainapp/carousel_confirm_delete.html'
    success_url = reverse_lazy('home_page')