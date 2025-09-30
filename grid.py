from random import sample
from selection import SelectNumber
from copy import deepcopy

SUB_GRID_SIZE = 3
GRID_SIZE = SUB_GRID_SIZE * SUB_GRID_SIZE


def create_line_coordinates(cell_size: int) -> list[list[tuple]]:
    """ Creates the x,y coordinates for drawing the grid lines. """
    points = []
    for y in range(1, 9):
        # horizontal lines
        temp = []
        temp.append((0, y * cell_size))     # x,y points [(0, 100), (0, 200), (0, 300), (0, 400) ...]
        temp.append((900, y * cell_size))   # x,y points [(900, 100), (900, 200), (900, 300), (900, 400) ...]
        points.append(temp)

    for x in range(1, 10):
        # vertical lines - from 1 to 10, to close the grid on the right side
        temp = []
        temp.append((x * cell_size, 0))     # x,y points [(100, 0), (200, 0), (300, 0), (400, 0) ...]
        temp.append((x * cell_size, 900))   # x,y points [(100, 900), (200, 900), (300, 900), (400, 900) ...]
        points.append(temp)
    return points


def pattern(row_num: int, col_num: int) -> int:
    return (SUB_GRID_SIZE * (row_num % SUB_GRID_SIZE) + row_num // SUB_GRID_SIZE + col_num) % GRID_SIZE


def shuffle(samp: range) -> list:
    return sample(samp, len(samp))


def create_grid(sub_grid: int) -> list[list]:
    """ Creates the 9x9 grid filled with random numbers. """
    row_base = range(sub_grid)
    rows = [g * sub_grid + r for g in shuffle(row_base) for r in shuffle(row_base)]
    cols = [g * sub_grid + c for g in shuffle(row_base) for c in shuffle(row_base)]
    nums = shuffle(range(1, sub_grid * sub_grid + 1))
    return [[nums[pattern(r, c)] for c in cols] for r in rows]


def remove_numbers(grid: list[list]) -> None:
    """ Randomly sets numbers to zeros on the grid. """
    num_of_cells = GRID_SIZE * GRID_SIZE
    empties = num_of_cells * 3 // 7  # 7 is ideal - higher this number means easier game
    for i in sample(range(num_of_cells), empties):
        grid[i // GRID_SIZE][i % GRID_SIZE] = 0


class Grid:
    def __init__(self, pygame, font):
        self.selected_cell = None
        self.cell_size = 100
        self.grid_origin = (50, 50)
        self.num_x_offset = 35
        self.num_y_offset = 12
        self.line_coordinates = create_line_coordinates(self.cell_size)
        self.win = False
        self.game_font = font

        self.grid = create_grid(SUB_GRID_SIZE)
        self.__test_grid = deepcopy(self.grid)
        remove_numbers(self.grid)
        self.occupied_cell_coordinates = self.pre_occupied_cells()
        self.selected_cell = None

    def restart(self) -> None:
        self.grid = create_grid(SUB_GRID_SIZE)
        self.__test_grid = deepcopy(self.grid)
        remove_numbers(self.grid)
        self.occupied_cell_coordinates = self.pre_occupied_cells()
        self.win = False

    def check_grids(self):
        """ Checks if all the cells in the main grid and the test grid are equal. """
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                if self.grid[y][x] != self.__test_grid[y][x]:
                    return False
        return True

    def is_cell_preoccupied(self, x: int, y: int) -> bool:
        """ Check for non-playable cells - preoccupied/initialized cells."""
        for cell in self.occupied_cell_coordinates:
            if x == cell[1] and y == cell[0]:
                return True
        return False

    def get_mouse_click(self, x, y):
        grid_x, grid_y = self.grid_origin
        if grid_x <= x < grid_x + 9 * self.cell_size and grid_y <= y < grid_y + 9 * self.cell_size:
            row = (y - grid_y) // self.cell_size
            col = (x - grid_x) // self.cell_size
            self.selected_cell = (int(row), int(col))
        else:
            self.selected_cell = None
    
    def set_cell_value(self, pos, value):
        row, col = pos
        if not self.is_cell_preoccupied(col,row):
            self.grid[row][col] = value
            
    def pre_occupied_cells(self) -> list[tuple]:
        """ Gather the y,x coordinates for all preoccupied/initialized cells. """
        occupied_cell_coordinates = []
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                if self.get_cell(x, y) != 0:
                    occupied_cell_coordinates.append((y, x))  # first the row, then the column: y,x
        return occupied_cell_coordinates

    def __draw_lines(self, pg, surface) -> None:
        """ Draws the grid lines. """
        for index, point in enumerate(self.line_coordinates):
            if index == 2 or index == 5 or index == 10 or index == 13:
                pg.draw.line(surface, (255, 200, 0), point[0], point[1])
            else:
                pg.draw.line(surface, (0, 50, 0), point[0], point[1])

    def __draw_numbers(self, surface) -> None:
        """ Draw the grid numbers. """
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                if self.get_cell(x, y) != 0:
                    if (y, x) in self.occupied_cell_coordinates:
                        text_surface = self.game_font.render(str(self.get_cell(x, y)), False, (0, 200, 255))
                    else:
                        text_surface = self.game_font.render(str(self.get_cell(x, y)), False, (0, 255, 0))

                    if self.get_cell(x, y) != self.__test_grid[y][x]:  # self.grid[y][x] != self.__test_grid[y][x]
                        text_surface = self.game_font.render(str(self.get_cell(x, y)), False, (255, 0, 0))

                    surface.blit(text_surface, (x * self.cell_size + self.num_x_offset, y * self.cell_size + self.num_y_offset))

    def draw_all(self, pg, surface):
        """ Draw everything here. """
        self.__draw_lines(pg, surface)
        self.__draw_numbers(surface)

    def get_cell(self, x: int, y: int) -> int:
        """ Get a cell value at y,x coordinate. """
        return self.grid[y][x]

    def set_cell(self, x: int, y: int, value: int) -> None:
        """ Set a cell value at y,x coordinate. """
        self.grid[y][x] = value

    def show(self):
        """ Prints the grid row by row to the output. """
        for row in self.grid:
            print(row)


if __name__ == "__main__":
    import pygame
    pygame.font.init()
    game_font = pygame.font.SysFont('Comic Sans MS', 50)
    grid = Grid(pygame, game_font)
    grid.show()
