from django.urls import path

from . import views

from django.conf.urls.static import static
from django.conf import settings

app_name = 'testapp'

urlpatterns = [
    path('', views.index1, name='index1'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
