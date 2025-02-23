from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
import json
import os

from .models import File, Folder
from .forms import SignupForm, FileUploadForm

def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            return redirect('dashboard')  # Ensure this URL name exists
    else:
        form = SignupForm()
    return render(request, "auth/signup.html", {"form": form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')  # Ensure this URL name exists
    else:
        form = AuthenticationForm()
    return render(request, 'auth/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    folders = Folder.objects.filter(owner=request.user, parent_folder__isnull=True)  # Only show root folders
    files = File.objects.filter(uploaded_by=request.user)
    return render(request, 'files/dashboard.html', {'folders': folders, 'files': files})


@login_required
def folder_detail(request, folder_id):
    folder = get_object_or_404(Folder, id=folder_id, owner=request.user)
    files = File.objects.filter(folder=folder)

    for file in files:
        file.filename = os.path.basename(file.file.name)

    return render(request, 'files/folder_detail.html', {'folder': folder, 'files': files})


from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from .forms import FileUploadForm
from .models import File

@csrf_exempt
@login_required
def upload_file(request):
    if request.method == 'POST':
        files = request.FILES.getlist('files') 
        folder_id = request.POST.get('folder')  

        if files:
            for file in files:
                file_instance = File(file=file, uploaded_by=request.user, folder_id=folder_id)
                file_instance.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': 'No files uploaded.'})

    form = FileUploadForm(user=request.user)
    return render(request, 'files/upload_file.html', {'form': form})
@csrf_protect
@login_required
def create_folder(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            folder_name = data.get("name")
            parent_folder_id = data.get("parent_folder")
            parent_folder = None

            if parent_folder_id:
                parent_folder = get_object_or_404(Folder, id=parent_folder_id, owner=request.user)

            if folder_name:
                new_folder = Folder.objects.create(name=folder_name, owner=request.user, parent_folder=parent_folder)
                return JsonResponse({"success": True, "folder_id": new_folder.id})
            return JsonResponse({"success": False, "error": "Folder name required"})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})
    
    return JsonResponse({"success": False, "error": "Invalid request method"})


@login_required
def delete_file(request, file_id):
    if request.method == "DELETE":
        file = get_object_or_404(File, id=file_id, uploaded_by=request.user)
        file.delete()
        return JsonResponse({"success": True})
    
    return JsonResponse({"success": False, "error": "Invalid request method"}, status=400)

@csrf_exempt
@login_required
def rename_folder(request, folder_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            new_name = data.get('name')
            folder = get_object_or_404(Folder, id=folder_id, owner=request.user)
            folder.name = new_name
            folder.save()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@csrf_exempt
@login_required
def delete_folder(request, folder_id):
    if request.method == 'DELETE':
        try:
            folder = get_object_or_404(Folder, id=folder_id, owner=request.user)
            folder.delete()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})
