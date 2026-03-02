from time import sleep
from random import randint, choice
from loguru import logger

player = "X" if randint(0, 1) else "O"
robot = "O" if player == "X" else "X"
board = [
    1, 2, 3,
    4, 5, 6,
    7, 8, 9
]
all_nums = [*range(1, 10)]


def show_board(board: list) -> None:
    print("-------------")
    print(f"| {board[0]} | {board[1]} | {board[2]} |")
    print(f"| {board[3]} | {board[4]} | {board[5]} |")
    print(f"| {board[6]} | {board[7]} | {board[8]} |")
    print("-------------")


def check_board(board: list) -> bool:
    answer = all(isinstance(i, str) for i in board)
    return answer


def turn(board: list, board_place: int, simbol: str) -> list:
    board[board.index(board_place)] = simbol

    all_nums.remove(board_place)
    return board

def winner(board: list) -> str:
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


def main() -> None:
    print(f"Начнём игру: Крестики-нолики!\nТы играешь за {player}, а робот играет за {robot}")
    show_board(board)
    turn_now = "player" if player == "X" else "robot"
    sleep(2)

    while not check_board(board) and winner(board) is None:
        try:
            if turn_now == "player":
                board_place = int(input("Твой ход: "))
                turn(board, board_place, player)
                show_board(board)
                turn_now = "robot"
                print("++++++++++++++++++++++++++++++++++")
                sleep(2)
            else:
                board_place = choice(all_nums)
                print(f"Ход робота: {board_place}")
                turn(board, board_place, robot)
                show_board(board)
                turn_now = "player"
                print("++++++++++++++++++++++++++++++++++")
                sleep(2)
        except ValueError as e:
            print("Ошибка: Нельзя поставить свой значок на уже занятое поле или вы используете другой символ!")
            logger.error(e)

    win = winner(board)

    if win != "Ничья!":
        print(f"И победитель у нас: {"player" if win == player else "robot"}")
    else:
        print("Победителей нет. Ничья!")


if __name__ == "__main__":
    main()
