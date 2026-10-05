import pygame, sys
from cenas import Jogo

pygame.init()
LARGURA, ALTURA = 960, 540
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Adelis")
relogio = pygame.time.Clock()
jogo = Jogo(tela)

while True:
    dt = relogio.tick(60) / 1000
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        jogo.evento(evento)
    jogo.atualizar(dt)
    jogo.desenhar()
    pygame.display.flip()
