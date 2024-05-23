from django.urls import path
from . import views
urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    path('create/', views.create_post, name="create_post"),
    path('edit/<slug:slug>/', views.post_edit,name='post_edit'),
    path('delete/<slug:slug>', views.delete_post, name='post_delete'),
    path('search/', views.search, name='search')
]
