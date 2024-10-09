import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
BLOCK_SIZE = 50
GRID_SIZE = 25
WINDOW_SIZE = (GRID_SIZE * BLOCK_SIZE, GRID_SIZE * BLOCK_SIZE)

# Function to generate a random color (RGB)
def random_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

# Predefined color list (expanded)
PREDEFINED_COLORS = [
    (255, 0, 0),   # Red
    (0, 255, 0),   # Green
    (0, 0, 255),   # Blue
    (255, 255, 0), # Yellow
    (255, 165, 0), # Orange
    (128, 0, 128), # Purple
    (0, 255, 255), # Cyan
    (255, 192, 203), # Pink
    random_color(),  # Random color 1
    random_color()   # Random color 2
]

# Create window
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Slide and Match with Random Colors")

# Generate the initial grid with random colors
def generate_grid(size):
    return [[random.choice(PREDEFINED_COLORS) for _ in range(size)] for _ in range(size)]

def draw_grid(grid):
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            pygame.draw.rect(screen, grid[row][col], (col * BLOCK_SIZE, row * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

def check_for_matches(grid):
    # Check for any horizontal, vertical, or diagonal matches of 3 or more
    pass  # Add your matching logic here

def expand_grid(grid):
    # Expand grid size by adding more rows/columns
    new_row = [random.choice(PREDEFINED_COLORS) for _ in range(len(grid) + 1)]
    for row in grid:
        row.append(random.choice(PREDEFINED_COLORS))  # Add a new column to each row
    grid.append(new_row)  # Add a new row at the bottom
    return grid

def get_block_at_pos(pos):
    """ Returns the row, col of the block based on mouse position. """
    x, y = pos
    col = x // BLOCK_SIZE
    row = y // BLOCK_SIZE
    if row < GRID_SIZE and col < GRID_SIZE:
        return row, col
    return None, None

def move_block(grid, start_pos, end_pos):
    """ Move the block to a new position and swap the positions in the grid. """
    if start_pos and end_pos:
        start_row, start_col = start_pos
        end_row, end_col = end_pos
        grid[start_row][start_col], grid[end_row][end_col] = grid[end_row][end_col], grid[start_row][start_col]

def random_move(grid):
    """ Move random blocks to adjacent positions """
    for _ in range(2):  # You can control how many blocks move
        row, col = random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1)
        direction = random.choice(["up", "down", "left", "right"])
        
        if direction == "up" and row > 0:
            move_block(grid, (row, col), (row - 1, col))
        elif direction == "down" and row < GRID_SIZE - 1:
            move_block(grid, (row, col), (row + 1, col))
        elif direction == "left" and col > 0:
            move_block(grid, (row, col), (row, col - 1))
        elif direction == "right" and col < GRID_SIZE - 1:
            move_block(grid, (row, col), (row, col + 1))

# Initial grid
grid = generate_grid(GRID_SIZE)

# Variables to handle block dragging
dragging = False
selected_block = None
original_pos = None

# Game loop
running = True
while running:
    screen.fill((255, 255, 255))  # White background
    draw_grid(grid)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Mouse button down event - Start dragging the block
        if event.type == pygame.MOUSEBUTTONDOWN:
            original_pos = get_block_at_pos(pygame.mouse.get_pos())
            if original_pos:
                dragging = True
                selected_block = original_pos  # Store the block being moved
        
        # Mouse button up event - Snap block to the nearest position
        if event.type == pygame.MOUSEBUTTONUP:
            if dragging:
                new_pos = get_block_at_pos(pygame.mouse.get_pos())
                move_block(grid, original_pos, new_pos)
                dragging = False
                selected_block = None

                # After the player moves, trigger random block movements
                random_move(grid)

    # If dragging, visually follow the mouse cursor
    if dragging and selected_block:
        row, col = selected_block
        mouse_x, mouse_y = pygame.mouse.get_pos()
        pygame.draw.rect(screen, grid[row][col], (mouse_x - BLOCK_SIZE // 2, mouse_y - BLOCK_SIZE // 2, BLOCK_SIZE, BLOCK_SIZE))

    # Check for matches and expand the grid if necessary
    if check_for_matches(grid):
        grid = expand_grid(grid)  # Expand the grid if a match is found

    pygame.display.update()

pygame.quit()
