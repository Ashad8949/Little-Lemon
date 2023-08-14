from django.urls import path
from . import views

app_name = 'voiceorder'

urlpatterns = [
    path('', views.root, name='root'),
    path('get_topping', views.get_topping, name='get_topping'),
    path('get_topping_redirect', views.get_topping_redirect, name='get_topping_redirect'),
    path('get_order', views.get_order, name='get_order'),
    path('get_topping_upload_wav', views.get_topping_upload_wav, name='get_topping_upload_wav'),
    path('get_topping_record_wav', views.get_topping_record_wav, name='get_topping_record_wav'),
    path('play_local_wav', views.play_local_wav, name='play_local_wav'),
]
