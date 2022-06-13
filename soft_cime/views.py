from ast import Try
from datetime import date, datetime
from email import message
from heapq import merge
from itertools import product
from multiprocessing import context
from tkinter.ttk import Style
from unicodedata import name
from xmlrpc.client import DateTime
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from .models import *
from soft_cime.utils import render_to_pdf
from django.views.generic import View
import matplotlib.pyplot as plt
import urllib, base64
import numpy as np
import io
# from .form import *

from datetime import date

from openpyxl import *

import xlrd
import os
from tempfile import NamedTemporaryFile
from django.db.models import Q
from django.db.models import Sum
# Create your views here.
today = date.today()


def connexion(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            messages.success(request, "Login succesfully")
            return redirect('index')
        else:
            messages.error(request, "ERREUR !!!")
    return render(request, "soft_cime/login.html")


@login_required
def deconnection(request):
    logout(request)
    return redirect("login")


# @login_required
# def deleteContrib(request, idContrib):
#     contrib = get_object_or_404(contribuable, id=idContrib)
#     if request.method == "POST":
#         contrib.delete()
#         return redirect('liste_contribuable')

#     return render(request, "soft_cime/deleteConfirm.html", {'contribuable':contrib})

@login_required
def index(request):
    if request.user.is_authenticated:
        nbcontrib = contribuable.objects.count()
        personnel = Personnel.objects.get(user=request.user)
        nbDec = Declaration.objects.count()
        nbPaye =Payement.objects.count()
        percent = 100/nbcontrib
        import random
        r = lambda: random.randint(0,255)
        couleur = []
        for i in range(0,5):
            couleur.append("("+str(r())+","+str(r())+","+str(r())+")")
            
        ugs = UG.objects.all()
        
        tab_contrib = []
        recipe = []
        for ug in ugs:
            recipe.append(str(ug.contribuable_set.count()) + " UG " + str(ug.ug) )
                
            
        fig, ax = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))

        

        data = [float(x.split()[0]) for x in recipe]
        ingredients = [str(x.split()[-2]) + str(x.split()[-1]) for x in recipe]


        def func(pct, allvals):
            absolute = int(np.round(pct/100.*np.sum(allvals)))
            return "{:.1f}%\n({:d})".format(pct, absolute)


        wedges, texts, autotexts = ax.pie(data, autopct=lambda pct: func(pct, data),
                                        textprops=dict(color="w"))

        ax.legend(wedges, ingredients,
                title="Unité de gestion",
                loc="center left",
                bbox_to_anchor=(1, 0, 0.5, 1))

        plt.setp(autotexts, size=8, weight="bold")

        ax.set_title("CONTRIBUABLE EN FONCTION DES UG")
        
        
        graphe = plt.gcf()
        buf = io.BytesIO()
        graphe.savefig(buf, format='png')
        buf.seek(0)
        string = base64.b64encode(buf.read())
        uri = urllib.parse.quote(string)
        
        
        
        context = {
            "nbcontrib" : nbcontrib,
            "personnel" : personnel,
            "nbDec" : nbDec,
            "nbPaye" : nbPaye,
            "ugs" : ugs,
            "couleur" : couleur,
            "percent" : percent,
            "today" : today,
            "data" : uri,
            
        }
        return render(request, "soft_cime/index.html", context)
    else:
        return redirect('login')





    
# Menu Contribuable
@login_required
def liste_contribuable(request):
    contrib_list = contribuable.objects.all()
    nbContrib = contribuable.objects.count()


    context = {
        'contribuable' : contrib_list,
        'nbContrib' : nbContrib
    }
    
    

    return render(request, "soft_cime/contribuable-list.html", context)


@login_required
def new_contribuable(request):

    # if request.method == 'POST':
    #     fichier = load_workbook(request.POST.get("file"))
    #     sh = fichier["Table1"]
    #     for j in sh:
    #         i=j[0].value
    #         NIU=sh.cell(row=i, column=2).value 
    #         raison_social=sh.cell(row=i, column=3).value 
    #         activite=sh.cell(row=i, column=4).value
    #         regime_impot = sh.cell(row=i, column=5).value
    #         telephone=sh.cell(row=i, column=6).value
    #         arrondissement=sh.cell(row=i, column=7).value
    #         departement=sh.cell(row=i, column=8).value
    #         statut=sh.cell(row=i, column=9).value
    #         ug=sh.cell(row=i, column=10).value
    #         sous_secteur=sh.cell(row=i, column=11).value
                                                     
    #         newContrib = contribuable.objects.create(NIU=NIU, raison_social=raison_social, activite=activite, regime_impot=Regime_impot.objects.get(id=regime_impot),telephone=telephone, arrondissement=arrondissement, departement=Departement.objects.get(id=departement), ug=UG.objects.get(id=ug), sous_secteur=Sous_secteur.objects.get(id=sous_secteur))
    #         newContrib.save()
            

        
    message = " "
    if request.method == 'POST':
        NIU = request.POST.get('NIU')
        raison_social = request.POST.get('raison_social')
        activite = request.POST.get('activite')
        telephone = request.POST.get('telephone')
        arrondissement = request.POST.get('arrondissement')
        departement = Departement.objects.get(departement=request.POST.get('departement'))
        regime_impot = Regime_impot.objects.get(regime_impot=request.POST.get('regime_impot'))
        ug = UG.objects.get(ug=request.POST.get('ug'))
        sous_secteur = Sous_secteur.objects.get(libelle=request.POST.get('sous_secteur'))
        
        if len(contribuable.objects.filter(NIU=NIU))==0:
            newContrib = contribuable.objects.create(NIU=NIU, raison_social=raison_social, activite=activite, regime_impot=regime_impot,telephone=telephone, arrondissement=arrondissement, departement=departement, ug=ug, sous_secteur=sous_secteur)
            if newContrib.save():
                message = "Enregistrer avec succès"
                classmsg = "text-success"
            else:
                message = "Erreur lors de l'enregistrement"
                classmsg = "text-danger"
        else:
            message = "Le contribuable existe dejà"
            classmsg = "text-danger"
        
        
        
        
            
    regimes_impots = Regime_impot.objects.all()
    departements = Departement.objects.all()
    impots = Impot.objects.all()
    ugs = UG.objects.all()
    sous_secteurs = Sous_secteur.objects.all()
    context = {
        'message':message,
        'regimes_impots' : regimes_impots,
        'departements' : departements,
        'impots':impots,
        'ugs':ugs,
        'sous_secteurs':sous_secteurs,
        'classmsg' : classmsg,
    }
    return render(request, "soft_cime/contribuable-new.html", context)


@login_required
def detail_contribuable(request,id):
    
    contrib = contribuable.objects.get(pk=id)
    declarations = Declaration.objects.filter(contribuable=contrib)
    # impots_declare = Impot_Declare.objects.filter(declaration in declarations)
    
    declarations_infos = []
    
    for declaration in declarations:
        line=[]
        line.append(declaration.num_avis)
        line.append(declaration.date_emission)
        montant_dec=Impot_Declare.objects.filter(declaration = declaration).aggregate(Sum('montant'))
        line.append(montant_dec['montant__sum'])
        declarations_infos.append(line)
    
    amrs = AMR.objects.filter(contribuable=contrib)
    # impots_declare = Impot_Declare.objects.filter(declaration in declarations)
    
    amr_infos = []
    
    for amr in amrs:
        line=[]
        line.append(amr.num_amr)
        line.append(amr.date)
        montant_dec=Impot_AMR.objects.filter(amr = amr).aggregate(Sum('montant'))
        line.append(montant_dec['montant__sum'])
        amr_infos.append(line)
        
        
    # total_dec=Impot_Declare.objects.filter(declaration in declarations).aggregate(sum('montant'))
        
    payements = Payement.objects.filter(contribuable=contrib)
    context = {
        'contribuable' : contrib,
        'declarations_infos' : declarations_infos,
        'payements' : payements,
        'declarations' : declarations,
        'amr_infos' : amr_infos,
    }
    
    

    return render(request, "soft_cime/contribuable-detail.html", context)


# Menu Gestion et Suivie
@login_required
def liste_declaration(request):
    declaration_history = Declaration.objects.all().order_by('-date_emission')
    nbdeclaration = Declaration.objects.count()
    impots_declare = Impot_Declare.objects.all()
    


    context = {
        'declarations' : declaration_history,
        'nbdeclaration' : nbdeclaration,
        'impots_declare' : impots_declare,
    }
    
    
    return render(request, "soft_cime/declaration-history.html", context)


@login_required
def declaration_incomplete(request):
    declaration_history = Declaration.objects.filter().order_by('-date_emission')
    nbdeclaration = Declaration.objects.count()
    impots_declare = Impot_Declare.objects.all()
    


    context = {
        'declarations' : declaration_history,
        'nbdeclaration' : nbdeclaration,
        'impots_declare' : impots_declare,
    }
    
    
    return render(request, "soft_cime/declaration-incomplet.html", context)


@login_required
def new_declaration(request):
    #formDec = newDeclaration(request.POST or None)
    contribuables = contribuable.objects.all()
    impots = Impot.objects.all()
    today = date.today()
    message = ""
    classmsg = ""
    
    
    if request.method == 'POST':
        num_avis = request.POST.get("num_avis")
        if len(Declaration.objects.filter(num_avis=num_avis))==0:
            contrib = contribuable.objects.get(NIU=request.POST.get("contribuable"))
            chiffre_affaire = request.POST.get("chiffre_affaire")
            date_limite = request.POST.get("date_limite")
            personnel = Personnel.objects.get(user = request.user)
            
            newDeclaration = Declaration.objects.create(num_avis=num_avis,contribuable=contrib,chiffre_affaire=chiffre_affaire, date_limite=date_limite, personnel=personnel )        
            newDeclaration.save()
            return redirect('new_declaration_impots',newDeclaration.id)
        else:
            message = "Declaration already exist"
            classmsg = "text-danger"
        
    context = {
        'contribuables' : contribuables,
        'impots':impots,
        'today':today,
        'message' : message,
        'classmsg' : classmsg,
    }
    return render(request, "soft_cime/declaration-new.html", context)


@login_required
def update_declaration(request, idDec):
    #formDec = newDeclaration(request.POST or None)
    contribuables = contribuable.objects.all()
    declaration = Declaration.objects.get(id=idDec)
    today = date.today()
    
    context = {
        'contribuables' : contribuables,
        'declaration':declaration,
        'today':today,
    }
    
    if request.method == 'POST':
        
        declaration.num_avis = request.POST.get("num_avis")
        declaration.contribuable = contribuable.objects.get(NIU=request.POST.get("contribuable"))
        declaration.chiffre_affaire = request.POST.get("chiffre_affaire")
        declaration.date_limite = request.POST.get("date_limite")
        
        declaration.save()
        
        
        return redirect('new_declaration_impots',declaration.id)
    
    return render(request, "soft_cime/declaration-update.html", context)


@login_required
def new_declaration_impots(request, idDec):
    # formDec = newDeclaration(request.POST or None)
    # impots = contrib.impots.all()
    impots = Impot.objects.all()
    declaration = get_object_or_404(Declaration, pk=idDec)
    impots_declares = Impot_Declare.objects.filter(declaration=declaration).order_by("-id")
    message=""
    classmsg = ""
    if request.method == "POST":
        montant = request.POST.get("montant")
        impot = Impot.objects.get(impot=request.POST.get('impot'))
        exist = Impot_Declare.objects.filter(impot=impot) & Impot_Declare.objects.filter(declaration=declaration)
        if len(exist) == 0:
            newImpotDec = Impot_Declare.objects.create(declaration=declaration, impot=impot, montant=montant)
            newImpotDec.save()
            message = "Enregistré"
            classmsg = "text-success"
        else:
            message = "Impot Déjà Déclaré"
            classmsg = "text-danger"
            
    context = {
        'impots':impots,
        "message":message,
        "classmsg" : classmsg,
        'impots_declares' : impots_declares,
    }
    return render(request, "soft_cime/declaration-new1.html", context)


@login_required
def detail_declaration(request,idDec):
    
    declaration = Declaration.objects.get(id=idDec)
    impots_declares = Impot_Declare.objects.filter(declaration=declaration)
    context = {
        'declaration' : declaration,
        'impots_declares' : impots_declares,
    }
    
    

    return render(request, "soft_cime/declaration-detail.html", context)

@login_required
def excel_declaration(request,idDec):
    
    declaration = Declaration.objects.get(id=idDec)
    impots_declares = Impot_Declare.objects.filter(declaration=declaration)
    context = {
        'declaration' : declaration,
        'impots_declares' : impots_declares,
    }
    wb=load_workbook("soft_cime/static/doc/detail declaration.xlsx")
    ws = wb.active
    
    ws['B3'] = str(declaration.num_avis)
    ws['B4'] = str(declaration.contribuable.NIU) + " : " + str(declaration.contribuable.raison_social)
    ws['B5'] = str(declaration.chiffre_affaire)
    ws['B6'] = str(declaration.date_emission)
    ws['B7'] = str(declaration.date_limite)
    ws['B8'] = declaration.personnel.nom
    
    paye = Payement.objects.filter(num_avis=declaration.num_avis)
    if len(paye) != 0:
        for p in paye:
            ws['B9'] = "Payement enregistré le " + str(p.date)
    else:
        ws['B9'] = "Non payé"
    
    # if declaration.num_avis in Payement.objects.all().num_avis:
    #     ws['B9'] = "Payé"
    
    j='A'
    i=13
    for impot in impots_declares:
        ws["A"+str(i)]=impot.impot.impot
        ws["B"+str(i)]=impot.montant
        i = i+1
        # j=chr(ord(j) + 1)

    ws.oddFooter.center.text ="Powered by Le Gestionnaire \n" + str(datetime.today())
    wb.save(os.path.expanduser("~/Downloads/Déclaration " + str(declaration.num_avis) + ".xlsx"))
    os.popen(os.path.expanduser("~/Downloads/Déclaration " + str(declaration.num_avis) + ".xlsx"))
    
    return redirect("detail_declaration", idDec)




# Menu suivi des Recette
@login_required
def liste_payements(request):
    payement_history = Payement.objects.all()
    nbpayement = Payement.objects.count()
    


    context = {
        'payements' : payement_history,
        'nbpayement' : nbpayement,
    }
    
    
    return render(request, "soft_cime/payement-history.html", context)

@login_required
def payement_declare(request):
    payement_history = Payement.objects.all()
    declarations = Declaration.objects.all()
    
    paye_declare = []
    n=0
    for payement in payement_history:
        infos = [1, 2]
        for declaration in declarations:
            if (declaration.num_avis == payement.num_avis) and (declaration.contribuable.NIU == payement.contribuable.NIU):
                impots = ""
                for impot in declaration.impots.all():
                    impots = impot.impot + ", "
                    
                infos = [declaration.num_avis, declaration.contribuable.NIU, declaration.date_emission, impots , payement.date, payement.montant]
                paye_declare.append(infos)
                n=n+1
                break


    context = {
        'paye_declare' : paye_declare,
        'nb_payeD' : n,
    }
    
    
    return render(request, "soft_cime/payement-declare.html", context)


def payement_non_declare(request):
    
    declarations = Declaration.objects.all()
    
    nums_avis = []
    for declaration in declarations:
        nums_avis.append(declaration.num_avis)
        
    
    payement_history = Payement.objects.filter(~Q(num_avis__in=nums_avis))
    

    context = {
        'payement_history' : payement_history,
    }
    
    
    return render(request, "soft_cime/payement-non_declare.html", context)



@login_required
def new_payement(request):
    contribuables = contribuable.objects.all()
    declarations = Declaration.objects.all()
    context = {
        'contribuables' : contribuables,
        'declarations' : declarations,
        'today' : today,
    }
    
    if request.method == 'POST':
        num_avis = request.POST.get("num_avis")
        contrib = contribuable.objects.get(NIU=request.POST.get("contribuable"))
        montant = request.POST.get("montant")
        datep = request.POST.get("date")
        personnel = Personnel.objects.get(user = request.user)
        
        newPayement = Payement.objects.create(num_avis=num_avis,contribuable=contrib,montant=montant, date=datep, personnel=personnel )        
        newPayement.save()
    
    return render(request, "soft_cime/payement-new.html", context)

# Menu Statistique
@login_required
def stats1(request):
    ugs = UG.objects.all()
    nbContrib = contribuable.objects.count()
    regime_impots = Regime_impot.objects.all()
    departements = Departement.objects.all()
    context = {
        "ugs" : ugs,
        "nbContrib" :nbContrib,
        "regime_impots" : regime_impots,
        "departements" : departements,
    }
    return render(request, "soft_cime/stats1.html", context)

def excelStats1(request):
    ugs = UG.objects.all()
    nbContrib = contribuable.objects.count()
    regime_impots = Regime_impot.objects.all()
    departements = Departement.objects.all()
    
    bigTitle = styles.NamedStyle(name = 'bigTitle')
    borderStyle1 = styles.Side(style = 'double', color = '000000')
    bigTitle.border = styles.Border(left = borderStyle1, right = borderStyle1, top = borderStyle1, bottom = borderStyle1)
    bigTitle.font = styles.Font(name = 'Times New Roman', size = 12, bold=True)
    
    headstyle = styles.NamedStyle(name = 'headstyle')
    headstyle.font = styles.Font(name = 'Times New Roman', size = 10, color = 'ffffff', bold=True)
    headstyle.fill = styles.PatternFill(patternType = 'solid', fgColor = '212529')
    borderStyle = styles.Side(style = 'thin', color = 'cccccc')
    headstyle.border = styles.Border(left = borderStyle, right = borderStyle, top = borderStyle, bottom = borderStyle)
    headstyle.alignment.horizontal = "center"
    
    subtitle = styles.NamedStyle(name = 'subtitle')
    subtitle.font = styles.Font(name = 'Times New Roman', size = 10, bold=True)
    subtitle.fill = styles.PatternFill(patternType = 'solid', fgColor = 'cccccc')
    subtitle.border = styles.Border(left = borderStyle, right = borderStyle, top = borderStyle, bottom = borderStyle)
    subtitle.alignment.horizontal = "center"
    
    s2 = styles.NamedStyle(name = 's2')
    s2.alignment.horizontal = "center"
    s2.border = styles.Border(left = borderStyle, right = borderStyle, top = borderStyle, bottom = borderStyle)
    
    s1 = styles.NamedStyle(name = 's1')
    s1.alignment.horizontal = "center"
    s1.font = styles.Font(bold=True)
    s1.border = styles.Border(left = borderStyle, right = borderStyle, top = borderStyle, bottom = borderStyle)
    
    
    
    wb= Workbook()
    ws = wb.active
    
    ws.oddHeader.center.text ="PAR REGIME D'IMPOSITION ET PAR DEPARTEMENT"
    ws.oddHeader.center.font  = "Times New Roman"
    ws.oddHeader.center.size  = 14
    ws.oddHeader.center.border  = borderStyle1
    ws.oddFooter.center.text ="Powered by Le Gestionnaire \n" + str(datetime.today())
    
    ws.print_options.horizontalCentered = True
    
    ws["A1"].border = styles.Border(top = borderStyle1)
    ws.merge_cells("A1:E1")
    
    #PAR SOUS SECTEUR
    ws["A3"] = "SOUS SECTEURS" 
    ws["B3"] = "TAILLES"
    
    ws["A3"].style = headstyle
    ws["B3"].style = headstyle
    
    
    i=4
    for ug in ugs:
        ws.merge_cells("A"+str(i)+":"+"B"+str(i))
        ws["A"+str(i)] = "UG" + str(ug.ug)
        ws["A"+str(i)].style = subtitle
        i=i+1
        for sous_secteur in ug.sous_secteur_set.all():
            ws["A"+str(i)] = sous_secteur.libelle
            ws["A"+str(i)].border = styles.Border(left = borderStyle, right = borderStyle, top = borderStyle, bottom = borderStyle)
            ws["B"+str(i)] = sous_secteur.contribuable_set.count()
            ws["B"+str(i)].style = s2
            i=i+1
        
        ws["A"+str(i)] = "TOTAL " + str(ug.ug)
        ws["A"+str(i)].border = styles.Border(left = borderStyle, right = borderStyle, top = borderStyle, bottom = borderStyle)
        ws["B"+str(i)] = str(ug.contribuable_set.count())
        ws["B"+str(i)].style = s1
        i=i+1
    ws["A"+str(i)] = "TOTAL FICHIER"
    ws["A"+str(i)].style = subtitle
    ws["B"+str(i)] = str(nbContrib)
    ws["B"+str(i)].style = subtitle
    
    ws.column_dimensions['A'].width = 25
    ws.row_dimensions[1].height = 15
    
    #PAR REGIME 
    ws["D3"] = "REGIME D'IMPOSITION" 
    ws["E3"] = "TAILLES"
    
    ws["D3"].style = headstyle
    ws["E3"].style = headstyle
    
    i=4
    for regime in regime_impots:
        ws["D"+str(i)] = regime.regime_impot
        ws["D"+str(i)].border = styles.Border(left = borderStyle, right = borderStyle, top = borderStyle, bottom = borderStyle)
        ws["E"+str(i)] = regime.contribuable_set.count()
        ws["E"+str(i)].style = s1
        i=i+1
        
       
    ws["D"+str(i)] = "TOTAL"
    ws["D"+str(i)].style = subtitle
    ws["E"+str(i)] = str(nbContrib)
    ws["E"+str(i)].style = subtitle
    i=i+2
    
    #PAR DEPARTEMENT
    ws["D"+str(i)] = "DEPARTEMENT" 
    ws["E"+str(i)] = "TAILLES"
    
    ws["D"+str(i)].style = headstyle
    ws["E"+str(i)].style = headstyle
    
    i=i+1
    for departement in departements:
        ws["D"+str(i)] = departement.departement
        ws["D"+str(i)].border = styles.Border(left = borderStyle, right = borderStyle, top = borderStyle, bottom = borderStyle)
        ws["E"+str(i)] = departement.contribuable_set.count()
        ws["E"+str(i)].style = s1
        i=i+1
        
       
    ws["D"+str(i)] = "TOTAL"
    ws["D"+str(i)].style = subtitle
    ws["E"+str(i)] = str(nbContrib)
    ws["E"+str(i)].style = subtitle
    
    
    ws.column_dimensions['D'].width = 25
    
    # with NamedTemporaryFile() as tmp:
    #     wb.save(tmp.name)
    #     tmp.seek(0)
    #     stream = tmp.read()
    
    wb.save(os.path.expanduser("~/Downloads/stats_contribuable.xlsx"))
    os.popen(os.path.expanduser("~/Downloads/stats_contribuable.xlsx"))
    
    return redirect('stats1')
    
    
def stats2(request):
    
    ugs = UG.objects.all()
    nbContrib = contribuable.objects.count()
    
    impots = Impot.objects.all()
    sous_secteurs = Sous_secteur.objects.all()
    
    if request.method != "POST":
        mois=today.month
    else:
        mois = request.POST.get("mois")
        
    montant_ug_im_alls = []
    
    nbug=0
    line_Total_ug=[]
    line_Total_ug.append("TOTAUX")
    for ug in ugs:
        line_Total_ug.append(0)
        nbug = nbug+1
    line_Total_ug.append(0)
        
    for impot in impots:
        line = []
        line.append(impot.impot)
        ids = Impot_Declare.objects.filter(impot = impot)
        for ug in ugs:
            montant = 0
            total_impot = 0 
            for contrib in ug.contribuable_set.all():
                if today.month == 1:
                    declaration = Declaration.objects.filter(contribuable=contrib) &  Declaration.objects.filter(date_limite__month = 12) &  Declaration.objects.filter(date_limite__year = today.year-1)
                    annee = today.year - 1
                else:
                    declaration = Declaration.objects.filter(contribuable=contrib) &  Declaration.objects.filter(date_limite__month = today.month-1) &  Declaration.objects.filter(date_limite__year = today.year)
                    annee = today.year
                m=0
                for id1 in ids:
                    for dec in declaration:
                        if id1.declaration == dec:
                            m = id1.montant
                            break
                         
                montant = montant + m
            line_Total_ug[ug.ug]=line_Total_ug[ug.ug]+montant
            total_impot = total_impot + montant    
            line.append(montant)
        line.append(total_impot)
        line_Total_ug[nbug+1]=line_Total_ug[nbug+1]+total_impot
        montant_ug_im_alls.append(line)
        
    montant_ug_im_alls.append(line_Total_ug)            
    montant_ss_alls = []
    for sous_secteur in sous_secteurs:
        line = []
        line.append(sous_secteur.libelle)
        ids = Impot_Declare.objects.all()
        montant = 0 
        for contrib in sous_secteur.contribuable_set.all():
            if today.month == 1:
                declaration = Declaration.objects.filter(contribuable=contrib) &  Declaration.objects.filter(date_limite__month = 12) &  Declaration.objects.filter(date_limite__year = today.year-1)
            else:
                declaration = Declaration.objects.filter(contribuable=contrib) &  Declaration.objects.filter(date_limite__month = today.month-1) &  Declaration.objects.filter(date_limite__year = today.year)
            m=0
            for id1 in ids:
                for dec in declaration:
                    if id1.declaration == dec:
                        montant = montant + id1.montant
            
        line.append(montant)
        montant_ss_alls.append(line)
    
    mois ={
        1: "Janvier", 
        2: "Fevrier",
        3: "Mars",
        4: "Avril",
        5: "Mai",
        6: "Juin", 
        7: "Juillet",
        8: "Août",
        9: "Septembre",
        10: "Octobre",
        11: "Novembre",
        12: "Décembre",
    }   
    context = {
        "ugs" : ugs,
        "annee" : annee,
        "mois" : mois[today.month-1],
        "impots" : impots,
        "montant_ug_im_alls" : montant_ug_im_alls,
        "montant_ss_alls" : montant_ss_alls,
        
    }
    return render(request, "soft_cime/stats_perf_gestion.html", context)



# Excel stats 2
def excelStats2(request):
    wbl=load_workbook("soft_cime/static/doc/statistiques.xlsx")
    wb= Workbook()
    ws = wbl["Evaluation"]
    
    today = date.today()
    
    def set_border(ws, cell_range):
        border = styles.Border(left=styles.Side(border_style='thin', color='000000'),
                    right=styles.Side(border_style='thin', color='000000'),
                    top=styles.Side(border_style='thin', color='000000'),
                    bottom=styles.Side(border_style='thin', color='000000'))

        rows = ws.iter_rows(cell_range)
        for row in rows:
            for cell in row:
                cell.border = border
            
            
    subtitle = styles.NamedStyle(name = 'subtitle')
    subtitle.font = styles.Font(name = 'Times New Roman', size = 10, bold=True)
    subtitle.fill = styles.PatternFill(patternType = 'solid', fgColor = 'cccccc')

    ws["A20"] = "EVALUATION DES PERFORMANCES DU MOIS DE  "  + str(today.year)
    ws.merge_cells("A20:I20")
    
    ws["A22"] = "I - CELLULE DE GESTION ET DE SUIVI"
    
    ws["A24"] = "RENDEMENT PAR TYPE D'IMPOT, PAR UNITE DE GESTION ET PAR SOUS SECTEUR D'ACTIVITE (VS " + str(today.year)
    
    i=26
    
    ws["A"+str(i)]="UG"
    ws["A"+str(i+1)]="IMPOT"
    ws.column_dimensions['A'].width = 15
    j='B'
    
    
    ugs = UG.objects.all()
    impots = Impot.objects.all()
    dico = {}
    
    
    for ug in ugs:
        ws.merge_cells(j+""+str(i)+":"+j+""+str(i+1))
        ws[j+""+str(i)] = "UG" + str(ug.ug)
        ws[j+""+str(i)].style = subtitle
        ws.column_dimensions[j].width = 15
        dico[ug.ug]=j
        j=chr(ord(j) + 1) 
    
    ws[j+""+str(i)] = "TOTAUX"
    dico["T_impot"]=j
    
    i=i+2
    j='A'
        
    
    for impot in impots:
        ws[j+""+str(i)] = str(impot.impot)
        ws[j+""+str(i)].style=subtitle
        dico[impot.impot]=i
        i=i+1
        
    ws[j+""+str(i)] = "TOTAUX"
    dico["T_ug"]=i    
    
    
    #bordure plage 
    # plage = "A4:"+str(dico["T_impot"])+str(dico["T_ug"])
    # set_border(ws, plage)
    
    # impots_declare = Impot_Declare.objects.filter(declaration in (Declaration.objects.filter(date_limite__month = today.month-1) &  Declaration.objects.filter(date_limite__year = today.year)))
    impots_declare = Impot_Declare.objects.all()

    for impot_dec in impots_declare:
        ref = str(dico[impot_dec.declaration.contribuable.ug.ug]) + str(dico[impot_dec.impot.impot])
        
        if ws[ref].value == None:
            ws[ref]=0
            
        ws[ref]=ws[ref].value + impot_dec.montant
        
        # ws[dico["T_impot"]+""+dico[impot_dec.impot.impot]]="=SUM("
    
    
    wbl.save(os.path.expanduser("~/Downloads/stats_performance.xlsx"))
    os.popen(os.path.expanduser("~/Downloads/stats_performance.xlsx"))
    
    return redirect('stats2')


def stat_perf_recette(request):
    if today.month == 1:
        impots_amr = Impot_AMR.objects.filter(Q(date__month = 12) & Q(date__year = today.year-1))
        amrs = AMR.objects.filter(Q(date__month = 12) & Q(date__year = today.year-1)).exclude(impots__count=0)
    else:
        impots_amr = Impot_AMR.objects.filter(Q(date__month = today.month) & Q(date__year = today.year))
        amrs = AMR.objects.filter(Q(date__month = today.month) & Q(date__year = today.year)).exclude()

    stat_recette=[]
    for amr in amrs:
        line=[]
        line.append(amr.recette)
        line.append(amr.contribuable.raison_social + " / " + str(amr.num_amr))
        montant = 0
        montant_budg = 0
        for impot in impots_amr:
            if impot.amr == amr:
                montant = montant + impot.montant
                montant_budg = montant_budg + impot.montant_budg
            
        line.append(montant)
        line.append(montant_budg)
        stat_recette.append(line)
                

        
    montantT = Impot_AMR.objects.aggregate(Sum('montant'))
    montantBT = Impot_AMR.objects.aggregate(Sum('montant_budg'))
        
        
        
            
    context={
        "stat_recette" : stat_recette,
        "montantT" : montantT,
        "montantBT" : montantBT,
        "amrs" : amrs,
    }
    return render(request, "soft_cime/stats_perf_recette.html", context)





# AMR
def new_amr(request):
    
    contribuables = contribuable.objects.all()
    message = ""
    success = False
    if request.method == 'POST':
        num_amr = request.POST.get("num_amr")
        contrib = contribuable.objects.get(NIU=request.POST.get("contribuable"))
        personnel = Personnel.objects.get(user = request.user)
        recette = request.POST.get("recette")
        newAMR = AMR.objects.create(num_amr=num_amr,contribuable=contrib, personnel=personnel, recette=recette)        
        newAMR.save()
        message = 'Success'
        success = True
        return redirect('new_impot_amr',newAMR.id)
        
    
    context = {
        'contribuables' : contribuables,
        'message' : message,
        'success' : success,
    }
    return render(request, "soft_cime/amr-new.html", context)

def new_impot_amr(request, idAmr):
    
    impots = Impot.objects.all()
    message = ""
    classmsg = ""
    if request.method == 'POST':
        amr = AMR.objects.get(id=idAmr)
        montant = request.POST.get("montant")
        montant_budg = request.POST.get("recette_budg")
        impot = Impot.objects.get(impot=request.POST.get("impot"))
        
        exist = Impot_AMR.objects.filter(impot=impot) & Impot_AMR.objects.filter(amr=amr)
        
        if len(exist)==0:
            newImpotAMR = Impot_AMR.objects.create(amr=amr,impot=impot, montant=montant,montant_budg = montant_budg)        
            newImpotAMR.save()
            message = 'Success'
            classmsg = "text-success"
        else:
            message = 'Vous essayer de dupliquer une déclaration !!!'
            classmsg = "text-danger"
    
    context = {
        'impots' : impots,
        'message' : message,
        'classmsg' : classmsg,
    }
    return render(request, "soft_cime/amr-new1.html", context)


def liste_amr(request):
    
    amrs = AMR.objects.all().order_by('-date')
    nbamr = AMR.objects.count()
    impots_amr = Impot_AMR.objects.all()

    context = {
        'amrs' : amrs,
        'nbamr' : nbamr,
        'impots_amr' : impots_amr,
    }
    
        
    return render(request, "soft_cime/amr-history.html", context)

def amr_incomplet(request):
    amr_history = AMR.objects.filter().order_by('-date')
    impots_amr = Impot_AMR.objects.all()
    


    context = {
        'amrs' : amr_history,
        'impots_amr' : impots_amr,
    }
    
    
    return render(request, "soft_cime/amr-incomplet.html", context)

def update_amr(request, idAmr):
    contribuables = contribuable.objects.all()
    amr = AMR.objects.get(id=idAmr)
    message = ""
    classmsg=""
    if request.method == 'POST':
        amr.num_amr = request.POST.get("num_amr")
        amr.contribuable = contribuable.objects.get(NIU=request.POST.get("contribuable"))
        amr.recette = request.POST.get("recette")
        amr.save()
        message = 'Success'
        classmsg="text-success"
        return redirect('new_impot_amr',amr.id)
        
        
    
    context = {
        'contribuables' : contribuables,
        'amr':amr,
        'message' : message,
        'classmsg' : classmsg,
    }
    return render(request, "soft_cime/amr-update.html", context)


def detail_amr(request, idAmr):
    amr = AMR.objects.get(id=idAmr)
    impots_amr = Impot_AMR.objects.filter(amr=amr)
    context = {
        'amr' : amr,
        'impots_amr' : impots_amr,
    }
    
    

    return render(request, "soft_cime/amr-detail.html", context)



def excel_amr(request,idAmr):
    
    amr = AMR.objects.get(id=idAmr)
    impots_amr = Impot_AMR.objects.filter(amr=amr)
    context = {
        'amr' : amr,
        'impots_amr' : impots_amr,
    }
    wb=load_workbook("soft_cime/static/doc/detail amr.xlsx")
    ws = wb.active
    
    ws['B3'] = str(amr.num_amr)
    ws['B4'] = str(amr.contribuable.NIU) + " : " + str(amr.contribuable.raison_social)
    ws['B5'] = str(amr.date)
    ws['B6'] = amr.recette
    ws['B7'] = amr.personnel.nom
    
    
    j='A'
    i=11
    for impot in impots_amr:
        ws["A"+str(i)]=impot.impot.impot
        ws["B"+str(i)]=impot.montant
        ws["C"+str(i)]=impot.montant_budg
        i = i+1
        # j=chr(ord(j) + 1)

    ws.oddFooter.center.text ="Powered by Le Gestionnaire \n" + str(datetime.today())
    wb.save(os.path.expanduser("~/Downloads/AMR " + str(amr.num_amr) + ".xlsx"))
    os.popen(os.path.expanduser("~/Downloads/AMR " + str(amr.num_amr) + ".xlsx"))
    
    return redirect("detail_amr", idAmr)


class GeneratePdf(View):
    def get(self, request, *args, **kwargs):
        ugs = UG.objects.all()
        nbContrib = contribuable.objects.count()
        regime_impots = Regime_impot.objects.all()
        departements = Departement.objects.all()
        context = {
            "ugs" : ugs,
            "nbContrib" :nbContrib,
            "regime_impots" : regime_impots,
            "departements" : departements,
        }
        pdf = render_to_pdf('soft_cime/stats1.html', context)
        
        return HttpResponse(pdf, content_type='application/pdf')
    
    
    