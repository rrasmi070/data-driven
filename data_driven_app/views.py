import json
import os
from django.shortcuts import render
from django.views import generic
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth import logout
from django.db import connection
from data_driven.settings import BASE_DIR, MEDIA_ROOT
from data_driven_app.models import Folder, MyFiles
from data_driven_app.utils import check_dir, make_hierarchy
import pandas as pd
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
import subprocess
from itertools import chain
# Create your views here.


class Login(generic.View):
    def get(self, request, *args, **kwargs):
        
        
        return render(request,'login.html')
    
    def post(self, request, *args, **kwargs):
        print(request.POST)
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # user = User.objects.filter(username=email)
        # print(type(user))
        user = auth.authenticate(username=email, password=password)
        print(user)
        if user:
            auth.login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Login failed. Please check your credentials.')
            return render(request,'login.html')
            # if user is not None:
                # auth.login(request, user)
            
        
    
    
    
    
class Register(generic.View):
    def get(self, request, *args, **kwargs):
        return render(request,'register.html')
    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        user = f"SELECT * FROM auth_user WHERE email = {email}AND staff_status = {1};"
        try:
            with connection.cursor() as cursor:
                user = cursor.execute(user)
                user = user.fetchall()
        except:
            user = None

        if password !=confirm_password:
            messages.error(request, 'New password and confirm password must be same..')
            print(messages)
            return render(request,'register.html')
            
        if user:
            messages.error(request, 'User already exist.')
            print(messages)
            return render(request,'register.html')
        else:
            User.objects.create_user(username=email,first_name=first_name, email=email,last_name=last_name, password=password)
            return render(request,'login.html')



class Dashboard(generic.View):
    def get(self, request, *args, **kwargs):
        
        query = f"SELECT id,user_id, name, parent_folder_id FROM folder WHERE user_id = {request.user.id};"
        
        # try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            row = cursor.fetchall()
            df = pd.DataFrame(row, columns=['id','user', 'name','parent_folder'])
            print(row, "========>")
            df = pd.DataFrame(row, columns=['id','user', 'name','parent_folder'])
            id_li = list(set(df['id'].tolist()))
            print(id_li,"===========lllllkkk")
            img_query = MyFiles.objects.filter(parent_folder__in = id_li )
            img_df = pd.DataFrame(img_query.values())
            if img_query:
                img_df['file_url'] = img_df['file'].apply(lambda x :f"{request.scheme}://" +f"{request.get_host()}/media/{x}")
                print(img_df, "=====>===>",request.scheme)
                    # print(df)
                    
        
        val = make_hierarchy(df ,img_df)
        # val = make_hierarchy(df)
                
                    # print(df)
        # except:
        #     user = None
        print(val)
        val = json.dumps(val)
        val = json.loads(val)
        return render(request,'dashboard.html', {'user': val})
    


def userLogout(request):
    print("Logout Success")
    logout(request)
    return redirect('login')
    
class ShowFolder(generic.View):
    def get(self, request, pk,*args, **kwargs):
        print(pk,"=======lll")
        query = f"SELECT id,user_id, name, parent_folder_id FROM folder WHERE user_id = {request.user.id} AND parent_folder_id = {pk};"
        # try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            row = cursor.fetchall()
            print(row, "========>")
            df = pd.DataFrame(row, columns=['id','user', 'name','parent_folder'])
            id_li = list(set(df['id'].tolist()))
            print(id_li,"===========lllllkkk")
        img_query = MyFiles.objects.filter(parent_folder__in = id_li )
        img_df = pd.DataFrame(img_query.values())
        if img_query:
            img_df['file_url'] = img_df['file'].apply(lambda x :f"{request.scheme}://" +f"{request.get_host()}/media/{x}")
            print(img_df, "=====>===>",request.scheme)
            print(img_df, "========>")
                    # print(df)
                    
        
        val = make_hierarchy(df ,img_df)
        # except:
        #     user = None
        print(val)
        val = json.dumps(val)
        val = json.loads(val)
        return render(request,'file_folder.html', {'user': val,'files':[]})
    
    
class FolderMgt(generic.View):
    def get(self, request, *args, **kwargs):
        # User.objects.filter(user=request
        return render(request,'dashboard.html')
        
    
    
    def post(self, request, *args, **kwargs):
        folder_name = request.POST.get('name')
        folderid = request.POST.get('folderid').strip()
        print(type(''),"------------------999")
        if (folderid == '') or (not int(folderid)):
            dir_li = os.listdir(MEDIA_ROOT)
            res = check_dir(dir_li, folder_name)
            print(folderid,"==================")
            if not res:
                path = f"{MEDIA_ROOT}/{request.user.id}"
                try:
                    mode = 0o777
                    os.mkdir(path,mode)
                    os.mkdir(f"{path}/{folder_name}",mode)
                except:
                    os.mkdir(f"{path}/{folder_name}",mode)
                folder = Folder()
                folder.name = folder_name
                folder.user_id = request.user.id
                # folder.parent_folder_id = 0
                folder.save()
                return redirect('dashboard')
                
            else:
                messages.error(request, 'Directory already exist.')
                return redirect('dashboard')
        else:
            print(type(folderid),"-----kkkk")
            path = f"{MEDIA_ROOT}/{request.user.id}"
                
            mode = 0o777
            try:
                os.mkdir(path,mode)
            except:
                
                query = f"SELECT name FROM folder WHERE parent_folder_id < {folderid} and user_id = {request.user.id};"
                query_1st = f"SELECT name FROM folder WHERE user_id = {request.user.id};"
                with connection.cursor() as cursor:
                    cursor.execute(query_1st)
                    row1 = cursor.fetchall()
                with connection.cursor() as cursor:
                    cursor.execute(query)
                    row = cursor.fetchall()
                    path_nest = [i[0]for i in row]
                    paths = path_nest if path_nest else row1[0]
                print(path_nest,"=======folderid",row)
                print(f"{path}/{'/'.join(paths)}/", "========>",paths)
                os.mkdir(f"{path}/{'/'.join(paths)}/{folder_name}",mode)
                # print(a=9)
                folder = Folder()
                folder.name = folder_name
                folder.parent_folder_id =  0 if folderid == 0 else folderid
                folder.user_id = request.user.id
                # folder.parent_folder_id = folderid
                folder.save()
            
        return redirect('dashboard')

class FileUpload(generic.View):
    
    def post(self, request, *args, **kwargs):
        yourfile = request.POST.get('yourfile')
        folderid = request.FILES.getlist('folderid')
        print(yourfile,"=====", folderid )
        return redirect('dashboard')
    
@csrf_exempt
def upload_file(request):
    if request.method == 'POST':
        yourfile = request.FILES.getlist('yourfile')
        folderid = request.POST.get('folderid')
        print(yourfile,"====>=>>", folderid )
        res = Folder.objects.filter(id__gte = folderid).values_list('id', flat=True)
        for img in yourfile:
            print(img,"=====", folderid)
            imgs = MyFiles()
            imgs.parent_folder_id = res[0]
            imgs.file = img
            imgs.save()
            
        return redirect('dashboard')


@csrf_exempt
def update_file(request):
    if request.method == 'POST':
        update_file = request.FILES.getlist('update_file')
        pid = request.POST.get('pid')
        old_file = request.POST.get('old_file')
        file_obj = MyFiles.objects.filter(id=pid).last()
        print(pid)
        os.remove(f"{MEDIA_ROOT}/{file_obj.file}")
        file_obj.file=update_file[0]
        file_obj.save()
        
            
    return redirect('dashboard')


@csrf_exempt
def delete_file(request, pk):
    id = request.GET.get('pk')
    file_obj = MyFiles.objects.filter(id=pk)
    os.remove(f"{MEDIA_ROOT}/{file_obj.last().file}")
    file_obj.delete()
    print(pk,"==============================pk============")
        
            
    return redirect('dashboard')