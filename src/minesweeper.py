from typing import Iterator, Tuple, List
import tkinter as tk
from tkinter import ttk
from dataclasses import dataclass
from enum import Enum
from random import randint



PADX = 1  # Padding width along horizontal axis
PADY = 1  # Padding width along vertical axis


def _get_mine_position(bomb_num, width, height) -> List[Tuple[int, int]]:
    result = []

    while True:
        if len(result) == bomb_num:
            break

        pos = (randint(0, width-1), randint(0, height-1))

        if not pos in result:
            result.append(pos)

    return result


def _get_neighbor_indexes(width: int, height: int) -> Iterator[int, int, Tuple[Tuple[int, int]]]:
    for w in range(width):
        for h in range(height):
            if w == 0:
                if h == 0:
                    indexes = ((1, 0), (0, 1), (1, 1))
                elif h == height-1:
                    indexes = ((1, 0), (0, -1), (1, -1))
                else:
                    indexes = ((0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
            elif w == width-1:
                if h == 0:
                    indexes = ((-1, 0), (0, -1), (-1, 1))
                elif h == height-1:
                    indexes = ((-1, 0), (0, -1), (-1, -1))
                else:
                    indexes = ((0, -1), (0, 1), (-1, -1), (-1, 0), (-1, 1))

            elif h == 0:
                if 0 < w < width-1:
                    indexes = ((-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0))
            elif h == height-1:
                    indexes = ((-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0))

            else:
                indexes = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))

            yield w, h, indexes


class CellType(Enum):
    NOTHING = 0
    MINE = 1
    NUM = 2


class CellOpenType(Enum):
    OPEN = 0
    HIDE = 1


@dataclass
class Grid:
    x: int
    y: int
    frame: tk.Frame
    cell_open: CellOpenType
    cell_type: CellType = CellType.NOTHING
    NEIGHBOR_MINE_NUM: int = 0


def _prepare_frame(master: tk.Tk, col: int, row: int) -> tk.Frame:
    frame = tk.Frame(master)
    frame.grid(column=col, row=row, padx=PADX, pady=PADY)
    return frame


class Board:
    def __init__(self, bomb_num: int, width: int, height: int, master: tk.Tk):
        self.board = [[Grid(w, h, _prepare_frame(w, h), CellOpenType.HIDE) for w in range(width)] for h in range(height)]
        self._initialize_mine_position(bomb_num, width, height)
        self._initialize_mine_neighbor(width, height)

    def _initialize_mine_position(self, bomb_num: int, width: int, height: int):
        mine_position = _get_mine_position(bomb_num, width, height)
        for mine_pos in mine_position:
            self[mine_pos].cell_type = CellType.MINE

    def _initialize_mine_neighbor(self, width: int, height: int):
        for w, h, indexes in _get_neighbor_indexes(width, height):
            if self[w, h].cell_type == CellType.MINE:
                continue

            bomb_num = sum([1 for x, y in indexes if self[w+x, h+y].cell_type == CellType.MINE])
            if bomb_num > 0:
                self[w, h].NEIGHBOR_MINE_NUM = bomb_num
                self[w, h].cell_type = CellType.NUM

    def __getitem__(self, idx) -> Grid:
        return self.board[idx[1]][idx[0]]


class MineSweeper:
    def __init__(self, master: tk.Tk, bomb_num: int, width: int, height: int):
        self.master = master
        self.BOMB_NUM = bomb_num
        self.WIDTH = width
        self.HEIGHT = height
        self.board = Board(bomb_num, width, height, master)


if __name__ == "__main__":
    width = 10
    height = 10
    bomb_num = 10
    board = Board(bomb_num, width, height)

    for w in range(width):
        for h in range(height):
            if board[w, h].cell_type == CellType.MINE:
                print("X", end="")
            elif board[w, h].cell_type == CellType.NUM:
                print(board[w, h].NEIGHBOR_MINE_NUM, end="")
            else:
                print("N", end="")

        print()