"""Тут можно настроить характеристики для игрока, обычных врагов и триггер-противника."""
import pygame

# --- Игрок ---
player_size = 32
player = pygame.Rect(50, 50, player_size, player_size)
player_speed = 4
lives = 3
start_pos = player.topleft
is_key_obtained = False


# --- Враги ---
enemy_size = 50
enemies = [
    pygame.Rect(150, 150, enemy_size, enemy_size),
    pygame.Rect(450, 350, 70, 70)
]
enemy_speed = 1

# ---Триггер противник ---
trigger_enemy = pygame.Rect(25, 535, 32, 32)
trigger_enemy_flag = False