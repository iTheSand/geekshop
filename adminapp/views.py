from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from adminapp.forms import ShopUserAdminEditForm, ProductEditForm, ProductCategoryEditForm
from authapp.forms import ShopUserRegisterForm
from authapp.models import ShopUser
from mainapp.models import ProductCategory, Product


# @user_passes_test(lambda u: u.is_superuser)
# def user_create(request):
#     title = 'пользователи/создание'
#
#     if request.method == 'POST':
#         user_form = ShopUserRegisterForm(request.POST, request.FILES)
#         if user_form.is_valid():
#             user_form.save()
#             return HttpResponseRedirect(reverse('admin:user_read'))
#     else:
#         user_form = ShopUserRegisterForm()
#     content = {
#         'title': title,
#         'form': user_form
#     }
#     return render(request, 'adminapp/user_update.html', content)


# переписываем user_create
class UserCreateView(CreateView):
    model = ShopUser
    template_name = 'adminapp/user_update.html'
    success_url = reverse_lazy('admin:user_read')
    form_class = ShopUserRegisterForm

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


# @user_passes_test(lambda u: u.is_superuser)
# def users(request):
#     title = 'админка/пользователи'
#
#     users_list = ShopUser.objects.all().order_by('-is_active', '-is_superuser', '-is_staff', 'username')
#
#     content = {
#         'title': title,
#         'objects': users_list
#     }
#     return render(request, 'adminapp/users.html', content)

# переписываем users
class UserListView(ListView):
    model = ShopUser
    template_name = 'adminapp/users.html'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


# @user_passes_test(lambda u: u.is_superuser)
# def user_update(request, pk):
#     title = 'пользователи/редактирование'
#
#     edit_user = get_object_or_404(ShopUser, pk=pk)
#     if request.method == 'POST':
#         user_form = ShopUserAdminEditForm(request.POST, request.FILES, instance=edit_user)
#         if user_form.is_valid():
#             user_form.save()
#             return HttpResponseRedirect(reverse('admin:user_read'))
#     else:
#         user_form = ShopUserAdminEditForm(instance=edit_user)
#
#     content = {
#         'title': title,
#         'form': user_form
#     }
#     return render(request, 'adminapp/user_update.html', content)


# переписываем user_update
class UserUpdateView(UpdateView):
    model = ShopUser
    template_name = 'adminapp/user_update.html'
    success_url = reverse_lazy('admin:user_read')
    form_class = ShopUserAdminEditForm

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


# @user_passes_test(lambda u: u.is_superuser)
# def user_delete(request, pk):
#     title = 'пользователи/удаление'
#
#     user_item = get_object_or_404(ShopUser, pk=pk)
#     if request.method == 'POST':
#         if user_item.is_active:
#             user_item.is_active = False
#         else:
#             user_item.is_active = True
#         user_item.save()
#         return HttpResponseRedirect(reverse('admin:user_read'))
#
#     content = {
#         'title': title,
#         'user_to_delete': user_item
#     }
#     return render(request, 'adminapp/user_delete.html', content)


# переписываем user_delete
class UserDeleteView(DeleteView):
    model = ShopUser
    template_name = 'adminapp/user_delete.html'
    success_url = reverse_lazy('admin:user_read')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.is_active:
            self.object.is_active = False
        else:
            self.object.is_active = True
        self.object.save()
        return HttpResponseRedirect(self.success_url)

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


# @user_passes_test(lambda u: u.is_superuser)
# def category_create(request):
#     title = 'категории/создание'
#
#     if request.method == 'POST':
#         category_form = ProductCategoryEditForm(request.POST, request.FILES)
#         if category_form.is_valid():
#             category_form.save()
#             return HttpResponseRedirect(reverse('admin:category_read'))
#     else:
#         category_form = ProductCategoryEditForm()
#     content = {
#         'title': title,
#         'form': category_form
#     }
#     return render(request, 'adminapp/category_update.html', content)


# переписываем category_create
class ProductCategoryCreateView(CreateView):
    model = ProductCategory
    template_name = 'adminapp/category_update.html'
    success_url = reverse_lazy('adminapp:category_read')
    form_class = ProductCategoryEditForm

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


# @user_passes_test(lambda u: u.is_superuser)
# def categories(request):
#     title = 'админка/категории'
#
#     categories_list = ProductCategory.objects.all().order_by('-is_active')
#
#     content = {
#         'title': title,
#         'objects': categories_list
#     }
#     return render(request, 'adminapp/categories.html', content)


# переписываем categories
class ProductCategoryListView(ListView):
    model = ProductCategory
    template_name = 'adminapp/categories.html'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


# @user_passes_test(lambda u: u.is_superuser)
# def category_update(request, pk):
#     title = 'категории/редактирование'
#
#     edit_category = get_object_or_404(ProductCategory, pk=pk)
#     if request.method == 'POST':
#         update_form = ProductCategoryEditForm(request.POST, request.FILES, instance=edit_category)
#         if update_form.is_valid():
#             update_form.save()
#             return HttpResponseRedirect(reverse('admin:category_read'))
#     else:
#         update_form = ProductCategoryEditForm(instance=edit_category)
#
#     content = {
#         'title': title,
#         'form': update_form,
#     }
#
#     return render(request, 'adminapp/category_update.html', content)


# переписываем category_update
class ProductCategoryUpdateView(UpdateView):
    model = ProductCategory
    template_name = 'adminapp/category_update.html'
    success_url = reverse_lazy('adminapp:category_read')
    form_class = ProductCategoryEditForm

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


# @user_passes_test(lambda u: u.is_superuser)
# def category_delete(request, pk):
#     title = 'категории/удаление'
#
#     category_item = get_object_or_404(ProductCategory, pk=pk)
#     if request.method == 'POST':
#         if category_item.is_active:
#             category_item.is_active = False
#         else:
#             category_item.is_active = True
#         category_item.save()
#         return HttpResponseRedirect(reverse('admin:category_read'))
#
#     content = {
#         'title': title,
#         'category_delete': category_item
#     }
#     return render(request, 'adminapp/category_delete.html', content)


# переписываем category_delete
class ProductCategoryDeleteView(DeleteView):
    model = ProductCategory
    template_name = 'adminapp/category_delete.html'
    success_url = reverse_lazy('adminapp:category_read')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.is_active:
            self.object.is_active = False
        else:
            self.object.is_active = True
        self.object.save()
        return HttpResponseRedirect(self.success_url)

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


# @user_passes_test(lambda u: u.is_superuser)
# def product_create(request, pk):
#     category_item = get_object_or_404(ProductCategory, pk=pk)
#     if request.method == 'POST':
#         product_form = ProductEditForm(request.POST, request.FILES)
#         if product_form.is_valid():
#             product_form.save()
#             return HttpResponseRedirect(reverse('admin:products', args=[pk]))
#     else:
#         product_form = ProductEditForm()
#
#     content = {
#         'form': product_form,
#         'category': category_item
#     }
#     return render(request, 'adminapp/product_update.html', content)


# переписываем product_create
class ProductCreateView(CreateView):
    model = Product
    form_class = ProductEditForm
    template_name = 'adminapp/product_update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = get_object_or_404(ProductCategory, pk=self.kwargs['pk'])
        context['category'] = category
        return context

    def get_success_url(self):
        return reverse('admin:products', args=[self.kwargs['pk']])

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


# @user_passes_test(lambda u: u.is_superuser)
# def products(request, pk):
#     title = 'админка/пользователи'
#
#     category_item = get_object_or_404(ProductCategory, pk=pk)
#
#     products_list = Product.objects.filter(category__pk=pk).order_by('name')
#
#     content = {
#         'title': title,
#         'category': category_item,
#         'objects': products_list
#     }
#     return render(request, 'adminapp/products.html', content)


# переписываем products
class ProductListView(ListView):
    model = Product
    template_name = 'adminapp/products.html'
    paginate_by = 2

    def get_queryset(self):
        category_pk = self.kwargs['pk']
        return Product.objects.filter(category__pk=category_pk).order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = get_object_or_404(ProductCategory, pk=self.kwargs['pk'])
        context['category'] = category
        return context

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


# @user_passes_test(lambda u: u.is_superuser)
# def product_read(request, pk):
#     product_item = get_object_or_404(Product, pk=pk)
#     content = {
#         'object': product_item
#     }
#     return render(request, 'adminapp/product_detail.html', content)


# переписываем product_read
class ProductDetailView(DeleteView):
    model = Product
    template_name = 'adminapp/product_detail.html'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


# @user_passes_test(lambda u: u.is_superuser)
# def product_update(request, pk):
#     product_item = get_object_or_404(Product, pk=pk)
#     if request.method == 'POST':
#         product_form = ProductEditForm(request.POST, request.FILES, instance=product_item)
#         if product_form.is_valid():
#             product_form.save()
#             return HttpResponseRedirect(reverse('adminapp:products', args=[product_item.category_id]))
#     else:
#         product_form = ProductEditForm(instance=product_item)
#
#     content = {
#         'form': product_form,
#         'category': product_item.category
#     }
#
#     return render(request, 'adminapp/product_update.html', content)


# переписываем product_update
class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductEditForm
    template_name = 'adminapp/product_update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.object = self.get_object()
        category = get_object_or_404(Product, pk=self.kwargs['pk'])
        context['category'] = category
        return context

    def get_success_url(self):
        self.object = self.get_object()
        return reverse('adminapp:products', args=[self.object.category.pk])

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


# @user_passes_test(lambda u: u.is_superuser)
# def product_delete(request, pk):
#     product_item = get_object_or_404(Product, pk=pk)
#
#     if request.method == 'POST':
#         if product_item.is_active:
#             product_item.is_active = False
#         else:
#             product_item.is_active = True
#         product_item.save()
#         return HttpResponseRedirect(reverse('admin:products', args=[product_item.category.pk]))
#
#     content = {
#         'product_to_delete': product_item
#     }
#     return render(request, 'adminapp/product_delete.html', content)

# переписываем product_delete
class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'adminapp/product_delete.html'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.is_active:
            self.object.is_active = False
        else:
            self.object.is_active = True
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        self.object = self.get_object()
        return reverse('adminapp:products', args=[self.object.category.pk])

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
