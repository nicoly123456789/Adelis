import pygame, random, os

class Obstaculo(pygame.sprite.Sprite):
    def __init__(self,x,y,tipo="passaro",velocidade=220,pasta="imagens"):
        super().__init__()
        nomes={"passaro":"passaro.png.png","monstro":"monstro.png","bala":"bala_magica.png"}
        caminho=os.path.join(pasta,nomes.get(tipo,"passaro.png"))
        
        if os.path.exists(caminho):
            self.image=pygame.image.load(caminho).convert_alpha()

            if tipo=="passaro":
                self.image=pygame.transform.scale(self.image,(260,240))
            else:
                self.image=pygame.transform.scale(self.image,(128,192))
        else:
            self.image=pygame.Surface((38,38),pygame.SRCALPHA)
            pygame.draw.circle(self.image,(190,65,80),(19,19),18)

        self.rect=self.image.get_rect(center=(x,y))
        self.tipo=tipo
        self.velocidade=velocidade

        if self.tipo=="passaro":
            self.hitbox=pygame.Rect(0,0,70,60)
            self.hitbox.center=self.rect.center
        else:
            self.hitbox=self.rect.copy()

    def update(self,dt):
        self.rect.x-=int(self.velocidade*dt)
        self.hitbox.center=self.rect.center

        if self.tipo=="bala":
            self.rect.y+=int(random.choice([-1,1])*self.velocidade*.12*dt)