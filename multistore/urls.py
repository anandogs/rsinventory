from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('sale', views.sale, name='sale'),
    path('transfer', views.transfer, name='transfer'),
    path('returns', views.returns, name='returns'),
    path('download', views.download, name='download')
]