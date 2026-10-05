import pygame, os

class Jogador(pygame.sprite.Sprite):
    def __init__(self,x,y,pasta="imagens"):
        super().__init__()
        self.frames=[]

        for nome in ("adan2.png","andando.png.png"):
            caminho=os.path.join(pasta,nome)

            if os.path.exists(caminho):
                img=pygame.image.load(caminho).convert_alpha()

                self.frames.append(
                    pygame.transform.scale(img,(260,300))
                )

        if not self.frames:
            self.frames=[pygame.Surface((48,80),pygame.SRCALPHA)]
            pygame.draw.rect(
                self.frames[0],
                (240,190,80),
                (10,5,28,70),
                border_radius=8
            )

        self.image=self.frames[0]
        self.rect=self.image.get_rect(midbottom=(x,y))

        self.velocidade=230
        self.tempo_anim=0
        self.indice=0

    def atualizar(self,dt,teclas,limites):
        dx=dy=0

        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            dx-=self.velocidade*dt

        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            dx+=self.velocidade*dt

        if teclas[pygame.K_UP] or teclas[pygame.K_w]:
            dy-=self.velocidade*dt

        if teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
            dy+=self.velocidade*dt

        self.rect.x+=int(dx)
        self.rect.y+=int(dy)

        self.rect.clamp_ip(limites)

        # Limite superior da grama
        self.rect.top=max(self.rect.top,110)

        if dx or dy:
            self.tempo_anim+=dt

            if self.tempo_anim>.15:
                self.indice=(self.indice+1)%len(self.frames)
                self.tempo_anim=0
                self.image=self.frames[self.indice]