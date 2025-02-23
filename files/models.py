import os
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone

def user_directory_path(instance, filename):
    """Uploads files to 'uploads/user_<id>/folder_<folder_id>/filename'"""
    folder_path = f'user_{instance.uploaded_by.id}/folder_{instance.folder.id}'
    return os.path.join('uploads', folder_path, filename)

class Folder(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    parent_folder = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subfolders')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class File(models.Model):
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE)
    file = models.FileField(upload_to=user_directory_path)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    uploaded_at = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name
