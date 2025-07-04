import pyxel


SIZE = 256
class Sprites:
    _x = 20
    _y = 20
    def __init__(self):
        pyxel.init(SIZE, SIZE,title ="Lutin Demo")
        self._frame = 0

        # Crée une image de sprite dans la mémoire graphique de Pyxel 0
        # Equivaut à Pyxel.load("mon_fichier.pyxres", )
        '''pyxel.images[1].set(
            0, 0,
            [
                "00077000",
                "00777770",
                "07777770",
                "77777777",
                "77077077",
                "07777770",
                "00700700",
                "07000070",
            ]
        )

        #pyxel.images[0].set(
            8, 0,
            [
                "00077000",
                "07777700",
                "07777770",
                "77777777",
                "77077077",
                "07777770",
                "00077000",
                "00700700",
            ]
        )'''
        pyxel.load("../Template/2.pyxres")

        pyxel.run(self.update, self.draw)

    def update(self):
        # Changer d'animation toutes les 10 frames
        self._frame = (pyxel.frame_count // 10) % 2


    def draw(self):
        pyxel.cls(0)  # Efface l'écran
        pyxel.blt(Sprites._x, Sprites._y, 0, 0, 16, 16, 16,colkey=2)
        pyxel.text(Sprites._x-15, Sprites._y+30, "Image de\nla banque 0\n8 x 8 px",pyxel.COLOR_WHITE)
        pyxel.blt(Sprites._x+50, Sprites._y, 1, self._frame * 8, 0, 8, -8, 0)
        pyxel.text(Sprites._x+35, Sprites._y+30, "Image de\nla banque 1\n8 x 8 px\ninv. vert",pyxel.COLOR_WHITE)
        pyxel.blt(Sprites._x+100, Sprites._y, 1, self._frame * 8, 0, 8, 8, -0)
        pyxel.text(Sprites._x+85, Sprites._y+30, "Image de\nla banque 1\n8 x 8 px\ninv. horiz",pyxel.COLOR_WHITE)
        pyxel.blt(Sprites._x+150, Sprites._y, 1, self._frame * 8, 0, 8, 8, 0, rotate=45)
        pyxel.text(Sprites._x+135, Sprites._y+30, "Image de\nla banque 1\n8 x 8 px\ntournee 45°\nsens ind.",pyxel.COLOR_WHITE)
        pyxel.blt(Sprites._x+200, Sprites._y, 1, self._frame * 8, 0, 8, 8, 0, scale=2)
        pyxel.text(Sprites._x+185, Sprites._y+30, "Image de\nla banque 1\n8 x 8 px\nhomotethie x2",pyxel.COLOR_WHITE)

#pyxel.blt()
#pyxel.bltm()
Sprites()