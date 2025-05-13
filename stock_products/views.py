import json
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from stock_products.models import Article, ArticleModifier, Composant, ComposantModifier
from django.shortcuts import get_object_or_404

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
def update_quantite(request) : 
    if request.method == "POST" : 
        data = json.loads(request.body)
        quantite = data.get("quantite")
        reference_article = data.get("reference_article")
        article = get_object_or_404(Article, reference =reference_article)
        article.quantite = quantite
        article.save()
        article_modifier = ArticleModifier.objects.create(
            article = article,
            nouvelle_quantite = quantite
        )
        article_modifier.save()
        return JsonResponse({"success": "modifié"}, safe=False , status = 200)
    
@csrf_exempt
def update_quantiteC(request) : 
    if request.method == "POST" : 
        data = json.loads(request.body)
        quantite = data.get("quantite")
        reference_c = data.get("reference_c")
        
        composant = get_object_or_404(Composant, reference =reference_c)
        composant.quantite = quantite
        composant.save()
        Composant_modifier = ComposantModifier.objects.create(
            composant = composant,
            nouvelle_quantite = quantite
        )
        Composant_modifier.save()
        return JsonResponse({"success": "modifié"}, safe=False , status = 200)
 
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

            if not all([reference, description, quantite]):
                return JsonResponse({"error": "Tous les champs sont requis"}, status=400)

            article = Article.objects.create(
                reference=reference,
                description=description,
                quantite=quantite
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
            referencesA = data.get("referencesA")  # une liste de références d'articles
            reference = data.get("reference")
            quantite = data.get("quantite")
            description = data.get("description")

            # Vérification
            if not all([reference, referencesA, quantite]):
                return JsonResponse({"error": "Tous les champs sont requis"}, status=400)
            if not isinstance(referencesA, list):
                return JsonResponse({"error": "Le champ 'referencesA' doit être une liste"}, status=400)

            # Création du composant
            composant = Composant.objects.create(
                reference=reference,
                quantite=quantite,
                description=description
            )

            # Ajout des articles liés
            articles = Article.objects.filter(reference__in=referencesA)
            composant.article.set(articles)  # ManyToMany : set() ou add(*articles)

            return JsonResponse({
                "message": "Composant ajouté avec succès"
            }, status=201)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Données JSON invalides"}, status=400)
        except Article.DoesNotExist:
            return JsonResponse({"error": "Un ou plusieurs articles n'existent pas"}, status=404)
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