import pyxel

class APP():
    def __init__(self):
        pyxel.init(256,256,"Terminal V1.1",fps=30)
        pyxel.load("../Template/2.pyxres")
        pyxel.run(self.Update,self.Draw)
    
    def Update(self):
        pass

    def Draw(self):
        pyxel.cls(9)

APP()