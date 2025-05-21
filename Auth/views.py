from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth.models import User

from django.http import JsonResponse
from django.contrib.auth.hashers import check_password

from Auth.models import Admin, SuperAdmin, Utilisateur
import shortuuid
from Auth.utils import generate_jwt_token
import jwt

@csrf_exempt
def login_employee(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return JsonResponse({'message': 'Utilisateur non trouvé', 'status': 'failed'}, status=404)

        superAdmin = SuperAdmin.objects.filter(user=user).exists()
        admin = Admin.objects.filter(user=user).exists()
        utilisateur = Utilisateur.objects.filter(user=user).exists()
        blocked_user = Admin.objects.filter(user=user).first() if admin else Utilisateur.objects.filter(user=user).first() if utilisateur else SuperAdmin.objects.filter(user=user).first()

        if check_password(password, user.password) and (blocked_user.is_blocked == False):
            token = generate_jwt_token(user.id)
            return JsonResponse({
                'message': 'Connexion réussie',
                'superAdmin': superAdmin,
                'admin': admin,
                'utilisateur': utilisateur,
                'token': token,
                'username': username
            }, status=200)
        else:
            return JsonResponse({'message': 'Mot de passe incorrect ou utilisateur bloqué', 'status': 'failed'}, status=400)

@csrf_exempt
def logout_employee(request):
    if request.method == 'POST':
        # Aucun traitement côté serveur requis
        return JsonResponse({'message': 'Déconnexion côté client réussie'}, status=200)
    else:
        return JsonResponse({'message': 'Méthode non autorisée'}, status=405)


@csrf_exempt
def get_users(request , is_admin , is_super_Admin): 
        if request.method == "POST" : 
            if(is_admin == "true" or is_super_Admin == "true") : 
                   admins = Admin.objects.all()
                   users = Utilisateur.objects.all()
                   admins_list = list(admins.values())
                   users_list = list(users.values()) 
                   return JsonResponse({"users" : users_list , 'admins':admins_list} , status=200)
        else : 
               return JsonResponse({"echec" : "echec"} , status=400) 
@csrf_exempt
def block_user(request, email):
    if request.method == "POST":
        print("methode mriigla")
       
        print("user trouver ")
        user = Utilisateur.objects.filter(email = email).first()  # Assurez-vous de gérer le cas où il n'y a pas d'administrateurs
        print(user)
        if user:
            user.is_blocked = True
            user.save()
            return JsonResponse({"message": "user bloqué"}, status=200)
        else:
            return JsonResponse({"erreur": "Aucun administrateur trouvé pour cet utilisateur"}, status=404)
    else:
        return JsonResponse({"erreur": "erreur"}, status=400)


@csrf_exempt
def dblock_user(request, email):
    if request.method == "POST":
        print("methode mriigla")
        print("user trouver ")
        user = Utilisateur.objects.filter(email = email).first()  # Assurez-vous de gérer le cas où il n'y a pas d'administrateurs
        print(user)
        if user:
            user.is_blocked = False
            user.save()
            return JsonResponse({"message": "user bloqué"}, status=200)
        else:
            return JsonResponse({"erreur": "Aucun administrateur trouvé pour cet utilisateur"}, status=404)
    else:
        return JsonResponse({"erreur": "erreur"}, status=400)


@csrf_exempt
def block_admin(request, email):
    if request.method == "POST":
        print("methode mriigla")
       
        print("user trouver ")
        admin = Admin.objects.filter(email = email).first()  # Assurez-vous de gérer le cas où il n'y a pas d'administrateurs
        print(admin)
        if admin:
            admin.is_blocked = True
            admin.save()
            return JsonResponse({"message": "user bloqué"}, status=200)
        else:
            return JsonResponse({"erreur": "Aucun administrateur trouvé pour cet utilisateur"}, status=404)
    else:
        return JsonResponse({"erreur": "erreur"}, status=400)

@csrf_exempt
def dblock_admin(request, email):
    if request.method == "POST":
        print("methode mriigla")
       
        print("user trouver ")
        admin = Admin.objects.filter(email = email).first()  # Assurez-vous de gérer le cas où il n'y a pas d'administrateurs
        print(admin)
        if admin:
            admin.is_blocked = False
            admin.save()
            return JsonResponse({"message": "user bloqué"}, status=200)
        else:
            return JsonResponse({"erreur": "Aucun administrateur trouvé pour cet utilisateur"}, status=404)
    else:
        return JsonResponse({"erreur": "erreur"}, status=400)

@csrf_exempt
def delete_user(request, email):
    if request.method == "DELETE":
        print("methode mriigla")
       
        print("user trouver ")
        user = Utilisateur.objects.filter(email = email).first()  # Assurez-vous de gérer le cas où il n'y a pas d'administrateurs
        print(user)
        if user:
            user.delete()
            
            return JsonResponse({"message": "user bloqué"}, status=200)
        else:
            return JsonResponse({"erreur": "Aucun administrateur trouvé pour cet utilisateur"}, status=404)
    else:
        return JsonResponse({"erreur": "erreur"}, status=400)

@csrf_exempt
def delete_admin(request, email):
    if request.method == "DELETE":
        print("methode mriigla")
        print("user trouver ")
        user = Admin.objects.filter(email = email).first()  # Assurez-vous de gérer le cas où il n'y a pas d'administrateurs
        print(user)
        if user:
            user.delete()
            
            return JsonResponse({"message": "user bloqué"}, status=200)
        else:
            return JsonResponse({"erreur": "Aucun administrateur trouvé pour cet utilisateur"}, status=404)
    else:
        return JsonResponse({"erreur": "erreur"}, status=400)