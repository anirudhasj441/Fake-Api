from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from django.contrib.auth.models import User
from .models import Client, Project, UserExtend
import json

# Create your views here.

def index(request):
    return render(request,'app/index.html')

@csrf_exempt
def clients(request):
    if request.method == 'GET':
        if request.GET.get("id"):
            data = []
            client = Client.objects.get(pk = request.GET.get("id"))
            projects = Project.objects.filter(client = client)
            for project in projects:
                project_data = {
                    "id" : project.pk,
                    "name" : project.project_name
                }
                data.append(project_data)
            client_data = {
                "id" : client.pk,
                "client_name" : client.client_name,
                "projects" : data
            }
            return JsonResponse(client_data)
        else:
            data = []
            clients = Client.objects.all()
            for client in clients:
                client_data = {}
                client_data['id'] = client.pk
                client_data['client_name'] = client.client_name
                client_data['created_at'] = str(client.created_at)
                client_data['creatde_by'] = client.created_by.username
                data.append(client_data)
            return JsonResponse(data, safe=False)
    elif request.method == 'POST':
        if request.user.is_authenticated:
            data = json.loads(request.body)
            print(data['client_name'])
            client = Client.objects.create(
                client_name = data['client_name'],
                created_by = request.user
            )
            client_data = {
                "id" : client.pk,
                "client_name" : client.client_name,
                "created_at" : str(client.created_at),
                "created_by" : client.created_by.username
            }
            return JsonResponse(client_data)        
        else:
            return JsonResponse({"payload" : "User Not Login"})
    elif request.method == "PUT" or request.method == "PATCH":
        if request.GET.get("id"):
            if request.user.is_authenticated:
                data = json.loads(request.body)
                client = Client.objects.get(pk = request.GET.get("id"))
                client.client_name = data["client_name"]
                client.save()
                data = {
                    "id" : client.pk,
                    "client_name" : client.client_name,
                    "created_at" : str(client.created_at),
                    "created_by" : client.created_by.username,
                    "updated_at" : str(timezone.now())
                }
                return JsonResponse(data)
            else:
                return JsonResponse({"warning" : "User Not Log in "})
        else:
            return JsonResponse({"warning" : "id not specified"})
    elif request.method == "DELETE":
        if request.GET.get("id"):
            if request.user.is_authenticated:
                client = Client.objects.filter(pk=request.GET.get("id")).first()
                if client:
                    client.delete()
                    return JsonResponse({},status=204)
                else:
                    return JsonResponse({"Warning" : "Client not present"})
            else:
                return JsonResponse({"Warning" : "User Not Loged in"})
        else:
            return JsonResponse({"Error" : "id not specified"})

@csrf_exempt
def projects(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            data = []
            projects = Project.objects.filter(users=request.user)
            if projects:
                for project in projects:
                    project_data = {
                        "id" : project.pk,
                        "project_name" : project.project_name,
                        "created_at" : str(project.created_at),
                        "created_by" : project.created_by.user.username
                    }
                    data.append(project_data)
                return JsonResponse(data, safe=False)
            else:
                return JsonResponse({"Message" : "No Projects Assigned"})
        else:
            return JsonResponse({"warning" : "User Not Logged In"})
    elif request.method == "POST":
        if request.GET.get("id"):
            if request.user.is_authenticated:
                data = json.loads(request.body)
                users = []
                client = Client.objects.get(pk = request.GET.get("id"))
                users_data = data["users"]
                user_extended = UserExtend.objects.filter(user = request.user.pk).first()
                if not user_extended:
                    user_extended = UserExtend.objects.create(
                        user = request.user
                    )
                project = Project.objects.create(
                    project_name = data["project_name"],
                    client = client,
                    created_by = user_extended
                )
                for user_data in users_data:
                    user = User.objects.filter(pk = user_data["id"], username= user_data["name"]).first()
                    if not user:
                        return JsonResponse({"Error" : str(user_data["id"])+"-"+user_data["name"]+"User Not Found"})
                    else:
                        project.users.add(user)
                        print(user_extended,"hello")
                for user in project.users.all():
                    user_data = {
                        "id" : user.pk,
                        "name" : user.username
                    }
                    users.append(user_data)
                data = {
                    "id" : project.pk,
                    "project_name" : project.project_name,
                    "client" : project.client.client_name,
                    "users" : users,
                    "created_at" : str(project.created_at),
                    "created_by" : user_extended.user.username
                }
                return JsonResponse(data)
            else:
                return JsonResponse({"Warning" : "User Not Logged In"})
        else:
            return JsonResponse({"Warning" : "id Not Specified"})

@csrf_exempt
def user_login(request):
    if request.method == "POST":
        if not request.user.is_authenticated:
            data = json.loads(request.body)
            user = authenticate(request,username=data['username'], password=data['password'])
            if user:
                login(request,user)
                return JsonResponse({"payload" : "Succesfully Log in"})
            else:
                return JsonResponse({"payload" : "Invalid Credential"})
        else:
            return JsonResponse({"payload" : "Already Loged in"})
    else:
        return JsonResponse({"Warning" : "Wrong Request Method"})

@csrf_exempt
def user_logout(request):
    logout(request)
    return JsonResponse({"message" : "Successfully Log out"})