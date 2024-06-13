
<div align="center">

  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://user-images.githubusercontent.com/25423296/163456776-7f95b81a-f1ed-45f7-b7ab-8fa810d529fa.png">
    <source media="(prefers-color-scheme: light)" srcset="https://user-images.githubusercontent.com/25423296/163456779-a8556205-d0a5-45e2-ac17-42d089e3c3f8.png">
    <img alt="Shows an illustrated sun in light mode and a moon with stars in dark mode." src="https://user-images.githubusercontent.com/25423296/163456779-a8556205-d0a5-45e2-ac17-42d089e3c3f8.png">
  </picture>

  # Potich'Advendutes

  <!-- python badge -->
  ![Python 3.12](https://img.shields.io/badge/python-3.12-%23FFE873?style=for-the-badge&logo=python&labelColor=%23FFE873)
  ![Pygame](https://img.shields.io/badge/Pygame-black?style=for-the-badge&color=08df1c)



  <!-- ![GitHub commit activity](https://img.shields.io/github/commit-activity/w/ThimoteB/Jeux-Python?style=for-the-badge) -->


  [Contexte](##contexte) - [Gestion du projet](##gestion-du-projet) - [:star: Nous supporter :star:](#Nous-supporter)


  ---


</div>

## Contexte

Projet universitaire de création d'un jeu-vidéo. Cette collaboration en équipe s'inscrit dans la suite d'un projet en binôme.

Ci-dessous une visualisation des phases du projet:

```mermaid

flowchart LR
    A[Premier rendu: jeu original\nThimoté et Colin] --> C
    C{Deuxième rendu:\nJeu en réseau, IA et BDD\n Thimoté, Colin, Célian et Justin}
    C -->|Thimoté, Justin| D[fa:fa-brain Ajout d'une IA]
    C -->|Colin| E[fa:fa-book Création du readme]
    C -->|Colin, Justin| F[fa:fa-pen Qualité de code]
    C -->|Célian| G[fa:fa-globe Mise en réseau]
```



## Gestion du projet

Le suivi du projet a principalement été fait via les issues Github. Le trello n'a été que peu utilisé après la phase de mise en place de 
la poursuite du projet.

Voici notre workflow adopté :

```mermaid
flowchart TD
    Bug([Découverte d'un Bug]) --> Issue
    Feature([Ajout d'une fonctionnalité]) --> Issue
    Modif([Modifications du code\nOu refactor]) --> Issue
    

    Issue[Ouverture d'une Issue Github] --> Branch

    Branch[Création d'une branch\nex: 14-provide-more-ai] --> Work

    Work[Travail sur ordinateur local \nsur la branche] --> PR

    PR[Création d'une \nMerge Request] --> Review

    Review{Revue du code par\nune autre personne}
    Review -. Commentaire et travail\ncomplémentaire à faire .-> Work
    Review -- PR approuvée, fusion possible --> Merge
    Review -- PR approuvée, fusion impossible --> Conflict

    Conflict[Résolution manuelle du conflit] --Nouvelle revue à faire --> Review
    
    Merge[Fusion sur la branche main] --> End
    Merge -. Poursuite éventuelle\n du développement\nNe pas oublier de rebase sur main .-> Work



    End[[Fermeture de la branche]]

```

## Nous supporter





<!-- ====================RENDU FINAL==================== -->
<!-- TODO - Relire les issues -->
<!-- TODO - Remettre le jeu en fullscreen -->
<!-- TODO - Faire une release github -->



<!-- ====================ARCHIVE==================== -->
<!-- Vérifier avant rendu final -->
<!-- TODO - Readme -->
<!-- TODO - Cartes de départ -->
<!-- TODO - Curseur personnalisé ? -->
<!-- FIXME - rename les sons de racistes qui ont une majuscule -->

<!-- Dans le futur -->
<!-- TODO - Chanegr comment les animations sont chargées (virer props_catalogue -> get_tile_properties_by_gid) -->
<!-- TODO - méthode from_card_list() pour le main -->
<!-- TODO - Sauvegarde d'une partie -->
<!-- TODO - sprites randoms pour les ennemis -->
<!-- TODO - Axe Z (se cacher derrière les arbres ...)-->
<!-- TODO - Spawn des joueurs et des mobs avec des spawners sur la carte (dans tiled) -->
<!-- TODO - Déplacer la gestion du fog dans cell.py -->
<!-- TODO - Rendre tout responsive sur la verticale -->