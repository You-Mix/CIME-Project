from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('accounts/login/', connexion, name='login'),
    path('logout/', deconnection, name='logout'),
    
    path('contribuables/', liste_contribuable, name='liste_contribuable'),
    path('contribuables/new/', new_contribuable, name='new_contribuable'),
    path('contribuables/<int:id>/', detail_contribuable, name='detail_contrib'),
    # path('delete_contrib/<int:idContrib>', deleteContrib, name='delete_contrib'),
    
    path('gestion/', liste_declaration, name='liste_declaration'),
    path('gestion/new_declaration', new_declaration, name='new_declaration'),
    path('gestion/declaration_impot/<int:idDec>', new_declaration_impots, name='new_declaration_impots'),
    path('gestion/declaration/<int:idDec>', detail_declaration, name='detail_declaration'),
    path('gestion/declaration_incomplete/', declaration_incomplete, name='declaration_incomplete'),
    path('gestion/update_declaration/<int:idDec>', update_declaration, name='update_declaration'),
    path('gestion/excel_declaration/<int:idDec>', excel_declaration, name='excel_declaration'),
    path('gestion/new_declaration/<int:idPaye>', new_declaration1, name='new_declaration1'),
    
    path('recette/', liste_payements, name='liste_payements'),
    path('recette/new_payement', new_payement, name='new_payement'),
    path('recette/paye_non_declare', payement_non_declare, name='paye_non_declare'),
    
    path('statistiques/1', stats1, name='stats1'),
    path('statistiques/1/excelStats1', excelStats1, name='excelStats1'),
    path('statistiques/2', stats2, name='stats2'),
    path('statistiques/2/excelStats2', excelStats2, name='excelStats2'),
    path('statistiques/3', stat_perf_recette, name='stat_perf_recette'),
    
    path('amr/new', new_amr, name='new_amr'),
    path('amr/new/<int:idAmr>', new_impot_amr, name='new_impot_amr'),
    path('amr/', liste_amr, name='liste_amr'),
    path('amr/incomplets/', amr_incomplet, name='amr_incomplet'),
    path('amr/update_amr/<int:idAmr>', update_amr, name='update_amr'),
    path('amr/<int:idAmr>', detail_amr, name='detail_amr'),
    path('amr/excel_amr/<int:idAmr>', excel_amr, name='excel_amr'),
    
    
    path('statistiques/stats_etats', stats_etats, name='stats_etats'),
    path('statistiques/stats_consolide_irc/<int:m>/<int:y>', stats_consolide_irc, name='stats_consolide_irc'),
    path('statistiques/stats_consolide_retc/<int:m>/<int:y>', stats_consolide_retc, name='stats_consolide_retc'),
    path('statistiques/etats_virements/<int:m>/<int:y>', excel_virements, name='excel_virements'),
    path('statistiques/recette_affectees/<int:m>/<int:y>', stats_recette_af, name='stats_recette_af'),    
    

    

]