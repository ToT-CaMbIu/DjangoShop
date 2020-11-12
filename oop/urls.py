"""oop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
from polls.views import (
    index,
    category_view,
    product_view,
    cart_view,
    cart_adding_view,
    cart_deleting_view,
    registration_view,
    search_view,
    loging_view,
    coupon_usage_view,
    order_create_view,
    make_order_view,
    account_view,
    payment_success_view,
    payment_failure_view
)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index,name = 'base'),
    url(r'search_by_title/$', search_view, name='search_by_title'),
    url(r'coupon_usage/$', coupon_usage_view, name='coupon_usage'),
    url(r'^category/(?P<category_slug>[-\w]+)/$', category_view, name='category_detail'),
    url(r'^product/(?P<product_slug>[-\w]+)/$', product_view, name='product_detail'),
    url(r'^cart_adding/(?P<product_slug>[-\w]+)/$', cart_adding_view, name='cart_adding'),
    url(r'^cart_deleting/(?P<product_slug>[-\w]+)/$', cart_deleting_view, name='cart_deleting'),
    url(r'^cart/$', cart_view, name='cart'),
    url(r'^registration/$', registration_view, name='registration'),
    url(r'^loging/$', loging_view, name='loging'),
    url(r'^logout/$', LogoutView.as_view(next_page=reverse_lazy('base')), name='logout'),
    url(r'^order/$', order_create_view, name='create_order'),
    url(r'^make_order/$', make_order_view, name='make_order'),
    url(r'^account/$', account_view, name='account'),
    url(r'^make_order/payment_success/(?P<order_id>[-\w]+)/$', payment_success_view, name='payment_success'),
    url(r'^make_order/payment_failure/(?P<order_id>[-\w]+)/$', payment_failure_view, name='payment_failure'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)