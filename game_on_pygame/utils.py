"""Здесь лежат всякие переменные и окружение."""
import pygame

# --- Цвета ---
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GOLDEN = (225, 215, 0)

# --- Лабиринт (стены) ---
walls = [
    pygame.Rect(0, 0, 600, 10),     # верх
    pygame.Rect(0, 0, 10, 600),     # левая
    pygame.Rect(0, 590, 600, 10),   # низ
    pygame.Rect(590, 0, 10, 600),    # правая

    pygame.Rect(10, 90, 200, 10),
    pygame.Rect(200, 90, 10, 200),
    pygame.Rect(300, 10, 10, 200),
    pygame.Rect(200, 290, 200, 10),
    pygame.Rect(400, 290, 10, 100),
    pygame.Rect(100, 380, 300, 10),
    pygame.Rect(100, 500, 500, 10)
]

# --- Закрытая дверь ---
locked_door = pygame.Rect(10, 500, 100, 10)

# --- Выход ---
exit_rect = pygame.Rect(550, 550, 40, 40)

# --- Ключ для двери ---
key_rect = pygame.Rect(50, 150, 40, 40)

# --- Триггер-стена ---
trigger_door = pygame.Rect(189, 510, 10, 80)
