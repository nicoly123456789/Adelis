
import pygame, random, os
from jogador import Jogador
from obstaculo import Obstaculo
from interfaces import Interface


class Aviao(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        caminho = os.path.join("imagens", "aviao.png.png")
        self.image = pygame.image.load(caminho).convert_alpha()
        self.image = pygame.transform.scale(self.image, (220, 230))
        self.rect = self.image.get_rect(center=(x, y))
        self.hitbox = pygame.Rect(0, 0, 70, 45)
        self.hitbox.center = self.rect.center

    def atualizar(self, dt, teclas, limites):
        velocidade = 300
        dx = dy = 0

        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            dx -= velocidade * dt
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            dx += velocidade * dt
        if teclas[pygame.K_UP] or teclas[pygame.K_w]:
            dy -= velocidade * dt
        if teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
            dy += velocidade * dt

        self.rect.x += int(dx)
        self.rect.y += int(dy)
        self.rect.clamp_ip(limites)
        self.hitbox.center = self.rect.center


class Jogo:
    def __init__(self, tela):
        self.tela = tela
        self.w, self.h = tela.get_size()
        self.ui = Interface()

        self.estado = "menu"
        self.fase = 1
        self.pontos = 0
        self.distancia = 0

        self.jogador = Jogador(150, 400)
        self.aviao = Aviao(150, 270)

        self.obstaculos = pygame.sprite.Group()
        self.fundo = None
        self.dialogo = []
        self.linha = 0
        self.escolhas = []

        self.timer_spawn = 0
        self.timer = 0
        self.indice_cena = 0

        self.npc_pos = (850, 400)
        self.npc_interagiu = False

        self.loading = 0
        self.imagem_loading = None

        caminho_loading = os.path.join(
            "imagens",
            "adelisloading.png"
        )

        if os.path.exists(caminho_loading):
            imagem = pygame.image.load(
                caminho_loading
            ).convert_alpha()

            largura = 500
            altura = int(
                imagem.get_height()
                * (largura / imagem.get_width())
            )

            self.imagem_loading = pygame.transform.scale(
                imagem,
                (largura, altura)
            )

        self.cenas_f2 = [
            "floresta_inicio.png",
            "cena2floresta.png",
            "cidade.png",
            "floresta_cemiterio.png",
            "cemiterio1.png.jpeg"
        ]

        self.cenas_f5 = ["floresta_boss.png"]

        self.carregar_fundo("ceu.png")

    def carregar_fundo(self, nome):
        caminho = os.path.join("imagens", nome)

        if os.path.exists(caminho):
            self.fundo = pygame.transform.scale(
                pygame.image.load(caminho).convert(),
                (self.w, self.h)
            )
        else:
            self.fundo = None

    def iniciar_dialogo(self, linhas, proximo):
        self.dialogo = linhas
        self.linha = 0
        self.proximo = proximo
        self.estado = "dialogo"

    def evento(self, e):
        if e.type != pygame.KEYDOWN:
            return

        if self.estado == "menu":
            if e.key == pygame.K_RETURN:
                self.fase1()

        elif self.estado == "dialogo":
            if e.key in (pygame.K_RETURN, pygame.K_SPACE):
                self.linha += 1

                if self.linha >= len(self.dialogo):
                    self.estado = self.proximo

        elif self.estado == "interrogatorio":
            if e.key in (pygame.K_1, pygame.K_2, pygame.K_3):
                if e.key == pygame.K_1:
                    self.iniciar_dialogo(
                        [
                            "Kandelabra: Resposta aceitável.",
                            "Kandelabra: A carta fala sobre um corpo na Floresta de Sarius.",
                            "Adelis: Eu posso ajudar. Tenho um avião e posso levá-la até lá.",
                            "Kandelabra: Então partiremos imediatamente."
                        ],
                        "fase4"
                    )
                else:
                    self.estado = "gameover"

        elif self.estado == "gameover":
            if e.key == pygame.K_r:
                self.fase1()
            elif e.key == pygame.K_RETURN:
                self.estado = "menu"

        elif self.estado == "ranking":
            if e.key == pygame.K_RETURN:
                self.fase5()

        elif self.estado == "vitoria":
            if e.key == pygame.K_RETURN:
                self.estado = "menu"

    def fase1(self):
        self.fase = 1
        self.estado = "fase1"
        self.obstaculos.empty()
        self.timer = 0
        self.timer_spawn = 0
        self.pontos = 0
        self.npc_interagiu = False
        self.loading = 0

        self.aviao.rect.center = (150, 270)
        self.aviao.hitbox.center = self.aviao.rect.center

        self.carregar_fundo("ceu.png")

    def atualizar(self, dt):
        if self.estado == "fase1":
            self.timer += dt
            self.timer_spawn += dt

            teclas = pygame.key.get_pressed()

            self.aviao.atualizar(
                dt,
                teclas,
                self.tela.get_rect()
            )

            if self.timer_spawn > 1.8:
                self.obstaculos.add(
                    Obstaculo(
                        self.w + 20,
                        random.randint(50, self.h - 50),
                        "passaro",
                        260
                    )
                )
                self.timer_spawn = 0

            self.obstaculos.update(dt)

            for o in list(self.obstaculos):
                if o.rect.right < 0:
                    o.kill()
                    self.pontos += 5

            if any(
                self.aviao.hitbox.colliderect(o.hitbox)
                for o in self.obstaculos
            ):
                self.estado = "gameover"

            if self.timer > 18:
                self.estado = "loading"
                self.loading = 0
                self.obstaculos.empty()

        elif self.estado == "loading":
            self.loading += dt / 7

            if self.loading >= 1:
                self.loading = 1
                self.indice_cena = 0
                self.carregar_fundo(self.cenas_f2[0])
                self.estado = "exploracao"
                self.jogador.rect.midbottom = (100, 500)

        elif self.estado == "exploracao":
            teclas = pygame.key.get_pressed()

            limites = self.tela.get_rect()

            if self.indice_cena == 2:
                limites = pygame.Rect(
                    0,
                    185,
                    self.w,
                    self.h + 120
                )

            self.jogador.atualizar(
                dt,
                teclas,
                limites
            )

            if self.indice_cena == 2 and not self.npc_interagiu:
                npc_rect = pygame.Rect(
                    self.npc_pos[0] - 60,
                    self.npc_pos[1] - 80,
                    120,
                    160
                )

                if self.jogador.rect.colliderect(npc_rect):
                    self.npc_interagiu = True

                    self.iniciar_dialogo(
                        [
                            "Adelis: Com licença, sabe onde encontro a Faxineira?",
                            "NPC: Procure no cemitério, ao norte."
                        ],
                        "exploracao"
                    )

            if self.jogador.rect.right >= self.w - 10:
                self.indice_cena += 1

                if self.indice_cena < len(self.cenas_f2):
                    self.carregar_fundo(
                        self.cenas_f2[self.indice_cena]
                    )

                    self.jogador.rect.left = 5

                else:
                    self.iniciar_dialogo(
                        [
                            "Adelis: Finalmente encontrei você.",
                            "Kandelabra: Quem é você? O que veio fazer aqui?",
                            "Adelis: Trouxe uma carta diplomática."
                        ],
                        "interrogatorio"
                    )

        elif self.estado == "fase4":
            self.timer += dt
            self.timer_spawn += dt

            teclas = pygame.key.get_pressed()

            self.aviao.atualizar(
                dt,
                teclas,
                self.tela.get_rect()
            )

            if self.timer_spawn > 0.8:
                self.obstaculos.add(
                    Obstaculo(
                        self.w + 10,
                        random.randint(40, 500),
                        "monstro",
                        230
                    )
                )
                self.timer_spawn = 0

            self.obstaculos.update(dt)

            for o in list(self.obstaculos):
                if o.rect.right < 0:
                    o.kill()
                    self.pontos += 10

            if pygame.sprite.spritecollideany(
                self.jogador,
                self.obstaculos
            ):
                self.estado = "gameover"

            if self.timer > 20:
                self.estado = "ranking"
                self.obstaculos.empty()

        elif self.estado == "boss":
            self.timer += dt
            self.timer_spawn += dt

            teclas = pygame.key.get_pressed()

            self.jogador.atualizar(
                dt,
                teclas,
                self.tela.get_rect()
            )

            if self.timer_spawn > 0.65:
                self.obstaculos.add(
                    Obstaculo(
                        self.w + 10,
                        random.randint(40, 500),
                        "bala",
                        280
                    )
                )
                self.timer_spawn = 0

            self.obstaculos.update(dt)

            for o in list(self.obstaculos):
                if o.rect.right < 0:
                    o.kill()

            if pygame.sprite.spritecollideany(
                self.jogador,
                self.obstaculos
            ):
                self.estado = "gameover"

            if self.timer > 18:
                self.estado = "vitoria"
                self.obstaculos.empty()

    def fase5(self):
        self.fase = 5

        self.carregar_fundo("floresta_boss.png")

        self.jogador.rect.center = (130, 420)

        self.iniciar_dialogo(
            [
                "Adelis: O corpo não está aqui!",
                "Monsier: Era uma armadilha para Kandelabra.",
                "Prepare-se!"
            ],
            "boss"
        )

        self.timer = 0
        self.timer_spawn = 0

    def desenhar(self):
        if self.fundo:
            self.tela.blit(self.fundo, (0, 0))
        else:
            self.tela.fill((105, 155, 205))

        if self.estado == "menu":
            self.ui.tela_cheia(
                self.tela,
                "ADELIS",
                "Pressione ENTER para começar"
            )

        elif self.estado == "fase1":
            self.obstaculos.draw(self.tela)

            self.tela.blit(
                self.aviao.image,
                self.aviao.rect
            )

            self.ui.texto(
                self.tela,
                f"Pontos: {self.pontos}",
                15,
                15
            )

        elif self.estado == "loading":
            self.tela.fill((20, 20, 25))

            if self.imagem_loading:
                rect_imagem = self.imagem_loading.get_rect(
                    center=(self.w // 2, 150)
                )

                self.tela.blit(
                    self.imagem_loading,
                    rect_imagem
                )

            fonte = pygame.font.Font(None, 42)

            texto = fonte.render(
                "Adelis chega em Cotton",
                True,
                (255, 255, 255)
            )

            rect_texto = texto.get_rect(
                center=(self.w // 2, 320)
            )

            self.tela.blit(
                texto,
                rect_texto
            )

            largura_barra = 600
            altura_barra = 35

            x = (self.w - largura_barra) // 2
            y = 380

            pygame.draw.rect(
                self.tela,
                (70, 70, 75),
                (x, y, largura_barra, altura_barra)
            )

            pygame.draw.rect(
                self.tela,
                (255, 255, 255),
                (
                    x,
                    y,
                    int(largura_barra * self.loading),
                    altura_barra
                )
            )

            pygame.draw.rect(
                self.tela,
                (255, 255, 255),
                (x, y, largura_barra, altura_barra),
                2
            )

            porcentagem = int(self.loading * 100)

            texto_loading = fonte.render(
                f"Carregando... {porcentagem}%",
                True,
                (255, 255, 255)
            )

            rect_loading = texto_loading.get_rect(
                center=(self.w // 2, 450)
            )

            self.tela.blit(
                texto_loading,
                rect_loading
            )

        elif self.estado in ("fase4", "boss"):
            self.obstaculos.draw(self.tela)

            self.tela.blit(
                self.jogador.image,
                self.jogador.rect
            )

            self.ui.texto(
                self.tela,
                f"Pontos: {self.pontos}",
                15,
                15
            )

        elif self.estado == "exploracao":
            self.tela.blit(
                self.jogador.image,
                self.jogador.rect
            )

            self.ui.texto(
                self.tela,
                "Use WASD ou as setas para caminhar. Alcance a direita.",
                15,
                15
            )

        elif self.estado == "dialogo":
            self.ui.caixa(
                self.tela,
                [
                    self.dialogo[self.linha],
                    "ENTER/ESPAÇO para continuar"
                ]
            )

        elif self.estado == "interrogatorio":
            self.ui.caixa(
                self.tela,
                [
                    "Kandelabra: Responda ao que perguntei.",
                    "1) Vim entregar uma carta.",
                    "2) Vim roubar seus pertences.",
                    "3) Não lhe devo explicações."
                ]
            )

        elif self.estado == "gameover":
            self.ui.tela_cheia(
                self.tela,
                "GAME OVER",
                "R para tentar novamente | ENTER para menu"
            )

        elif self.estado == "ranking":
            nota = self.ui.ranking(self.pontos)

            self.ui.tela_cheia(
                self.tela,
                "FIM DA FASE 4",
                f"Pontos: {self.pontos} | Ranking: {nota} | ENTER para continuar"
            )

        elif self.estado == "vitoria":
            self.ui.tela_cheia(
                self.tela,
                "FIM DE ADELIS",
                "Monsier fugiu. ENTER para voltar ao menu"
            )

