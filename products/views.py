from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Product
from django.db.models import Q
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.contrib.auth.mixins import UserPassesTestMixin


# 🔹 ALL PRODUCTS
class ProductList(ListView):
    template_name = 'products/product_list.html'
    model = Product
    context_object_name = 'products'


# 🔹 PRODUCT DETAIL
class ProductDetail(DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 🔥 ADD VARIANTS
        context['variants'] = self.object.variants.all()

        # 🔥 ADD EXTRA IMAGES (optional but useful)
        context['images'] = self.object.images.all()

        return context


# 🔹 LAPTOP PAGE
class LaptopList(ListView):
    template_name = 'products/laptop_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.filter(category='laptop')

class AccessoryList(ListView):
    template_name = 'products/accessory_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.filter(category='accessory')

class SearchResults(ListView):
    model = Product
    template_name = 'products/search_results.html'
    context_object_name = 'products'

    def get_queryset(self):
        query = self.request.GET.get('q')

        if query:
            return Product.objects.filter(
                Q(name__icontains=query) |
                Q(brand__icontains=query) |
                Q(category__icontains=query)
            )
        return Product.objects.none()





def live_search(request):
    query = request.GET.get('q')

    results = []

    if query:
        products = Product.objects.filter(name__icontains=query)[:5]

        for product in products:
            results.append({
                'id': product.id,
                'name': product.name,
                'price': product.price,
                'image': product.image.url
            })

    return JsonResponse(results, safe=False)


# 🔒 Only staff allowed
class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff


class ProductCreate(StaffRequiredMixin, CreateView):
    model = Product
    fields = '__all__'
    template_name = 'products/product_form.html'
    success_url = reverse_lazy('product_list')


class ProductUpdate(StaffRequiredMixin, UpdateView):
    model = Product
    fields = '__all__'
    template_name = 'products/product_form.html'
    success_url = reverse_lazy('product_list')


class ProductDelete(StaffRequiredMixin, DeleteView):
    model = Product
    template_name = 'products/product_confirm_delete.html'
    success_url = reverse_lazy('product_list')