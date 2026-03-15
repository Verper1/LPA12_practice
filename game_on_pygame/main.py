"""Входной файл для запуска игры."""
import pygame

from game_on_pygame.config import player, player_speed, enemies, enemy_speed, \
    start_pos, lives, is_key_obtained, trigger_enemy, trigger_enemy_flag
from game_on_pygame.utils import exit_rect, walls, key_rect, BLUE, GOLDEN, \
    GREEN, WHITE, RED, locked_door, trigger_door

# --- Инициализация ---
pygame.init()
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Выберись из лабиринта")
clock = pygame.time.Clock()

if __name__ == "__main__":
    # --- Основной цикл ---
    running = True
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if player.colliderect(exit_rect):
                print("Ты выиграл!")
                running = False

        # --- Движение игрока ---
        old_player_pos = player.topleft
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            player.x -= player_speed
        if keys[pygame.K_d]:
            player.x += player_speed
        if keys[pygame.K_w]:
            player.y -= player_speed
        if keys[pygame.K_s]:
            player.y += player_speed

        # --- Проверка столкновений со стенами игроком ---
        for wall in walls:
            if player.colliderect(wall) or (locked_door and player.colliderect(locked_door)):
                player.topleft = old_player_pos
            if player.colliderect(key_rect):
                is_key_obtained = True
                locked_door = None
            if trigger_door and player.colliderect(trigger_door):
                trigger_door = None
                trigger_enemy_flag = True

        # --- Движение врагов направлено к игроку ---
        for enemy in enemies:
            old_enemy_pos = enemy.topleft

            if player.x > enemy.x:
                enemy.x += enemy_speed
            elif player.x < enemy.x:
                enemy.x -= enemy_speed

            if player.y > enemy.y:
                enemy.y += enemy_speed
            elif player.y < enemy.y:
                enemy.y -= enemy_speed

            # --- Проверка столкновений со стенами ---
            for wall in walls:
                if enemy.colliderect(wall):
                    enemy.topleft = old_enemy_pos

        # --- Проверка столкновения с врагами ---
        for enemy in enemies:
            if player.colliderect(enemy):
                lives -= 1
                if lives <= 0:
                    running = False
                    print("Ты проиграл! Жизней больше не осталось.")
                player.topleft = start_pos

        # --- Отрисовка ---
        screen.fill("grey")
        for wall in walls:
            pygame.draw.rect(screen, BLUE, wall)
        if locked_door:
            pygame.draw.rect(screen, GOLDEN, locked_door)
        pygame.draw.rect(screen, GREEN, exit_rect)
        pygame.draw.rect(screen, WHITE, player)
        if not is_key_obtained:
            pygame.draw.rect(screen, GOLDEN, key_rect)
        for enemy in enemies:
            pygame.draw.rect(screen, RED, enemy)
        if trigger_enemy_flag:
            pygame.draw.rect(screen, RED, trigger_enemy)
            trigger_enemy.x += 4.5
            if player.colliderect(trigger_enemy):
                running = False
                print("Тебя догнали! Не отпускай кнопку перемещения и действуй быстро.")

        # --- Шрифт для жизней ---
        font = pygame.font.Font(None, 36)

        # --- Отображение жизней ---
        lives_text = font.render(f"Lives: {lives}", True, WHITE)
        screen.blit(lives_text, (10, 10))

        pygame.display.flip()

    pygame.quit()