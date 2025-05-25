import json
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from stock_products.models import Article, ArticleModifier, Composant, ComposantModifier
from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from datetime import datetime, timedelta
from django.db.models import Sum
from django.db.models.functions import TruncDate
from .models import Composant, ComposantModifier



from stock_products.models import (
    Article, ArticleModifier,
    Composant, ComposantModifier
)

JOURS_FR = {
    'Monday': 'Lundi',
    'Tuesday': 'Mardi',
    'Wednesday': 'Mercredi',
    'Thursday': 'Jeudi',
    'Friday': 'Vendredi',
    'Saturday': 'Samedi',
    'Sunday': 'Dimanche',
}

def get_start_of_week(date):
    return date - timedelta(days=date.weekday())
# stock_products/views.py
from django.http import JsonResponse

def modifications_semaine(request):
    # Exemple simple de réponse
    data = {
        "message": "Cette fonction modifications_semaine sera implémentée ici."
    }
    return JsonResponse(data)


@csrf_exempt
def modifications_semaine(request):
    if request.method == "GET":
        today = datetime.today().date()
        debut_semaine_actuelle = get_start_of_week(today)
        debut_semaine_derniere = debut_semaine_actuelle - timedelta(days=7)
        fin_semaine_derniere = debut_semaine_actuelle - timedelta(days=1)

        articles_modifs = (
            ArticleModifier.objects
            .annotate(jour=TruncDate('created_at'))
            .values('jour', 'article__reference')
            .annotate(total_quantite=Sum('nouvelle_quantite'))
            .order_by('jour')
        )

        composants_modifs = (
            ComposantModifier.objects
            .annotate(jour=TruncDate('created_at'))
            .values('jour', 'composant__reference')
            .annotate(total_quantite=Sum('nouvelle_quantite'))
            .order_by('jour')
        )

        semaine_derniere = {}
        cette_semaine = {}

        def ajouter_donnee(dico, item, type_modif, jour_date, ref):
            jour_str = jour_date.strftime('%Y-%m-%d')
            jour_anglais = jour_date.strftime('%A')
            jour_nom = JOURS_FR.get(jour_anglais, jour_anglais)
            cle_jour = f"{jour_nom} ({jour_str})"

            dico.setdefault(cle_jour, [])
            dico[cle_jour].append({
                'type': type_modif,
                'reference': ref,
                'quantite': item['total_quantite'],
            })

        for item in articles_modifs:
            jour_date = item['jour']
            ref = item['article__reference']
            if debut_semaine_actuelle <= jour_date <= today:
                ajouter_donnee(cette_semaine, item, 'article', jour_date, ref)
            elif debut_semaine_derniere <= jour_date <= fin_semaine_derniere:
                ajouter_donnee(semaine_derniere, item, 'article', jour_date, ref)

        for item in composants_modifs:
            jour_date = item['jour']
            ref = item['composant__reference']
            if debut_semaine_actuelle <= jour_date <= today:
                ajouter_donnee(cette_semaine, item, 'composant', jour_date, ref)
            elif debut_semaine_derniere <= jour_date <= fin_semaine_derniere:
                ajouter_donnee(semaine_derniere, item, 'composant', jour_date, ref)

        return JsonResponse({
            'semaine_derniere': semaine_derniere,
            'cette_semaine': cette_semaine,
        }, safe=False)

    return JsonResponse({"error": "Méthode non autorisée"}, status=405)

@csrf_exempt
def get_articles(request):
    if request.method == "GET":
        articles = Article.objects.all()
        articles_list = list(articles.values())
        composant = Composant.objects.all()
        composant_list = list(composant.values())
        return JsonResponse({"articles": articles_list, "composant_list": composant_list}, safe=False)
@csrf_exempt
def get_articles_modifier(request, reference):
    if request.method == "POST":
        articles_modifier = ArticleModifier.objects.filter(article__reference = reference)
        articles_list = list(articles_modifier.values())
        return JsonResponse({"articles_modifier": articles_list}, safe=False , status=200)
@csrf_exempt
def get_composant_modifier(request, reference):
    if request.method == "POST":
        composant_modifier = ComposantModifier.objects.filter(composant__reference = reference)
        composants_list = list(composant_modifier.values())
        return JsonResponse({"composant_modifier": composants_list}, safe=False , status=200)


@csrf_exempt
def update_quantite(request):
    if request.method == "POST":
        data = json.loads(request.body)
        quantite = data.get("quantite")
        reference_article = data.get("reference_article")
        mode = data.get("mode", "set")  # "add", "remove", ou "set"

        article = get_object_or_404(Article, reference=reference_article)
        ancienne_quantite = article.quantite

        # Modification selon le mode
        if mode == "add":
            article.quantite += quantite
        elif mode == "remove":
            if article.quantite >= quantite:
                article.quantite -= quantite
            else:
                return JsonResponse({"error": "Stock insuffisant"}, status=400)
        elif mode == "set":
            article.quantite = quantite
        else:
            # Cas où le mode n'est pas reconnu
            return JsonResponse({"error": f"Mode inconnu: {mode}"}, status=400)

        article.save()

        # Historique
        ArticleModifier.objects.create(
            article=article,
            nouvelle_quantite=article.quantite,
            ancienne_quantite=ancienne_quantite,
            mode=mode
        )

        return JsonResponse({
            "success": "modifié",
            "nouvelle_quantite": article.quantite,
            "ancienne_quantite": ancienne_quantite,
            "mode": mode
        }, safe=False, status=200)
    else:
        return JsonResponse({"error": "Méthode non autorisée"}, status=405)

@csrf_exempt
def update_quantiteC(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            quantite = data.get("quantite")
            reference_c = data.get("reference_c")
            mode = data.get("mode", "set")  # "add", "remove", ou "set"

            if quantite is None or reference_c is None:
                return JsonResponse({"error": "Quantité ou référence manquante"}, status=400)

            composant = get_object_or_404(Composant, reference=reference_c)
            ancienne_quantite = composant.quantite  # AVANT modification

            # Modification selon le mode
            if mode == "add":
                composant.quantite += quantite
            elif mode == "remove":
                if composant.quantite >= quantite:
                    composant.quantite -= quantite
                else:
                    return JsonResponse({"error": "Stock insuffisant"}, status=400)
            elif mode == "set":
                composant.quantite = quantite
            else:
                return JsonResponse({"error": f"Mode inconnu: {mode}"}, status=400)

            composant.save()

            # Historique
            ComposantModifier.objects.create(
                composant=composant,
                nouvelle_quantite=composant.quantite,
                ancienne_quantite=ancienne_quantite,
                mode=mode
            )

            return JsonResponse(
                {
                    "success": "modifié",
                    "nouvelle_quantite": composant.quantite,
                    "ancienne_quantite": ancienne_quantite,
                    "mode": mode
                },
                safe=False,
                status=200,
            )
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Méthode non autorisée"}, status=405)
@csrf_exempt
def get_composant(request):
    if request.method == "POST":
        data = json.loads(request.body)
        reference = data.get("reference")
        composants = Composant.objects.filter(article__reference=reference)
        composants_list = list(composants.values())
        
        return JsonResponse({"composants": composants_list,} , status = 200)
@csrf_exempt
def get_all_composant(request):
    if request.method == "GET":
        composants = Composant.objects.all()
        composants_list = list(composants.values())
        
        return JsonResponse({"composants": composants_list,} , status = 200)       
        
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def add_article(request): 
    if request.method == "POST": 
        try:
            data = json.loads(request.body)
            reference = data.get("reference")
            description = data.get("description")
            quantite = data.get("quantite")
            ordre = data.get("ordre")

            if not all([reference, description, quantite,ordre]):
                return JsonResponse({"error": "Tous les champs sont requis"}, status=400)

            article = Article.objects.create(
                reference=reference,
                description=description,
                quantite=quantite,
                ordre=ordre,
            )
            article.save()

            return JsonResponse({
                "message": "Article ajouté avec succès",
                
            }, status=201)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Données JSON invalides"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Méthode non autorisée"}, status=405)

@csrf_exempt
def ajouter_piece(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        reference = data.get('reference')
        
        try:
            article = Article.objects.get(reference=reference)
            article.quantite += 1
            article.save()
            return JsonResponse({'message': 'Quantité mise à jour', 'quantite': article.quantite})
        except Article.DoesNotExist:
            return JsonResponse({'error': 'Article non trouvé'}, status=404)
    
    return JsonResponse({'error': 'Méthode non autorisée'}, status=405)


@csrf_exempt
def add_composant(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            referenceA = data.get("referenceA")  # Référence de l'article auquel rattacher le composant
            reference = data.get("reference")    # Référence du composant
            quantite = data.get("quantite")
            description = data.get("description")
            ordre = data.get("ordre")

            if not all([reference, referenceA, quantite,ordre]):
                return JsonResponse({"error": "Tous les champs sont requis"}, status=400)

            article = Article.objects.get(reference=referenceA)

            composant = Composant.objects.create(
                reference=reference,
                quantite=quantite,
                description=description,
                ordre=ordre,
            )
            composant.article.add(article)
            composant.save()

            return JsonResponse({"message": "Composant ajouté avec succès"}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Données JSON invalides"}, status=400)
        except Article.DoesNotExist:
            return JsonResponse({"error": "Article non trouvé"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Méthode non autorisée"}, status=405)
@csrf_exempt
def delete_article(request) : 
    if request.method == "DELETE" :
        data = json.loads(request.body)
        reference = data.get("reference")
        article = Article.objects.get(reference = reference)
        article.delete()
        return JsonResponse({"SUCCESS": "article supprimé"}, status=200)
@csrf_exempt
def delete_composant(request) : 
    if request.method == "DELETE" :
        data = json.loads(request.body)
        reference = data.get("reference")
        article = Composant.objects.get(reference = reference)
        article.delete()
        return JsonResponse({"SUCCESS": "composant supprimé"}, status=200)