from django.contrib import admin
from django.urls import path, include
from biblioteca.views import adicionar_livro

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', adicionar_livro)
]

