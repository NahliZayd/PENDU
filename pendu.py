# Importation de modules
import collections
import os
import re  # regex
import threading
from random import *
from time import sleep, time

from faker import Faker

# Variables avec leurs valeurs par defaut
niveau = "Facile"  # Niveau de difficulté du jeu
theme = "Indifferent"  # Thème du jeu
mode = "Normal"  # Mode de jeu choisi
langue = "fr_Fr"  # Langue utilisée pour le jeu

# Listes
niveaux = ["Facile", "Normal", "Difficile"]  # Liste des niveaux de difficulté possibles
themes = ["Indifferent", "Pays", "Metiers"]  # Liste des thèmes possibles pour le jeu
modes = ["Normal", "Chrono", "VS", "2joueurs"]  # Liste des modes de jeu possibles
langues = {'Fr': 'fr_FR', 'En': 'en_US', 'Es': 'es_ES', 'Pt': 'pt_PT', 'It': 'it_IT', 'De': 'de_DE',
           'Pl': 'pl_PL'}
# Dictionnaire des langues disponibles pour le jeu

# Variables pour le mode Chrono
temps_ecoule = False  # Variable indiquant si le temps est écoulé ou non
temps_debut = 0  # Variable stockant le temps de début du jeu

# Génère un mot aléatoire d'une longueur maximale de longueur_max
# Prend en argument : Une instance de Faker , la longueur minimale et maximale du mot à generer
# Retourne : La fonction retourne un mot généré aléatoirement apres avoir supprimé les caractères interdit
# Effet de bord : Aucun
def generer_mot(faker, longueur_min, longueur_max):
    # On initialise la variable mot à "a" afin d'entrer dans la boucle.
    mot = "a"
    # On boucle tant que la longueur du mot n'est pas comprise entre longueur_min et longueur_max inclus.
    while len(mot) < longueur_min or len(mot) > longueur_max:
        # Si le thème est "Metiers", on génère un métier aléatoire à l'aide de faker.job().
        if theme == "Metiers":
            mot = faker.job()
        # Si le thème est "Pays", on génère un pays aléatoire à l'aide de faker.country().
        elif theme == "Pays":
            mot = faker.country()
        # Si le thème n'est ni "Metiers" ni "Pays", on génère un mot aléatoire à l'aide de faker.word().
        else:
            mot = faker.word()
    # On retourne le mot généré en enlevant les caractères interdits à l'aide de la fonction enlever_char_interdit.
    return enlever_char_interdit(mot.lower())


# Ne prend aucun argument mais utilise des variables globales (niveau et langue)
# Ne retourne rien
# Effet de bord : Ecriture de la liste des 1000 mots générés dans un fichier "mots_gen.txt" à la racine du dossier de travail. Si le fichier existe déjà, son contenu sera écrasé.
def generer_liste_mots():
    longueur_min = 3  # Longueur minimale des mots générés
    longueur_max = 5  # Longueur maximale des mots générés
    if niveau == "Normal":  # Si le niveau est Normal, on ajuste les longueurs min/max des mots
        longueur_min = 6
        longueur_max = 8
    elif niveau == "Difficile":  # Si le niveau est Difficile, on ajuste les longueurs min/max des mots
        longueur_min = 9
        longueur_max = 15
    fake = Faker(langue)  # On utilise la bibliothèque Faker pour générer des mots aléatoires dans la langue choisie
    liste_mots = []  # On initialise une liste vide pour stocker les mots générés
    for i in range(10000):  # On génère 10000 mots aléatoires
        mot = generer_mot(fake, longueur_min,longueur_max)  # On génère un mot avec la longueur minimale et maximale définies
        liste_mots.append(mot)  # On ajoute le mot à la liste
    liste_mots = sample(liste_mots, 1000)  # On sélectionne au hasard 1000 mots parmi la liste générée

    # Écrit la liste de mots dans le fichier, chaque mot terminé par "\n", ce code ecrase le contenu de la ligne avant d'ecrire dedans
    with open("mots_gen.txt", "w") as f:  # On ouvre le fichier "mots_gen.txt" en mode écriture
        for mot in liste_mots:  # Pour chaque mot sélectionné
            f.write(mot.upper() + "\n")  # On écrit le mot en majuscules suivi d'un retour à la ligne


    # Efface le contenu du fichier
    with open("mots_gen.txt", "w") as f:
        f.write("")

    # Écrit la liste de mots dans le fichier, chaque mot terminé par "\n"
    with open("mots_gen.txt", "w") as f:
        for mot in liste_mots:
            f.write(mot.upper() + "\n")



# Prend en argument le mot à modifier
# Retourne le mot modifié
# Effet de bord : Aucun 
def enlever_char_interdit(mot):
    # Définition d'un dictionnaire des caractères interdits et leurs équivalents
    char_interdits = {'à': 'a', 'á': 'a', 'â': 'a', 'ä': 'a', 'è': 'e', 'é': 'e', 'ê': 'e', 'ë': 'e', 'î': 'i',
                      'ï': 'i', 'ô': 'o', 'ö': 'o', 'ù': 'u', 'û': 'u', 'ü': 'u', 'ç': 'c', '\'': ' ',
                      '(': '', ')': ''}
    for char, lettre in char_interdits.items():  # Pour chaque caractère interdit et son équivalent dans le dictionnaire
        mot = mot.replace(char, lettre)  # On remplace le caractère interdit par son équivalent dans le mot
    return mot.upper()  # On retourne le mot modifié

# Fonction qui recupere les mots possible
# Prend en argument le nom du fichier contenant les mots a importer
# Retourne le contenu du fichier
# Effet de bord : Ouverture et fermeture du fichier , suppression des caracteres "\n" a la fin de chaque ligne
def importer_mots(nom_fichier):
    # On vérifie que le nom de fichier contient bien l'extension ".txt"
    if ".txt" not in nom_fichier:
        nom_fichier = nom_fichier + ".txt"
    # On ouvre le fichier en mode lecture
    fichier = open(nom_fichier, 'r')
    # On lit toutes les lignes du fichier et on les stocke dans une liste en supprimant les "\n" à la fin
    lignes_fichier = fichier.readlines()
    contenu_du_fichier = []
    for mot in lignes_fichier:
        mot = mot.strip().replace(" ","").upper()  # On supprime les espaces et on met le mot en majuscules
        if len(mot) < 3:  # On exclut les mots de moins de 3 lettres
            continue
        contenu_du_fichier.append(mot)  # On ajoute le mot à la liste
    fichier.close()  # On ferme le fichier
    return contenu_du_fichier  # On retourne la liste des mots importés

# Prend en argument la liste de mots possible
# Retourne un mot choisi aleatoirement
# Effet de bord : Aucun
def choisir_mot_alea(mots):
    # On utilise la fonction "choice" du module "random" pour choisir un élément aléatoire de la liste "mots"
    mot = choice(mots)
    return mot  # On retourne le mot choisi
    

# Prend en argument le mot a deviné , et le caractère utilisé pour représenter les lettres non découvertes du mot mystère
# Retourne le mort partiellement decouvert sous forme d'une liste
# Effet de bord : Aucun
def initialiser_mot_part_decouv(mot_myst, car_subst="-"):
    lettres = [*mot_myst]  # On transforme le mot mystère en une liste de ses lettres
    premier_lettre = lettres[0]  # On sauvegarde la première lettre du mot mystère
    derniere_lettre = lettres[-1]  # On sauvegarde la dernière lettre du mot mystère
    for i in range(len(lettres)):
        lettres[i] = car_subst  # On remplace chaque lettre par le caractère de substitution spécifié

    if niveau != "Difficile":
        lettres[0] = premier_lettre  # Si le niveau n'est pas "Difficile", on découvre la première lettre
    if niveau == "Facile":
        lettres[-1] = derniere_lettre  # Si le niveau est "Facile", on découvre la dernière lettre
        
    return lettres  # On retourne la liste de lettres partiellement découvertes

# Prend en argument le nombre d'erreurs comises , la nombre d'erreurs maximal autorisé 
# Ne retourne rien
# Effet de bord : Affichage dans la console de la potence avec le nombre d'erreurs correspondant.
def afficher_potence_texte(nb_err, nb_err_max):
    # Création de la chaîne de caractères avec le bon nombre de points d'exclamation
    perdu = "PERDU" + ("!" * (nb_err_max - 5)) + "!"
    # Initialisation de la chaîne de caractères à afficher
    affichage = ""
    # Boucle sur nb_err_max toutes les lettres de la chaîne
    for i in range(nb_err_max):
        # Si on a atteint le nombre d'erreurs, on affiche les caractères correspondantes
        if i < nb_err:
            affichage += perdu[i]
        # Sinon, on affiche des tirets
        else:
            affichage += "-"
    # Affichage de la chaîne de caractères correspondante au nombre d'erreurs suivi d'un point d'exclamation
    print(affichage + "!")

# Cette fonction calcule la fréquence d'apparition de chaque lettre dans un fichier texte
# Prend en argument le nom du fichier contenant les mots possible 
# Retourne un dictionniaire contenant les lettres et leur frequence
# Effets de bord: Aucun
def dico_frequence(nom_fichier):
    # On importe tous les mots du fichier
    mots = importer_mots(nom_fichier)

    # On crée un dictionnaire pour stocker la fréquence de chaque lettre
    dict_frequence = dict()

    # Pour chaque mot dans le fichier
    for mot in mots:
        # Pour chaque lettre dans le mot
        for lettre in mot:
            # On ignore les caractères de fin de ligne '\n'
            if lettre == '\n':
                continue
            # Si la lettre n'est pas encore présente dans le dictionnaire, on l'ajoute avec une fréquence de 0
            if lettre.upper() not in dict_frequence:
                dict_frequence[lettre.upper()] = 0
            # On incrémente la fréquence de la lettre
            dict_frequence[lettre.upper()] = (dict_frequence[lettre.upper()]) + 1

    # On retourne le dictionnaire des fréquences
    return dict_frequence

# Cette fonction retourne la lettre la plus fréquente dans un dictionnaire de fréquences
# Prend en argument un dictionnaire de frequence
# Retourne la lettre la plus frequente du dictionnaire de frequence fourni
# Effet de bord : Aucun
def lettre_la_plus_frequente(dico):
    # On trie le dictionnaire par fréquence décroissante
    sorted_dico = sorted(dico.items(), key=lambda x: x[1], reverse=True)
    # On retourne la clé de la première entrée triée (i.e. la lettre la plus fréquente)
    return list(collections.OrderedDict(sorted_dico).keys())[0]


# Cette fonction crée une liste des lettres les plus fréquentes dans un fichier
# Prends en argument le nom du fichier contenant les mots possible
# Retourne une liste de lettres a proposée classé par frequence d'apparition
# Effet de bords : Aucun
def fabrique_liste_freq(nom_fichier):
    # On calcule le dictionnaire de fréquences
    dico_freq = dico_frequence(nom_fichier)

    # On crée une liste pour stocker les lettres les plus fréquentes
    liste_freq = []

    # Tant que le dictionnaire de fréquences n'est pas vide
    while dico_freq:
        # On trouve la lettre la plus fréquente
        lettre = lettre_la_plus_frequente(dico_freq)
        # On ajoute cette lettre à la liste des lettres les plus fréquentes
        liste_freq.append(lettre)
        # On supprime cette lettre du dictionnaire de fréquences
        del dico_freq[lettre]

    # On retourne la liste des lettres les plus fréquentes
    return liste_freq

# Fabrique la liste de lettres a proposé pour le joueur robot en se basant sur la strategie de probabilité
# Prend en argument le nom du fichier contenant les mots et la taille du mot mystere
# Renvoie la liste crée
# Effets de bord : Aucun
def fabrique_liste_prob(nom_fichier, taille_mot):
    # Importation des mots depuis le fichier
    mots = importer_mots(nom_fichier)

    # Initialisation d'un dictionnaire de fréquence des lettres et du nombre total de lettres
    freq = collections.defaultdict(int)
    total = 0

    # Calcule de la fréquence de chaque lettre dans les mots de la taille spécifiée
    for mot in mots:
        if len(mot) == taille_mot:
            for lettre in mot:
                freq[lettre] += 1
                total += 1

    # Calcul de la probabilité de chaque lettre en divisant sa fréquence par le nombre total de lettres
    prob = {}
    for lettre, freq_lettre in freq.items():
        prob[lettre] = freq_lettre / total

    # Tri des lettres par ordre décroissant de leur probabilité d'apparition
    lettres_triees = sorted(prob, key=prob.get, reverse=True)

    return lettres_triees

# Fonction qui recupere tout les mots ressemblant au mot mystere 
# Prend en argument le mot partiellement decouvert et le caractère utilisé pour représenter les lettres non découvertes
# Retourne une liste de mots correpondant au mot mystere
# Effets de bord : Aucun
def trouver_mots(lmot_decouv,car_subst="-"):
    # On crée une expression régulière pour trouver les mots qui correspondent à un certain modèle
    modele_regex = re.compile(lmot_decouv.replace(car_subst, '.'))
    # On importe la liste de mots
    mots = importer_mots("mots_gen")
    # On crée une liste de mots qui correspondent au modèle donné
    mots_correspondants = [mot for mot in mots if modele_regex.match(mot)]
    return mots_correspondants

# Fonction qui determine la proposition pour le joueur robot en se basant sur la strategie de recherche de mot
# Prend en argument le mot partiellement decouvert sous forme d'une liste , la liste de lettres
# deja proposées et le et le caractère utilisé pour représenter les lettres non découvertes
# Retourne la lettre a proposé 
# Effets de bord : Aucun
def lettre_suivante(lmot_decouv, deja_dit,car_subst="-"):
    # On cherche tous les mots possibles qui correspondent à la partie du mot découverte jusqu'à présent
    mots_possibles = trouver_mots(''.join(lmot_decouv))
    # On crée un dictionnaire qui contient toutes les lettres possibles qui n'ont pas encore été devinées et le nombre de fois qu'elles apparaissent dans les mots possibles
    lettres_deja_devinees = deja_dit
    lettres_possibles = collections.Counter()
    for mot in mots_possibles:
        for lettre in mot:
            if lettre not in lettres_deja_devinees:
                lettres_possibles[lettre] += 1
    # On trie les lettres possibles en ordre décroissant selon leur fréquence d'apparition dans les mots possibles
    prochaines_lettres = lettres_possibles.most_common()
    # Si la liste de prochaines lettres est vide, cela signifie que toutes les lettres possibles ont déjà été devinées. Dans ce cas, on choisit une lettre aléatoire dans l'alphabet
    prochaine_lettre = (fabrique_liste_alphabet_alea())[0]
    if prochaines_lettres:
        prochaine_lettre = prochaines_lettres[0][0]
    # On retourne la prochaine lettre à deviner
    return prochaine_lettre


# Ne prend pas d'arguments.
# Ne renvoie rien.
# Effet de bord : Modifie les variables globales niveau, theme, mode et langue en fonction des paramètres récupérés.
def charger_configuration():
    global niveau
    global theme
    global mode
    global langue

    # Si le fichier "config.txt" n'existe pas, la fonction sauvegarder_configuration est appelée pour le créer.
    if not os.path.exists("config.txt"):
        sauvegarder_configuration()

    fichier = open("config.txt", 'r')  # ouverture du fichier config.txt en mode lecture
    config = fichier.readlines()  # lecture de toutes les lignes du fichier
    niveau = config[0].split("=")[1].split()[0]  # récupère la valeur de niveau à partir de la première ligne
    theme = config[1].split("=")[1].split()[0]  # récupère la valeur de theme à partir de la deuxième ligne
    mode = config[2].split("=")[1].split()[0]  # récupère la valeur de mode à partir de la troisième ligne
    langue = config[3].split("=")[1].split()[0]  # récupère la valeur de langue à partir de la quatrième ligne


# Les paramètres niveau, theme, mode et langue sont récupérés depuis les variables globales.
# Ne prend pas d'arguments.
# Ne renvoie rien.
# Effet de bord : Écrit les paramètres de configuration dans le fichier config.txt.
def sauvegarder_configuration():
    # Écrit la liste de mots dans le fichier config.txt, écrase le contenu existant
    with open("config.txt", "w") as f:
        f.write(f"niveau={niveau}"
                f"\ntheme={theme}"
                f"\nmode={mode}"
                f"\nlangue={langue}"
                f"\n")
                
# Ne prend pas d'arguments.
# Ne renvoie rien.
# Effet de bord : Modifie les variables globales utilisées dans le programme en fonction des paramètres récupérés.
def appliquer_configuration():
    # appelle la fonction charger_configuration pour récupérer les valeurs des paramètres
    charger_configuration()
    # appelle la fonction generer_liste_mots pour générer la liste de mots en fonction des paramètres récupérés
    generer_liste_mots()

# methode pour demander la proposition
def demander_proposition(deja_dit):
    # On init la valeur à 1 , 1 n'est pas une lettre , on rentre donc dans le while
    proposition = "1"
    while proposition in deja_dit or not proposition.isalpha():
        # On demande une lettre qu'on mets en majuscule afin d'eviter de verifier si la lettre est en majuscule
        proposition = input("Entrer une lettre : ").upper()
        return proposition


# La fonction modifie la liste lmot_decouv en remplaçant les caractères de substitution par la lettre proposée si celle-ci est présente dans mot_myst
# Prend en argument la lettre a decouvrir , le mot mystere , et le mot partiellement decouvert
# Si la lettre a été remplacée au moins une fois, la fonction retourne True, sinon elle retourne False
# Effet de bord : modifie la variable lmot_decouv qui correspond au mot partiellement decouvert
def decouvrir_lettre(lettre, mot_myst, lmot_decouv):
    # Definition d'un boolean permettant de vérifier si la lettre à été remplacé
    remplace = False
    # Vérifier si la lettre proposée est dans le mot mystère
    if lettre in mot_myst:
        # Parcourir le mot pour "decouvrir" toute les fois ou la lettre proposé apparait
        for index, c in enumerate(mot_myst):
            if c == lettre and lmot_decouv[index] != lettre:
                lmot_decouv[index] = lettre
                # Renvoyer True si la lettre a été trouvée et remplacée dans le mot decouvert
                remplace = True
    # Renvoyer False si la lettre n'a pas été trouvée et remplacée dans le mot
    return remplace

# Methode permettant d'afficher une liste sur une seule ligne
# mais egalement d'afficher le mot decouvert de maniere esthethique
# Prend en argument : une liste de caractères à afficher et le caractère de fin de ligne à utiliser
# Ne retourne rien
# Effets de bord: Affiche la liste de caractères avec le caractère de fin de ligne spécifié.
def afficher_texte(liste, end=""):
    for c in liste:
        print(c, end=end)
    print("")


# Prend en argument le mot mystère que le joueur doit deviner,le nombre maximum d'erreurs autorisé et  
# le caractère utilisé pour représenter les lettres non découvertes
# Retourne le resultat de la partie , True si le joueur gagne et False si il perd
# Effets de bord : Affichage dans la console du déroulement de la partie et des informations relatives à la progression du joueur.
def partie_humain(mot_myst, nb_err_max, car_subst="-"):
    # Initialisation du mot partiellement découvert
    lmot_decouv = initialiser_mot_part_decouv(mot_myst, car_subst)
    # Initialisation du nombre d'erreurs à 0
    nb_err = 0
    # Initialisation de la liste des lettres déjà proposées
    deja_dit = []
    # Boucle de jeu
    while mot_myst != ''.join(lmot_decouv) and nb_err < nb_err_max:
        effacer_console()
        # Affichage du mot partiellement découvert
        print("\nMot actuel :", end="")
        afficher_texte(lmot_decouv)
        # Affichage de la liste des lettres déjà proposées s'il y en a
        if deja_dit:
            print("Lettres proposees : ", end="")
        afficher_texte(deja_dit, " ")
        # Demande de proposition de lettre
        lettre = demander_proposition(deja_dit)
        deja_dit.append(lettre)
        # Découverte de la lettre dans le mot mystère
        if not decouvrir_lettre(lettre, mot_myst, lmot_decouv):
            nb_err += 1
            print("Erreur n°", nb_err)
        else :
            print("Lettre presente")
        # Affichage de la potence  si le nombre d'erreurs est supérieur à 0
        if nb_err > 0:
            print("")
            afficher_potence_texte(nb_err, nb_err_max)
            print("")
        sleep(1)

    # Retourne True si le nombre d'erreurs est inférieur à nb_err_max, False sinon
    return nb_err != nb_err_max

# La fonction partie_humain_alea choisit un mot aleatoire et lance une partie avec un joueur humain
# Prend en argument le nom du fichier contenant les mots possibles , le nombre maximal d'erreurs autorisées
# Retourne : le resultat de la partie 
# Effet de bords : Aucun
def partie_humain_alea(fichier, nbErrMax):
    # Importation des mots du fichier
    mots = importer_mots(fichier)
    # Choix d'un mot aléatoire parmi la liste de mots
    mot_myst = choisir_mot_alea(mots)
    # Lancement de la partie avec le mot choisi aléatoirement et le nombre maximum d'erreurs
    return partie_humain(mot_myst, nbErrMax, "-")

#Prend en argument le type de partie ("humain" ou "auto").
#Ne renvoie rien.
#Effet de bord : Lance une partie en fonction du type de partie choisi et du mode de jeu paramétré.
def lancer_partie(type_partie):
    effacer_console()
    # Importe la liste de mots depuis le fichier 'mots_gen' et choisit un mot aléatoirement
    mots = importer_mots("mots_gen")
    mot_myst = choisir_mot_alea(mots)

    # Obtient le nombre d'erreurs maximum en fonction du niveau choisi
    nb_err_max = obtenir_nb_err_max()

    # Si la partie est automatique, choix de la stratégie de jeu automatique et lancement de la partie
    if type_partie == "auto":
        liste_lettres = choix_strategie(mot_myst)
        nb_err = partie_auto(mot_myst, liste_lettres, True, True)
        print("L'ordinateur a trouvé le mot en faisant " + str(nb_err) + " erreur(s)!")
    # Sinon, lancement de la partie en fonction du mode choisi
    else:
        if mode == "Chrono":
            # Si le mode est Chrono, lance une partie chronométrée
            partie_humain_chrono(mots, mot_myst)
        elif mode == "Vs":
            # Si le mode est VS, lance une partie contre l'ordinateur
            if partie_humain_vs_auto(mot_myst, "-"):
                print("Le joueur humain a gagné en devinant le mot :", mot_myst)
            else:
                print("Le joueur robot a gagné en devinant le mot :", mot_myst)
        elif mode == "2joueurs":
            # Si le mode est 2joueurs, lance une partie à deux joueurs
            if partie_humain_deux_joueurs(mot_myst, "-"):
                print("Le joueur 1 a gagné en devinant le mot:", mot_myst)
            else:
                print("Le joueur 2 a gagné en devinant le mot:", mot_myst)
        else:
            # Sinon, lance une partie en mode solo
            if partie_humain(mot_myst, nb_err_max, "-"):
                print("GAGNE ! Vous avez trouvé le mot :", mot_myst)
            else:
                print("PERDU ! Le mot était :", mot_myst)
    print("Appuyez sur Entrée pour continuer...")
    input()

# Prend une liste de mots en entrée.
# Ne renvoie rien.
# Effet de bord : Compare les performances de différentes stratégies pour deviner les mots de la liste donnée.
def comparaison_strat(liste_mots):
    effacer_console()

    # Demande à l'utilisateur s'il veut afficher les étapes
    afficher = input("Afficher les etapes ? (y/n) ").upper() == "Y"

    # Demande à l'utilisateur le nombre de simulation à effectuer
    n_parties_texte = input("Combien de simulation doit on effectuer par strategie ? (1-100)")

    # Si n_parties_texte est un nombre entre 1 et 100 inclus, convertit sa valeur en entier, sinon, assigne 1 par défaut
    n_parties = int(n_parties_texte) if n_parties_texte.isnumeric() and 0 < int(n_parties_texte) <= 100 else 10

    # Comparaison des différentes stratégies
    liste_strategies = ["Alphabétique", "Aléatoire", "Fréquentielle", "Probabiliste", "Recherche de mots"]
    perf = {}  # Dictionnaire pour stocker les résultats de chaque stratégie
    compteur_progression = 0
    for strategie in liste_strategies:
        if afficher:
            print(f"\n\nStratégie: {strategie}")
        if strategie == "Alphabétique":
            liste_lettres = fabrique_liste_alphabet()
        elif strategie == "Fréquentielle":
            liste_lettres = fabrique_liste_freq("mots_gen")
        elif strategie == "Probabiliste" or strategie == "Aléatoire":
            liste_lettres = []
        else:
            liste_lettres = ["recherche"]

        nb_erreurs_total = 0
        for i in range(n_parties):
            progression = round((compteur_progression / (len(liste_strategies) * n_parties)) * 100)
            modifier_titre("Comparaison des stratégies : " + str(progression) + "%")
            mot_myst = liste_mots[i]
            if strategie == "Probabiliste":
                liste_lettres = fabrique_liste_prob("mots_gen", len(mot_myst))
            elif strategie == "Aléatoire":
                liste_lettres = fabrique_liste_alphabet_alea()

            nb_err = partie_auto(mot_myst, liste_lettres, afficher, False)
            nb_erreurs_total += nb_err
            compteur_progression += 1
        effacer_console()
        moy_erreurs = nb_erreurs_total / n_parties
        perf[strategie] = moy_erreurs  # Stocke le résultat moyen de chaque stratégie dans le dictionnaire

    # Affiche les résultats de chaque stratégie
    for strat, moy_errs in perf.items():
        print(f"Résultat global de la stratégie {strat}: en moyenne, {moy_errs} erreurs par partie sur {n_parties} partie(s).")
    print("")
    modifier_titre("Jeu du Pendu par Nahli Zayd et Layada Nasrallah")
    print("Appuyez sur Entrée pour continuer...")
    input()

# Effet de bord : Affiche le menu principal du jeu avec les options disponibles pour l'utilisateur.
# Ne prend pas d'argument en entrée.
# Ne renvoie rien.
# Elle demande à l'utilisateur de saisir un choix parmi les options affichées et appelle la fonction correspondante.
# La fonction est récursive
def afficher_menu():
    effacer_console()
    print("Menu principal :")
    print("1. Lancer une partie manuelle (joueur humain)")
    print("2. Lancer une partie automatique (ordinateur)")
    print("3. Comparer les strategies")
    print("4. Parametres")
    print("5. Quitter")

    # Demande à l'utilisateur de saisir son choix et l'enregistre dans la variable choix
    choix = input("Votre choix (1-5) : ")

    # Condition qui vérifie le choix de l'utilisateur et appelle la fonction correspondante
    if choix == "1":
        generer_liste_mots()
        lancer_partie("humain")
    elif choix == "2":
        generer_liste_mots()
        lancer_partie("auto")
    elif choix == "3":
        generer_liste_mots()
        comparaison_strat(importer_mots("mots_gen"))
    elif choix == "4":
        afficher_parametre()
    elif choix == "5":
        print("Au revoir !")
        sleep(1)
        effacer_console()
        quit()
    else:
        print("Choix invalide. Veuillez réessayer.")

    # Rappelle la fonction pour afficher de nouveau le menu principal
    afficher_menu()

    


# Prend aucun argument.
# Ne renvoie rien.
# Effet de bord : Permet à l'utilisateur de modifier les paramètres du jeu (niveau, thème, mode et langue).
# La fonction est récursive
def afficher_parametre():
    effacer_console()
    # On utilise les variables globales pour stocker les paramètres
    global niveau
    global theme
    global mode
    global langue

    # Affichage du menu des paramètres
    print("Menu des parametres :")
    print("1. Changer la difficulté (Actuellement : " + niveau + ")")
    print("2. Changer le theme (Actuellement : " + theme + ")")
    print("3. Changer le mode (Actuellement : " + mode + ")")
    print("4. Changer la langue (Actuellement : " + langue + ")")
    print("5. Quitter")

    # L'utilisateur choisit une option
    choix = input("Votre choix (1-5) : ")

    # Traitement de l'option choisie
    if choix == "1":
        effacer_console()
        # Affichage des niveaux et demande de saisie d'un nouveau niveau
        print("Difficulté possible : ", end=" ")
        afficher_texte(niveaux, " , ")
        tempNiveau = input("Entrez la nouvelle difficulté : ")
        # Vérification que le niveau saisi est valide, sinon on conserve l'ancien niveau
        if tempNiveau.lower() in [niveau.lower() for niveau in niveaux]:
            niveau = tempNiveau.capitalize()
        else:
            print("Le niveau entré est incorrect , la modification n'est donc pas prise en compte ! ")
    elif choix == "2":
        effacer_console()
        print("Thème possible : ", end=" ")
        # Affichage des thèmes et demande de saisie d'un nouveau thème
        afficher_texte(themes, " , ")
        tempTheme = input("Entrez le nouveau thème : ")
        # Vérification que le thème saisi est valide, sinon on conserve l'ancien thème
        if tempTheme.lower() in [theme.lower() for theme in themes]:
            theme = tempTheme.capitalize()
        else:
            print("Le thème entré est incorrect , la modification n'est donc pas prise en compte ! ")
    elif choix == "3":
        effacer_console()
        print("Mode de jeu possible : ", end=" ")
        # Affichage des modes et demande de saisie d'un nouveau mode
        afficher_texte(modes, " , ")
        tempMode = input("Entrez le nouveau mode : ")
        # Vérification que le mode saisi est valide, sinon on conserve l'ancien mode
        if tempMode.lower() in [mode.lower() for mode in modes]:
            mode = tempMode.capitalize()
        else:
            print("Le mode entré est incorrect , la modification n'est donc pas prise en compte ! ")
    elif choix == "4":
        effacer_console()
        print("Langue possible : ", end=" ")
        # Affichage des langues et demande de saisie d'une nouvelle langue
        afficher_texte(langues.keys(), " , ")
        tempLangue = input("Entrez la nouvelle langue : ")
        # Vérification que la langue saisie est valide, sinon on conserve l'ancienne langue
        if tempLangue.lower() in [langue.lower() for langue in langues]:
            langue = langues.get(tempLangue.capitalize())
        else:
            print("La langue entrée est incorrect , la modification n'est donc pas prise en compte ! ")
    elif choix == "5":
        # Quitter les paramètres en sauvegardant et appliquant la configuration, puis en affichant le menu principal
        print("Au revoir !")
        sauvegarder_configuration()
        appliquer_configuration()
        sleep(1)
        effacer_console()
        afficher_menu()
    else:
        # Option invalide
        print("Choix invalide. Veuillez réessayer.")

    # On rappelle la fonction pour afficher à nouveau le menu des paramètres
    sleep(1)
    afficher_parametre()

# La fonction fabrique_liste_alphabet retourne une liste contenant les lettres de l'alphabet, en ordre alphabétique.
# Ne prend aucun argument
# Retourne : La liste contenant les lettres de l'alphabet dans l'ordre alphabétique
# Effets de bord : Aucun
def fabrique_liste_alphabet():
    # Initialisation de la liste vide pour contenir les lettres de l'alphabet
    alphabet = []
    # Parcourt les lettres de A à Z en utilisant leur code ASCII
    for i in range(ord('A'), ord('Z') + 1):
        # Ajout de la lettre correspondante à la liste
        alphabet.append(chr(i))
    # Retourne la liste complète de l'alphabet
    return alphabet

# La fonction fabrique_liste_alphabet_alea retourne une liste contenant les lettres de l'alphabet, en ordre aléatoire.
# Ne prend aucun argument 
# Retourne : L'alphabet melangées aleatoirement                                                                                                                            
# Effets de bord : Aucun  
def fabrique_liste_alphabet_alea():
    # Création d'une liste contenant les lettres de l'alphabet en ordre alphabétique
    alphabet_alea = fabrique_liste_alphabet()
    # Mélange aléatoire de la liste
    shuffle(alphabet_alea)
    # Retourne la liste mélangée aléatoirement
    return alphabet_alea


# Methode qui efface la console pour rendre le jeu plus jolie
# Ne prends aucun argument
# Ne retourne rien 
# Effet de bord : efface la console
def effacer_console():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


# Ne prends aucun argument
# Retourne le nombre maximum d'erreurs autorisées en fonction de la valeur de la variable globale niveau
# Effet de bord : aucun
def obtenir_nb_err_max():
    if niveau == "Normal":
        return 12
    elif niveau == "Difficile":
        return 8
    else:
        return 16

    
# Modifie le titre de la fenêtre de la console avec le titre spécifié.
# Prends en arguments : Le titre à afficher dans le titre de la fenêtre de la console.
# Effets de bord : Modifie le titre de la fenetre
# Ne renvoie rien.
def modifier_titre(titre):
    os.system("title " + titre)


# Cette fonction représente la boucle de jeu automatique
# Prends en argument : une liste de mots à deviner , le mot mystere , un boolean affichage et un boolean pause 
# Effets de bord:
# -La fonction affiche le mot partiellement découvert, la liste des lettres déjà proposées et demande une proposition
# de lettre au joueur robot.
# - Si la proposition de lettre est correcte, la fonction affiche le nouveau mot partiellement découvert.
# - Si le mot mystère a été entièrement découvert, la fonction affiche le mot mystère trouvé et passe au mot suivant.
# - Si pause est vrai alors on attends que le joueur appuie sur une touche avant chaque tour
# Retourne le nombre d'erreurs
def partie_auto(mot_myst, liste_lettres, affichage=True, pause=False):
    # Initialisation du mot partiellement découvert
    lmot_decouv = initialiser_mot_part_decouv(mot_myst, "-")
    # Initialisation du compteur de progression dans la liste
    indexActuel = 0
    # Initialisation du nombre d'erreurs à 0
    nb_err = 0
    # Initialisation de la liste des lettres déjà proposées
    deja_dit = []
    # Boucle de jeu
    while mot_myst != ''.join(lmot_decouv):
        effacer_console()
        # Affichage de la liste des lettres déjà proposées s'il y en a
        if deja_dit:
            if affichage:
                print("Lettres proposees : ", end="")
                afficher_texte(deja_dit, " ")
        # Demande de proposition de lettre
        if indexActuel < 26:
            if liste_lettres[0] == "recherche":
                lettre = lettre_suivante(lmot_decouv, deja_dit,"-")
            else:
                lettre = liste_lettres[indexActuel]
        # Vérification si la lettre a déjà été proposée
        deja_dit.append(lettre)
        # Découverte de la lettre dans le mot mystère
        if not decouvrir_lettre(lettre, mot_myst, lmot_decouv):
            nb_err += 1
            if affichage:
                print("\nErreur n°", nb_err)
        indexActuel += 1
        # Affichage du mot partiellement découvert
        if affichage:
            print("\nMot actuel :", end="")
            afficher_texte(lmot_decouv)
        # pause
        if pause:
            print("Appuyez sur Entrée pour continuer...")
            input()
            effacer_console()
    return nb_err

# Fonction qui permet de jouer au jeu du pendu avec un joueur humain et un joueur robot.
# Elle prends en arguments : le mot mystère à deviner et le caractère de substitution pour remplacer
# les lettres non devinées
# Effets de bord : Affiche à l'écran le déroulement du jeu , modifie la variable tour qui est le nombre
# de tours joués
# Retourne : True si le joueur humain a gagné, False sinon (joueur robot a gagné)
def partie_humain_vs_auto(mot_myst, car_subst="-"):
    liste_lettres = choix_strategie(mot_myst)  # Obtient la liste des lettres proposées par le joueur robot
    # Initialisation du mot partiellement découvert
    lmot_decouv = initialiser_mot_part_decouv(mot_myst, car_subst)
    # Initialisation de la liste des lettres déjà proposées
    deja_dit = []
    tour = 0

    # Boucle de jeu
    while mot_myst != ''.join(lmot_decouv):  # Tant que le mot mystère n'est pas découvert
        effacer_console()
        # Affichage du mot partiellement découvert
        print("\nMot actuel :", end="")
        afficher_texte(lmot_decouv)
        # Affichage de la liste des lettres déjà proposées s'il y en a
        if deja_dit:
            print("Lettres proposees : ", end="")
            afficher_texte(deja_dit, " ")
        # Demande de proposition de lettre
        if tour % 2 == 0:  # Si c'est le tour du joueur humain
            print("C'est au tour du joueur humain !")
            lettre = demander_proposition(deja_dit)  # Le joueur humain propose une lettre
        else:  # Sinon c'est le tour du joueur robot
            print("C'est au tour du joueur robot !")
            if liste_lettres[0] == "recherche":  # Si le joueur robot utilise la strategie de recherche de mots
                lettre = lettre_suivante(lmot_decouv, deja_dit,car_subst)
            else:  # Sinon, le joueur robot a une lettre en stock
                lettre = liste_lettres[0]  # Le joueur robot propose la première lettre de sa liste
        print("Le joueur a proposé : ", lettre)

        deja_dit.append(lettre)  # Ajout de la lettre proposée à la liste des lettres déjà proposées
        if lettre in liste_lettres and not liste_lettres[0] == "recherche":
            liste_lettres.remove(lettre)  # Retrait de la lettre proposée de la liste des lettres du robots

        decouvrir_lettre(lettre, mot_myst, lmot_decouv)  # Découverte de la lettre dans le mot mystère
        tour += 1  # Passage au tour suivant
        sleep(2)  # Pause de 2 secondes entre les tours pour rendre le jeu plus agreable
    return tour % 2 != 0  # Le joueur qui découvre le mot mystère en dernier a gagné

# Cette fonction permet de jouer à une partie de pendu à deux joueurs humains.
# Elle prend en argument : le mot mystère à trouver et le caractère utilisé pour remplacer les
# lettres non trouvées dans le mot découvert
# Elle renvoie True si le joueur 1 a gagné, False sinon (joueur 2 a gagné).
# Effet de bords : efface la console et affiche la progression de la partie
def partie_humain_deux_joueurs(mot_myst, car_subst):
    # Initialisation du mot partiellement découvert
    lmot_decouv = initialiser_mot_part_decouv(mot_myst, car_subst)
    # Initialisation de la liste des lettres déjà proposées
    deja_dit = []
    tour = 0

    # Boucle de jeu
    while mot_myst != ''.join(lmot_decouv):
        effacer_console()
        # Affichage du mot partiellement découvert
        print("\nMot actuel :", end="")
        afficher_texte(lmot_decouv)
        # Affichage de la liste des lettres déjà proposées s'il y en a
        if deja_dit:
            print("Lettres proposees : ", end="")
            afficher_texte(deja_dit, " ")
        # Demande de proposition de lettre
        if tour % 2 == 0:
            print("C'est au tour du joueur 1 !")
            lettre = demander_proposition(deja_dit)
        else:
            print("C'est au tour du joueur 2 !")
            lettre = demander_proposition(deja_dit)

        deja_dit.append(lettre)  # Ajout de la lettre à la liste des lettres proposées
        decouvrir_lettre(lettre, mot_myst, lmot_decouv)  # Découverte de la lettre dans le mot mystère
        tour += 1  # Augmentation du nombre de tours de jeu
        sleep(1)  # Pause de 1 seconde pour rendre le jeu plus agreable

    # Retourne True si le joueur 1 a gagné , False sinon (joueur 2 a gagné)
    return tour % 2 != 0
    
# Définit une fonction qui permet de chronométrer un temps limite et d'afficher le temps restant dans le titre de la fenêtre toutes les secondes.
# Cette fonction utilise deux variables globales : "temps_ecoule" pour indiquer si le temps limite est écoulé et "temps_debut" pour stocker le temps de départ.
# Elle prend en argument : un nombre entier représentant le temps limite en secondes
# Ne renvoie rien, la fonction s'exécute en continu jusqu'à ce que le temps limite soit écoulé.
# Effets de bord :
#   Modifie la variable globale "temps_ecoule" si le temps limite est écoulé
#   Modifie le titre de la fenêtre toutes les secondes pour afficher le temps restant
def chrono(temps_limite):
    # Utilisation des variables globales "temps_ecoule" et "temps_debut"
    global temps_ecoule
    global temps_debut

    # Initialisation de la variable "temps_ecoule" à False
    temps_ecoule = False

    # Initialisation de la variable "temps_debut" à la valeur actuelle du temps
    temps_debut = time()

    while True:
        # Récupération de la valeur actuelle du temps
        temps_actuel = time()

        # Calcul du temps restant avant la fin du temps limite
        temps_restant = round(max(0, temps_limite - (temps_actuel - temps_debut)))

        # Si le temps restant est inferieur à 0, on met la variable "temps_ecoule" à True et on sort de la boucle
        if temps_restant <= 0:
            temps_ecoule = True
            # On remet le titre par defaut
            modifier_titre("Jeu du Pendu par Nahli Zayd et Layada Nasrallah")
            break

        # On modifie le titre afin d'afficher le temps restant toute les secondes
        modifier_titre("Temps restant : {:.0f} secondes".format(temps_restant))
        sleep(1)

# Cette fonction représente la boucle de jeu du pendu en mode contre la montre
# Prends en argument : une liste de mots à deviner , le mot mystere et Le caractère de substitution
# utilisé pour remplacer les lettres non devinées du mot.
# Effets de bord:
# -La fonction affiche le mot partiellement découvert, la liste des lettres déjà proposées et demande une proposition
# de lettre au joueur humain.
# - Si la proposition de lettre est correcte, la fonction affiche le nouveau mot partiellement découvert.
# - Si le mot mystère a été entièrement découvert, la fonction affiche le mot mystère trouvé et passe au mot suivant.
# - Si le temps est écoulé, la fonction affiche un message de fin de jeu avec le nombre de mots trouvés et le mot mystère.
# Ne retourne rien
def boucle_partie_humaine_chrono(mots, mot_myst, car_subst="-"):
    # Initialisation des variables
    lmot_decouv = initialiser_mot_part_decouv(mot_myst, car_subst)
    score = 0
    deja_dit = []
    # Boucle principale du jeu
    while not temps_ecoule:
        # Si le mot mystère a été entièrement découvert, on passe au mot suivant
        if mot_myst == ''.join(lmot_decouv):
            print("Bravo vous avez trouvé le mot : ", mot_myst)
            mot_myst = choisir_mot_alea(mots)
            # Initialisation du mot partiellement découvert
            lmot_decouv = initialiser_mot_part_decouv(mot_myst, car_subst)
            # Initialisation de la liste des lettres déjà proposées
            deja_dit = []
            score += 1

        # Affichage du mot partiellement découvert
        print("\nMot actuel :", end="")
        afficher_texte(lmot_decouv)
        # Affichage de la liste des lettres déjà proposées s'il y en a
        if deja_dit:
            print("Lettres proposees : ", end="")
            afficher_texte(deja_dit, " ")

        # Demande de proposition de lettre
        lettre = demander_proposition(deja_dit)

        deja_dit.append(lettre)
        # Découverte de la lettre dans le mot mystère
        decouvrir_lettre(lettre, mot_myst, lmot_decouv)
        effacer_console()
    print("Temps écoulé !")
    if score > 0:
        print("Vous avez trouvé " + str(score) + " mots en 60 sec")
    else:
        print("PERDU ! Le mot était :", mot_myst)
    print("")
    sleep(1)


# La fonction crée deux threads en parallèle. La première thread est utilisée
# pour afficher le temps écoulé pendant la partie, tandis que la seconde thread gère la boucle de jeu.
# Elle prends en arguments : une liste de mots à deviner pendant la partie et un caractère à utiliser
# pour remplacer les lettres non trouvées dans le mot à deviner.
# Elle ne retourne rien
# Effet de bords : Modifie le titre de la console en lançant un des threads
def partie_humain_chrono(mots, car_subst="-"):
    temps_limite = 60  # Temps limite pour la partie en secondes

    # Boucle de jeu
    # Création de deux threads pour exécuter la fonction chrono() et la fonction boucle_partie_humaine_chrono()
    thread_afficher_temps = threading.Thread(target=chrono, args=(temps_limite,))
    thread_jeu = threading.Thread(target=boucle_partie_humaine_chrono, args=(mots, car_subst,))
    # Démarrage des threads
    thread_afficher_temps.start()
    thread_jeu.start()

    # Attente de la fin de l'exécution des threads
    thread_afficher_temps.join()
    thread_jeu.join()

# Affiche un menu permettant à l'utilisateur de choisir une stratégie de jeu automatique
# Prends en argument le mot à deviner pour lequel on veut proposer des lettres (optionnel, par défaut "")
# Renvoie une liste de lettres à proposer en fonction de la stratégie choisie
# Effet de bords : affichage du menu et demande de saisie utilisateur, possibles appels aux fonctions fabrique_liste_alphabet(), fabrique_liste_alphabet_alea(), fabrique_liste_freq() et fabrique_liste_prob()
def choix_strategie(mot_myst=""):
    # Affichage des choix possibles
    print("Choisissez une stratégie de jeu automatique :")
    print("1. Stratégie alphabétique")
    print("2. Stratégie aléatoire")
    print("3. Stratégie fréquentielle")
    print("4. Stratégie probabiliste")
    print("5. Stratégie de recherche de mots")
    print("6. Quitter")

    # Demande du choix à l'utilisateur
    choix = input("Votre choix (1-6) : ")

    # Selon le choix, renvoie une liste de lettres à proposer
    if choix == "1":
        return fabrique_liste_alphabet()
    elif choix == "2":
        return fabrique_liste_alphabet_alea()
    elif choix == "3":
        return fabrique_liste_freq("mots_gen")
    elif choix == "4":
        return fabrique_liste_prob("mots_gen", len(mot_myst))
    elif choix == "5":
        return ["recherche"]
    elif choix == "6":
        afficher_menu()
    else:
        # Si le choix est invalide, demande une nouvelle saisie
        print("Choix invalide. Veuillez réessayer.")
        return choix_strategie()

if __name__ == '__main__':
    modifier_titre("Jeu du Pendu par Nahli Zayd et Layada Nasrallah")
    appliquer_configuration()
    afficher_menu()
