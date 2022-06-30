from pickle import TRUE
from tabnanny import verbose
from tkinter import CASCADE
from types import CellType
from xml.parsers.expat import model
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

########################################################################
#                     CLASSE UNITE DE GESTION                          #
########################################################################
class UG(models.Model):
     ug = models.PositiveIntegerField(verbose_name='Unité de gestion')
     activite = models.CharField(max_length=200, null=True)

     def __str__(self):
          return "UG " + str(self.ug) + " : " + self.activite


########################################################################
#                     CLASSE SOUS SECTEUR                              #
########################################################################
class Sous_secteur(models.Model):
     libelle = models.CharField(max_length=200, verbose_name='Libéllé du sous unité de gestion')
     ug = models.ForeignKey(UG, on_delete=models.CASCADE)
     
     def __str__(self):
          return self.libelle


########################################################################
#                     CLASSE REGIME D'IMPOSITION                       #
########################################################################
class Regime_impot(models.Model):
     REGIME_IMPOT = (
          ('RPM', 'RPM'),
          ('RPP', 'RPP'),
          ('REEL', 'REEL'),
          ('SIMPLIFIE', 'SIMPLIFIE'),
          ('HRI', "Hors régime d'imposition"),
     )
     regime_impot = models.CharField(max_length=20, choices=REGIME_IMPOT, verbose_name="Régime d'imposition")
     
     def __str__(self):
          return self.regime_impot


########################################################################
#                     CLASSE DEPARTEMENT                               #
########################################################################
class Departement(models.Model):
     departement = models.CharField(max_length=30)
    
     def __str__(self):
          return self.departement


########################################################################
#                     CLASSE CONTRIBUABLE                             #
########################################################################

class contribuable(models.Model):
     NIU = models.CharField(max_length=200)
     raison_social = models.CharField(max_length=200)
     activite = models.CharField(max_length=200)
     telephone = models.CharField(max_length=200, verbose_name='Téléphone')
     arrondissement = models.CharField(max_length=200)
     STATUT = (
          ('actif', 'Actif'),
          ('inactif', 'Inactif'),
     )
     statut = models.CharField(max_length=200, default='Actif', choices=STATUT)
     
     regime_impot = models.ForeignKey(Regime_impot, on_delete=models.CASCADE, null=True)
     departement = models.ForeignKey(Departement, on_delete=models.CASCADE)
     ug = models.ForeignKey(UG, on_delete=models.CASCADE, verbose_name='Unité de gestion')
     sous_secteur = models.ForeignKey(Sous_secteur, on_delete=models.CASCADE)
     
     def __str__(self):
          return self.NIU + ":" + self.raison_social


########################################################################
#                     CLASSE CELLULE                                   #
########################################################################
class Cellule(models.Model):
     nom = models.CharField(max_length=200)
     
     def __str__(self):
          return self.nom


########################################################################
#                     CLASSE SERVICE                                   #
########################################################################
class Service(models.Model):
     nom = models.CharField(max_length=200)
     cellule = models.ForeignKey(Cellule, on_delete=models.CASCADE)
     
     def __str__(self):
          return self.nom

########################################################################
#                         CLASSE PERSONNEL                             #
########################################################################
class Personnel(models.Model):
     matricule = models.CharField(max_length=20, unique=True)
     nom = models.CharField(max_length=200)
     poste = models.CharField(max_length=200)
     cellule = models.ForeignKey(Cellule, on_delete=models.CASCADE, null=True)
     service = models.ForeignKey(Service, on_delete=models.CASCADE, null=True)
     user = models.ForeignKey(User, on_delete=models.CASCADE)

     def __str__(self):
          return self.nom


########################################################################
#                     CLASSE PART IMPOT                                #
########################################################################
class Part_Impot(models.Model):
     nom = models.CharField(max_length=30)
     proprietaire = models.CharField(max_length=200)
     taux = models.DecimalField(max_digits=7, decimal_places=6)
     
     def montant(self, montant):
          if "PAT " in self.nom and montant != 0:
               if 141500 <= montant < 150000:
                    tdl = 22500
               elif 150000 <= montant < 200000:
                    tdl = 30000
               elif 200000 <= montant < 300000:
                    tdl = 45000
               elif 300000 <= montant < 400000:
                    tdl = 60000
               elif 400000 <= montant < 500000:
                    tdl = 75000    
               else:
                    tdl = 90000
                    
               pat_theo = montant - tdl
               
               if "FAR" in self.nom:
                    m = self.taux * montant
               elif "TDL" in self.nom:
                    m = self.taux * tdl
               else:
                    m = self.taux * pat_theo
          else:
               m = self.taux * montant

          return round(m)
     
     def __str__(self):
          return self.nom
               

########################################################################
#                     CLASSE IMPOT                                    #
########################################################################
class Impot(models.Model):
     impot = models.CharField(max_length=30, verbose_name="Impôt")
     TYPE_IMPOT = (
          ('Budgétaire', 'Budgétaire'),
          ('Totalement Bugétaire', 'Totalement Bugétaire'),
          ('Non Budgétaire', "Non Budgétaire"),
     )
     type_impot = models.CharField(max_length=30, choices=TYPE_IMPOT)
     parts_impot = models.ManyToManyField(Part_Impot)
     impot_nom = models.CharField(max_length=200, null=True)
     
     def __str__(self):
          return self.impot



     
     
########################################################################
#                     CLASSE DECLARATION                               #
########################################################################
class Declaration(models.Model):
     num_avis = models.PositiveIntegerField()
     chiffre_affaire = models.PositiveBigIntegerField()
     date_limite = models.DateField()
     contribuable = models.ForeignKey(contribuable, on_delete=models.CASCADE)
     impots = models.ManyToManyField(Impot, through="Impot_Declare", through_fields=("declaration", "impot"))
     
     date_emission = models.DateTimeField(auto_now=True)
     personnel = models.ForeignKey(Personnel, on_delete=models.CASCADE)

     def __str__(self):
          return "Déclaration de l'avis N° " + str(self.num_avis)
     
     def monnaieCA(self):
          s = "{:,}".format(self.chiffre_affaire).replace(',', ' ')
          return s

########################################################################
#  CLASSE D'ASSOCIATION PRODUIT PAR LA RELATION  DECLARATION  - IMPOT  #
########################################################################
class Impot_Declare(models.Model):
     declaration = models.ForeignKey(Declaration, on_delete=models.CASCADE)
     impot = models.ForeignKey(Impot, on_delete=models.CASCADE)
     montant = models.PositiveIntegerField()
     statut_payement = models.BooleanField(default=0)
     
     def monnaie(self):
          s = "{:,}".format(self.montant).replace(',', ' ')
          return s
     
     
     def partImpot(self, part):
          return part.taux * self.montant

########################################################################
#                       CLASSE PAYEMENT                                #
########################################################################
class Payement(models.Model):
     date = models.DateField(auto_now=True)
     montant = models.PositiveIntegerField()  
     num_avis = models.PositiveIntegerField(null=True)   
     personnel = models.ForeignKey(Personnel, on_delete=models.CASCADE)
     contribuable = models.ForeignKey(contribuable, on_delete=models.CASCADE)
     date_virement = models.DateField(null=True)
     num_virement = models.PositiveBigIntegerField(null=True) 
     ETAT = (
          ("Comptabilisé" , "Comptabilisé"),
          ("Non Comptabilisé" , "Non Comptabilisé")
     )
     etat = models.CharField(max_length=30, choices=ETAT, null=True)
     
     def __str__(self):
          return "Payement de l'avis N° " + str(self.num_avis)

########################################################################
#                            CLASSE AMR                                #
########################################################################
class AMR(models.Model):
     num_amr = models.PositiveBigIntegerField(unique=True)   
     date = models.DateField(auto_now=True)
     personnel = models.ForeignKey(Personnel, on_delete=models.CASCADE)
     contribuable = models.ForeignKey(contribuable, on_delete=models.CASCADE)
     impots = models.ManyToManyField(Impot, through="Impot_AMR", through_fields=("amr", "impot"))
     recette = models.CharField(max_length=200)
     
     def montant_monnaie(self):
          s = "{:,}".format(self.montant).replace(',', ' ')
          return s
     
########################################################################
#                   CLASSE IMPOT AMR                                #
########################################################################
class Impot_AMR(models.Model):
     amr = models.ForeignKey(AMR, on_delete=models.CASCADE)   
     impot = models.ForeignKey(Impot, on_delete=models.CASCADE)
     date = models.DateField(auto_now=True)
     montant = models.PositiveIntegerField()  
     montant_budg = models.PositiveIntegerField()

     def monnaie(self, x):
          s = "{:,}".format(self.montant).replace(',', ' ')
          return s
     
     def recette_budgM(self, x):
          s = "{:,}".format(self.montant_budg).replace(',', ' ')
          return s


########################################################################
#                     CLASSE PROJECTION                                #
########################################################################
class Projection(models.Model):
     date = models.DateField(auto_now=True)
     personnel = models.ForeignKey(Personnel, on_delete=models.CASCADE)
     contribuable = models.ForeignKey(contribuable, on_delete=models.CASCADE)
     montant = models.PositiveIntegerField(null=True)  
     CELLULE = (
          ("GESTION ET SUIVI" , "Gestion et suivi"),
          ("RECOUVREMENT" , "Recouvrement"),
          ("CONTROLE" , "Controle"),
     )
     cellule = models.CharField(max_length=30, choices=CELLULE, null=True)
     def montant_monnaie(self):
          s = "{:,}".format(self.montant).replace(',', ' ')
          return s
     
     
     
########################################################################
#               CLASSE PROJECTION IMPOT                                #
########################################################################
class Projection_Impot(models.Model):
     date = models.DateField(auto_now=True)
     personnel = models.ForeignKey(Personnel, on_delete=models.CASCADE)
     impot = models.ForeignKey(Impot, on_delete=models.CASCADE)
     montant = models.PositiveIntegerField(null=True)  

     def montant_monnaie(self):
          s = "{:,}".format(self.montant).replace(',', ' ')
          return s
     




     
     
