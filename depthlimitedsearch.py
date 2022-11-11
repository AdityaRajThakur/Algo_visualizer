import time
import pygame
from queue import PriorityQueue
from plyer import notification
WIDTH = 800
HEIGHT = 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Depth First Search Algorithm")
DEPTH = 1
ITR = 0
RED = (255, 0, 0)
GREEN = (0, 255, 0)
LGREEN = (17, 241, 10)
DGREEN = (34, 129, 6)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (158, 0, 255)
ORANGE = (255, 165, 0)
GREY = (188, 174, 174)
BLUE = (4, 34, 252)


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
		# DOWN
		if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():
			self.neighbors.append(grid[self.row + 1][self.col])

		if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():  # UP
			self.neighbors.append(grid[self.row - 1][self.col])

		# RIGHT
		if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():
			self.neighbors.append(grid[self.row][self.col + 1])

		if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():  # LEFT
			self.neighbors.append(grid[self.row][self.col - 1])

	def __lt__(self, other):
		return False


def reconstruct_path(came_from, first, current, draw):
	while current in came_from:
		current = came_from[current]
		if first != current:
                   current.make_path()
                   draw()


def ntf(message):
	notification.notify(title="Depth First search",
	                    message=message, timeout=2, toast=True)


def dfs(draw, start, end,DEPTH):
    start_time = time.time()
    print("hello world ")
    count = 0
    stack = [(count, start)]
    visited = {start}
    prev = {}
    first = start
    size = len(stack)
    print(size)
    ITR  = 0 
    while(size != 0):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = stack.pop()[1]
        ITR+= 1
        # visited.remove(current)
        if current == end:
            reconstruct_path(prev, first, end, draw)
            #visited.clear()
            end.make_end()
            end_time = time.time()
            return True, end_time-start_time

        for neighbor in current.neighbors:
                if neighbor not in visited:
                    count += 1
                    prev[neighbor] = current
                    stack.append((count, neighbor))
                    visited.add(neighbor)

                    neighbor.make_open() # if you want to see the visited node
        size = len(stack)
        draw()
        if current != start:
            current.make_closed()
        if ITR==DEPTH:
            stack.clear()
        
            stack.append((0,current))
            
    visited.clear()
    end_time = time.time()
    
    return False,end_time - start_time   

def depth_limited_search(draw ,start ,end):
    DEPTH = 1 
	
    while(True):
        dfs(draw , start , end,DEPTH)
        DEPTH+=1
    
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
	ROWS = 20
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

					find,etime = depth_limited_search(lambda: draw(win, grid, ROWS, width),start, end)
					if find :
						ntf(f"Path Found And Time Taken : {etime} sec")
					else:
						ntf(f"Path Not Found And Time Taken : {etime} sec")
				if event.key == pygame.K_c:
					start = None
					end = None
					grid = make_grid(ROWS, width)

	pygame.quit()

main(WIN, WIDTH)
