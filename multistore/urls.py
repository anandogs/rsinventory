from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('sale', views.sale, name='sale'),
    path('transfer', views.transfer, name='transfer'),
    path('returns', views.returns, name='returns'),
    path('transact', views.transact, name='transact'),
    path('download', views.download, name='download'),
    path('login', views.login_view, name='login'),
    path('upload_file', views.upload_file, name='upload_file'),
]