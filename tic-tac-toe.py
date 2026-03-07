"""Игра 'Крестики-Нолики'."""
from time import sleep
from random import randint, choice

from loguru import logger


def show_board(board: list) -> None:
    """Отрисовка доски в человекочитаемом виде."""
    print("-------------")
    print(f"| {board[0]} | {board[1]} | {board[2]} |")
    print(f"| {board[3]} | {board[4]} | {board[5]} |")
    print(f"| {board[6]} | {board[7]} | {board[8]} |")
    print("-------------")


def check_board(board: list) -> bool:
    """Проверяет все ли элементы списка числа или нет. Если да, то проверяется на ничью в функции find_winner."""
    answer = all(isinstance(i, str) for i in board)
    return answer


def make_turn(board: list, board_place: int, simbol: str, all_nums: list) -> list:
    """Ставит символ ходящего игрока на место цифры в словаре."""
    board[board.index(board_place)] = simbol

    all_nums.remove(board_place)
    return board

def find_winner(board: list) -> str:
    """Отдаёт либо победителя, либо ничью, либо игра после всех проверок дальше продолжается."""
    win_coords = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Горизонтали
        (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Вертикали
        (0, 4, 8), (2, 4, 6)  # Диагонали
    ]

    for a, b, c in win_coords:
        if board[a] == board[b] == board[c] == "X":
            return "X"
        elif board[a] == board[b] == board[c] == "O":
            return "O"

    if check_board(board):
        return "Ничья!"

    return "Игра продолжается"


def main() -> None:
    """Главная функция, которая содержит в себе саму логику игры."""
    player = "X" if randint(0, 1) else "O"
    robot = "O" if player == "X" else "X"
    board = [
        1, 2, 3,
        4, 5, 6,
        7, 8, 9
    ]
    all_nums = [*range(1, 10)]

    print(f"Начнём игру: Крестики-нолики!\nТы играешь за {player}, а робот играет за {robot}")
    show_board(board)
    turn_now = "player" if player == "X" else "robot"
    sleep(2)

    while find_winner(board) == "Игра продолжается":
        try:
            if turn_now == "player":
                board_place = int(input("Твой ход: "))
                make_turn(board, board_place, player, all_nums)
                show_board(board)
                turn_now = "robot"
                print("++++++++++++++++++++++++++++++++++")
                sleep(2)
            else:
                board_place = choice(all_nums)
                print(f"Ход робота: {board_place}")
                make_turn(board, board_place, robot, all_nums)
                show_board(board)
                turn_now = "player"
                print("++++++++++++++++++++++++++++++++++")
                sleep(2)
        except ValueError as e:
            print("Ошибка: некорректный ввод! Используйте только целые числа от 1 до 9.")
            logger.error(e)
    else:
        win = find_winner(board)

        if win != "Ничья!":
            print(f"И победитель у нас: {"player" if win == player else "robot"}")
        else:
            print("Победителей нет. Ничья!")


if __name__ == "__main__":
    main()
