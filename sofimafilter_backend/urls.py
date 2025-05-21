"""
URL configuration for sofimafilter_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from stock_products import views
from Auth import views as v



urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/',v.login_employee , name="login"),
    path('logout/', v.logout_employee, name="logout"),
    path('getArticles/',views.get_articles , name="get"),
    path('deleteAricle/',views.delete_article , name="delete_article"),
    path('deleteComp/',views.delete_composant , name="delete_composant"),
    path('getComposant/',views.get_composant , name="get"),
    path('get_all_composant/',views.get_all_composant , name="get_all_composant"),
    path('updateQ/',views.update_quantite , name="update"),
    path('getArticlesModifier/<str:reference>/',views.get_articles_modifier , name="get_articles_modifier"),
    path('getComposantsModifier/<str:reference>/',views.get_composant_modifier , name="get_composant_modifier"),
    path('updateQC/',views.update_quantiteC , name="update"),
    path('adda/',views.add_article , name="add"),
    path('addC/',views.add_composant , name="addc"),
    path('block_admin/<str:email>/',v.block_admin , name="block_admin"),
    path('block_user/<str:email>/',v.block_user , name="block_user"),
    path('dblock_admin/<str:email>/',v.dblock_admin , name="block_admin"),
    path('dblock_user/<str:email>/',v.dblock_user , name="block_user"),
    path('delete_user/<str:email>/',v.delete_user , name="block_user"),
    path('delete_admin/<str:email>/',v.delete_admin , name="block_user"),
    path('getUsers/<str:is_admin>/<str:is_super_Admin>/',v.get_users , name="get_users"),
    path('api/ajouter-piece/',views.ajouter_piece , name="get_users"),
    path('api/modifications_semaine/', views.modifications_semaine, name='modifications_semaine'),

]