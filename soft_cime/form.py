from socket import fromshare
from django import forms
from .models import *

class newContribForm(forms.ModelForm):
    class Meta:
        model = contribuable
        fields = ('NIU','raison_social','activite','regime_impot','telephone','arrondissement','departement','ug','sous_secteur','impots')
 
        
class newDeclaration(forms.ModelForm):
    class Meta:
        model = Declaration
        fields = ('num_avis','chiffre_affaire','date_limite','contribuable','personnel')
