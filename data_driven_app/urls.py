from django.urls import path
from . import views

urlpatterns = [
    path('', views.Login.as_view(), name='login'),
    path('register', views.Register.as_view(), name='register'),
    path('dashboard', views.Dashboard.as_view(), name='dashboard'),
    path('logout/', views.userLogout, name= 'logout'),
    path('mgt_folder', views.FolderMgt.as_view(), name= 'mgt_folder'),
    path('show_folder/<int:pk>', views.ShowFolder.as_view(), name= 'show_folder'),
    path('file_upload/', views.upload_file, name='file_upload'),
    path('file_update/', views.update_file, name='file_update'),
    path('file_delete/<int:pk>', views.delete_file, name='file_update'),
    # path('folder/<int:pk>/', views.FolderDetailView.as_view(), name='folder-detail'),
    # path('folder/<int:pk>/update/', views.FolderUpdateView.as_view(), name='folder-update'),
    # path('folder/<int:pk>/delete/', views.FolderDeleteView.as_view(), name='folder-delete'),
    # path('file/upload/', views.FileCreateView.as_view(), name='file-upload'),
    # path('file/<int:pk>/', views.FileDetailView.as_view(), name='file-detail'),
    # path('file/<int:pk>/delete/', views.FileDeleteView.as_view(), name='file-delete'),
]