from django.db import models
from django.contrib.auth.models import User, auth
# Create your models here.


# class FolderDirectory(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     directory = models.TextField()
#     file = models.FileField()
#     public_access = models.BooleanField(default=False)
#     created_on = models.DateTimeField(auto_now_add=True)
    
class Folder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    parent_folder = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    public_access = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "folder"
    
    
class MyFiles(models.Model):
    parent_folder = models.ForeignKey(Folder, on_delete=models.SET_NULL, null=True, blank=True)
    file = models.FileField( null=True, blank=True)    
    class Meta:
        db_table = "my_files"