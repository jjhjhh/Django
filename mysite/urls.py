from django.contrib import admin
from django.urls import path
from searchkeyword import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),  # index 뷰와 연결
]