import pygame
import time
import math
from queue import PriorityQueue
from plyer import notification
WIDTH = 800
HEIGHT = 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("A* Algorithm")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
LGREEN = (17, 241, 10)
DGREEN  = (34, 129, 6 )
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (158, 0, 255)
ORANGE = (255, 165 ,0)
GREY = (188, 174, 174 )
BLUE = (4, 34, 252 )

class Node:
	def __init__(self, row, col, width, total_rows):
		self.row = row
		self.col = col
		self.x = row * width
		self.y = col * width
		self.color = WHITE
		self.neighbors = []
		self.width = width
		self.total_rows = total_rows

	def get_pos(self):
		return self.row, self.col

	def is_closed(self):
		return self.color == RED

	def is_open(self):
		return self.color == GREEN

	def is_barrier(self):
		return self.color == BLACK

	def is_start(self):
		return self.color == YELLOW 

	def is_end(self):
		return self.color == GREY

	def reset(self):
		self.color = WHITE

	def make_start(self):
		self.color = YELLOW 

	def make_closed(self):
		self.color = RED

	def make_open(self):
		self.color = GREEN

	def make_barrier(self):
		self.color = BLACK

	def make_end(self):
		self.color = GREY

	def make_path(self):
		self.color = LGREEN

	def draw(self, win):
		pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

	def update_neighbors(self, grid):
		self.neighbors = []
		if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # DOWN
			self.neighbors.append(grid[self.row + 1][self.col])

		if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # UP
			self.neighbors.append(grid[self.row - 1][self.col])

		if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): # RIGHT
			self.neighbors.append(grid[self.row][self.col + 1])

		if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # LEFT
			self.neighbors.append(grid[self.row][self.col - 1])

	def __lt__(self, other):
		return False


def h(p1, p2):
	x1, y1 = p1
	x2, y2 = p2
	return ((x1 - x2)**2 + (y1 - y2)**2 )**2 

def ntf(message):
    notification.notify(title = "A* Algorithm",message = message ,timeout = 2 ,toast = True)

def reconstruct_path(came_from, first, current, draw):
	while current in came_from:
		current = came_from[current]
		if first!=current :
                   current.make_path()
                   draw()
 
def astar(draw, grid, start, end):
	count = 0
	pq = PriorityQueue()
	pq.put((0, count, start))
	prev = {}
	g_value = {node: float("inf") for row in grid for node in row}
	g_value[start] = 0
	f_value = {node: float("inf") for row in grid for node in row}
	f_value[start] = h(start.get_pos(), end.get_pos())

	visited = {start}
	first_node = start

	while not pq.empty():
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		current = pq.get()[2]
		visited.remove(current)

		if current == end:
			reconstruct_path(prev,first_node, end, draw)
			end.make_end()
			return True

		for neighbor in current.neighbors:
			temp_g_value = g_value[current] + 1

			if temp_g_value < g_value[neighbor]:
				prev[neighbor] = current
				g_value[neighbor] = temp_g_value
				f_value[neighbor] = temp_g_value + h(neighbor.get_pos(), end.get_pos())
				if neighbor not in visited:
					count += 1
					pq.put((f_value[neighbor], count, neighbor))
					visited.add(neighbor)
					# neighbor.make_open()

		draw()
		if current != start:
			current.make_closed()
		
			
	
	return False


def make_grid(rows, width):
	grid = []
	gap = width // rows
	for i in range(rows):
		grid.append([])
		for j in range(rows):
			node = Node(i, j, gap, rows)
			grid[i].append(node)

	return grid

def draw_grid(win, rows, width):
	gap = width // rows
	for i in range(rows):
		pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
		for j in range(rows):
			pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))


def draw(win, grid, rows, width):
	win.fill(WHITE)

	for row in grid:
		for node in row:
			node.draw(win)

	draw_grid(win, rows, width)
	pygame.display.update()


def get_clicked_pos(pos, rows, width):
	gap = width // rows
	y, x = pos

	row = y // gap
	col = x // gap

	return row, col


def main(win, width):
	ROWS = 50
	grid = make_grid(ROWS, width)

	start = None
	end = None

	run = True
	while run:
		draw(win, grid, ROWS, width)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

			if pygame.mouse.get_pressed()[0]: # LEFT
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, width)
				node = grid[row][col]
				if not start and node != end:
					start = node
					start.make_start()

				elif not end and node != start:
					end = node
					end.make_end()

				elif node != end and node != start:
					node.make_barrier()

			elif pygame.mouse.get_pressed()[2]: # RIGHT
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, width)
				node = grid[row][col]
				node.reset()
				if node == start:
					start = None
				elif node == end:
					end = None
			find = False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE and start and end:
					for row in grid:
						for node in row:
							node.update_neighbors(grid)
					start_time = time.time()
					find= astar(lambda: draw(win, grid, ROWS, width), grid, start, end) 
					end_time = time.time()
					if find : 
						ntf(f"Path Found And Time Taken : {end_time-start_time} sec")
					else:
						ntf(f"Path Not Found And Time Taken : {end_time-start_time} sec")
				if event.key == pygame.K_c:
					start = None
					end = None
					grid = make_grid(ROWS, width)

	pygame.quit()

main(WIN, WIDTH)