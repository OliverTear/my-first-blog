from django.urls import path 
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    # トップページ
    path('top/', views.top, name='top'), 
    # 本棚一覧
    path('list/', views.book_list, name='book_list'), 
    # 本棚追加
    path('add/', views.add_post, name='add_post'), 
    # 本棚詳細
    path('detail/<int:pk>/', views.book_detail, name='book_detail'),
    # 本の検索（ユーザーからはアクセスされない想定）
    path('serch/<str:key>/', views.book_serch, name='book_serch'),
    # 本棚の編集
    path('edit/<int:pk>/', views.bookshelf_update, name='book_update'),
    # 本棚の削除
    path('delete/<int:pk>/', views.delete_post, name='book_delete'),
]