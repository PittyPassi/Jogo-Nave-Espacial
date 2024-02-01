import pygame
import sys
import random

# Inicialização do Pygame
pygame.init()

# Definição de constantes
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
PLAYER_COLOR = GREEN
BULLET_COLOR = GREEN
ENEMY_COLOR = RED
PLAYER_SPEED = 5
ENEMY_SPEED = 2
BULLET_SPEED = 5

# Configuração da tela
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Galaga Clone")

# Classe para representar o jogador (nave espacial triangular)
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 40), pygame.SRCALPHA)
        pygame.draw.polygon(self.image, GREEN, [(20, 0), (0, 40), (40, 40)])
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 10
        self.speedx = 0

    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -PLAYER_SPEED
        if keystate[pygame.K_RIGHT]:
            self.speedx = PLAYER_SPEED
        self.rect.x += self.speedx

        # Limitar a nave dentro da tela
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        bullets.add(bullet)
        all_sprites.add(bullet)

# Classe para representar os inimigos (triângulos apontando para baixo)
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
        pygame.draw.polygon(self.image, RED, [(15, 30), (0, 0), (30, 0)])
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(-50, -30)  # Começam acima da tela

    def update(self):
        self.rect.y += ENEMY_SPEED
        # Reiniciar inimigo quando sair da tela
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
            self.rect.y = random.randint(-50, -30)

# Classe para representar as balas
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill(BULLET_COLOR)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y

    def update(self):
        self.rect.y -= BULLET_SPEED
        # Remover a bala se ela sair da tela
        if self.rect.bottom < 0:
            self.kill()

# Grupo de sprites para todos os objetos em jogo
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

# Variáveis para controle de jogo
score = 0
game_over = False

# Fonte para exibir a pontuação
font = pygame.font.Font(None, 36)

# Loop principal do jogo
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over:
                player.shoot()

    if not game_over:
        # Gerar inimigos ordenadamente
        now = pygame.time.get_ticks()
        if now % 2000 < 50:  # Cria um inimigo a cada 2 segundos
            enemy = Enemy()
            enemies.add(enemy)
            all_sprites.add(enemy)

        # Atualizar
        all_sprites.update()

        # Verificar colisões entre balas e inimigos
        hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
        for hit_enemy in hits:
            score += 1

        # Verificar colisões entre jogador e inimigos
        hits = pygame.sprite.spritecollide(player, enemies, False)
        if hits:
            game_over = True

        # Renderizar
        screen.fill((0, 0, 0))
        all_sprites.draw(screen)

        # Exibir pontuação no topo da tela
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(60)

    else:
        # Exibir "GAME OVER" e pontuação final
        screen.fill((0, 0, 0))
        game_over_text = font.render("GAME OVER", True, WHITE)
        score_text = font.render(f"Score: {score}", True, WHITE)
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        screen.blit(game_over_text, game_over_rect)
        screen.blit(score_text, score_rect)
        pygame.display.flip()

pygame.quit()
sys.exit()
