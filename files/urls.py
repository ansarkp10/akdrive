from django.contrib.auth import views as auth_views
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("logout/", views.user_logout, name="logout"),
    path('upload/', views.upload_file, name='upload_file'),
    path('create_folder/', views.create_folder, name='create_folder'),
    path('folder/<int:folder_id>/', views.folder_detail, name='folder_detail'),
    path('delete_file/<int:file_id>/', views.delete_file, name='delete_file'),
    path('rename_folder/<int:folder_id>/', views.rename_folder, name='rename_folder'),
    path('delete_folder/<int:folder_id>/', views.delete_folder, name='delete_folder'),

    # Fix for missing accounts/login/ URL
    path('login/', views.user_login, name='login'),
    path('signup/', views.signup, name='signup'),
]

# Serve static files during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)