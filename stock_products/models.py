from django.db import models
import uuid


class Article(models.Model) : 
    #nom = models.CharField(max_length=400 , null=True)
    description = models.CharField(max_length=1500 , null = True)
    reference = models.CharField(primary_key=True , max_length=500)
    quantite = models.IntegerField(default=0)
    ordre = models.PositiveIntegerField(default=0)  # ordre métier ici aussi

class Composant(models.Model) :
    reference = models.CharField(max_length=500 , primary_key=True)
    quantite = models.IntegerField()
    description = models.TextField(max_length=1000 , null = True)
    article = models.ManyToManyField(Article, blank=True)  # ✅ corrigé
    ordre = models.IntegerField(null=True, blank=True)


class ArticleModifier(models.Model) : 
    article = models.ForeignKey(Article ,on_delete=models.CASCADE , null = False ,related_name="articleModifier")
    nouvelle_quantite = models.IntegerField()
    ancienne_quantite = models.IntegerField(null=True, blank=True)  # <-- ajoute ceci
    mode = models.CharField(max_length=10, default="set")           # <-- ajoute ceci
    created_at = models.DateTimeField( auto_now_add=True)

    

class ComposantModifier(models.Model) : 
    composant = models.ForeignKey(Composant ,on_delete=models.CASCADE , null = False ,related_name="composantModifier")
    nouvelle_quantite = models.IntegerField()
    ancienne_quantite = models.IntegerField(null=True, blank=True)  # <-- ajoute ceci
    mode = models.CharField(max_length=10, default="set")           # <-- ajoute ceci
    created_at = models.DateTimeField( auto_now_add=True)


    
