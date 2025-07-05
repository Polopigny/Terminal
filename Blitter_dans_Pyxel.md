# Blitter dans Pyxel

Le **blitter** dans Pyxel est un outil qui, de la manière pratiquée par les jeux vidéo anciens, permet de manipuler et d'afficher des images ou des portions d'images (lutins ou sprites en anglais) de manière efficace. Pour cela, la fonction `blt` de la bibliothèque copie le contenu indexé d'un fichier ressource pyxres et les colle à dans dans un rectangle dont on donne les coordonnées de l'angle en haut à droite. 


# Fonctionnement de la fonction `blt` dans Pyxel

Voici les paramètres principaux de cette fonction :

    `pyxel.blt(x, y, img, u, v, w, h, [colkey], [rotate], [scale])`

-   `x, y` : Les coordonnées où le lutin sera dessiné sur l'écran.
-   `img` : L'index de la banque d'images (`0` ou `1` par défaut).
-   `u, v` : Les coordonnées du coin supérieur gauche du lutin dans la banque d'images.
-   `w, h` : La largeur et la hauteur du lutin à dessiner.
-   `colkey` _(optionnel)_ : La couleur transparente (si définie, cette couleur du lutin ne sera pas dessinée et sera transparente).
-   `rotate` _(optionnel)_ : Donne un angle de rotation en degré dans le sens indirect.
-   `scale` _(optionnel)_ : Un rapport d'homothétie dont le centre est l'angle en haut à gauche du lutin.

## Créer, éditer un fichier ressource .pyxres

Depuis un terminal Python, on tape `pyxel edit *mon_fichier_resource.pyxres*`
Un éditeur graphique s'ouvre pour modifier ou créer les ressources suivantes:
- 3 banques d'image numérotée 0, 1, 2
- 8 tuiles (grands dessin pour le décor) pour le plan de tuilage
- 64 emplacements de sonnorité sur 4 canaux
- 8 pistes musicales pour combiner les sons

## Charger une resource pyxres et l'exploiter:

Pyxel ne peut employer qu'un seul fichier ressource que l'on charge avec la fonction:
`pyxel.load(nom_du_fichier :str)`
Par contre, les resources peuvent être modifié par par le programme qui emploie Pyxel avec des fonctions pour les images, les sons, les tuiles et la musique.