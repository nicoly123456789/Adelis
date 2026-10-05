import pygame

BRANCO=(255,255,255); PRETO=(15,15,20); ROXO=(45,32,62); DOURADO=(240,205,120)

class Interface:
    def __init__(self):
        self.fonte=pygame.font.SysFont("arial",24)
        self.pequena=pygame.font.SysFont("arial",19)
        self.titulo=pygame.font.SysFont("arial",48,bold=True)

    def texto(self,tela,texto,x,y,cor=BRANCO,fonte=None):
        tela.blit((fonte or self.fonte).render(str(texto),True,cor),(x,y))

    def caixa(self,tela,linhas):
        r=pygame.Rect(35,365,890,145)
        pygame.draw.rect(tela,ROXO,r,border_radius=12)
        pygame.draw.rect(tela,DOURADO,r,3,border_radius=12)
        for i,linha in enumerate(linhas[:4]):
            self.texto(tela,linha,60,385+i*29)

    def tela_cheia(self,tela,titulo,subtitulo=""):
        tela.fill(PRETO)
        t=self.titulo.render(titulo,True,DOURADO)
        tela.blit(t,t.get_rect(center=(480,220)))
        if subtitulo:
            s=self.fonte.render(subtitulo,True,BRANCO)
            tela.blit(s,s.get_rect(center=(480,290)))

    def ranking(self,pontos):
        if pontos>=80: return "A"
        if pontos>=60: return "B"
        if pontos>=40: return "C"
        if pontos>=20: return "D"
        return "E"
