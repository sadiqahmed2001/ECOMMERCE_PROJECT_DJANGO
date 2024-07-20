"""
URL configuration for ecommerceproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from ecomapp import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('demo/',views.demo),
    path('index/',views.index),
    path('register/',views.register),
    path('ulogin/',views.ulogin),
    path('ulogout/',views.ulogout),
    path('store/',views.store),
    path('product_details/<pid>/',views.product_details),
    path('filterbycategory/<cid>/',views.filterbycategory),
    path('sortbyprice/<sp>',views.sortbyprice),
    path('filterbyprice/',views.filterbyprice),
    path('addtocart/<pid>/',views.addtocart),
    path('viewcart/',views.viewcart),
    path('removecart/<cid>/',views.removecart),
    path('updateqty/<x>/<cid>/',views.updateqty),
    path('placeorder/',views.placeorder),
    path('fetchorder/',views.fetchorder),
    path('makepayment/',views.makepayment),
    path('paymentsuccess/',views.paymentsuccess),
]

urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
