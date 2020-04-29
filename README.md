# ETUBOT
Projet Dev App EPSI B1 2020
réalisé par Marine RICO, Olivier TANGUY, Daniel GAVRILINE, Hugo CABARET

## INTRO
Etubot est un bot discord destiné a l'organisation et l'information de la vie étudiante
Toutes les commandes doivent être précédé d'un point

## pré-requis
pensez avant toutes utilisation a installer les modules suivant (pip install):
- tinydb
- discord
- beautifulsoup4
- requests
- discord.py 
- time
- datetime

## utilisation
Pour avoir accès aux emploi du temps, nous avons eu besoin d'utiliser l'API de Calendz.
### etubot

- .load nom_bot (pour charger un bot)
- .unload nom_bot (pour décharger un bot)
- .reload nom_bot (pour recharger un bot)

### bot_edt.py

permet d'afficher les cours et de les gérer
- .id nom prenom id_channel (permet d'affecter un referent aux channel (par la suite .edt affichera l'edt du referent))
- .edt jour (affiche l'emploi du temps du jour demandé)
- .cours (Affiche une liste de cours)
- .time (Affiche l'heure)

### bot_devoir.py

permet d'afficher les devoirs et de les gérer
- .enter_dev date cours message (ajouter un devoir)
- .rem_dev date cours(supprimer un devoir)
- .list_dev (affiche tous les devoirs)
- .search_date date (affiche les devoirs d'un jour precis)

### bot_meteo.py

- .meteo (permet d'afficher lameteo du jour)

### bot_rappel.py

- .rappel (Envoyer l'emploi du temps sur le tchat)
- .mon_rappel (Envoyer l'emploi du temps en DM à l auteur)
- .mes_rappels (Envoyer l'emploi du temps en DM à l ou plusieurs membres)

### bot_df.py

- .df mot (donne la définition d'un mot) 

### bot_article.py

- .listnews (liste tous les articles abonnés)
- .addnews url ".class1 .class2" (rajoute un article)
- .remnews url (permet de supprimer un article des suivis)
