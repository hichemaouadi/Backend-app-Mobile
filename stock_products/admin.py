from django.contrib import admin

from stock_products.models import Article, ArticleModifier, Composant

class ArticleModifierAdmin(admin.ModelAdmin):
    list_display = ('article', 'nouvelle_quantite', 'created_at')
# Register your models here.
admin.site.register(Article)

admin.site.register(Composant)
admin.site.register(ArticleModifier ,ArticleModifierAdmin )