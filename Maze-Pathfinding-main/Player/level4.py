import pygame
import numpy as np

# colors
one = (79, 189, 186)
two = (206, 171, 147)
three = (227, 202, 165)
four = (255, 251, 233)
five = (246, 137, 137)
six = (255, 0, 0)
seven = (0, 255, 0)

pygame.init()

size = (900, 730)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("MAZE")

width = 20
height = 20
margin = 2

grid = [[0 for x in range(33)] for y in range(33)]

done = False
clock = pygame.time.Clock()
found = False
neighbour = []

# Các biến theo dõi thông số
steps_taken = 0
start_time = 0
elapsed_time = 0
time_end = 0
reached_destination = False  # Biến kiểm tra đã đến đích hay chưa

player_position = (0, 0)
destination = (0, 0)

def loadgrid():
    global grid, player_position, destination
    grid = np.loadtxt(r"Maze\lv4.txt").tolist()
    # Cập nhật vị trí ban đầu của người chơi và đích
    for row in range(len(grid)):
        for column in range(len(grid[0])):
            if grid[row][column] == 2:
                player_position = (row, column)
            elif grid[row][column] == 3:
                destination = (row, column)

def move_player(direction):
    global player_position, steps_taken, reached_destination

    # Kiểm tra đã đến đích hay chưa
    if reached_destination:
        return

    # Chuyển player_position thành list để có thể thay đổi giá trị
    new_position = list(player_position)

    # Xác định hướng di chuyển và cập nhật vị trí mới
    if direction == "UP" and player_position[0] > 0:
        new_position[0] -= 1
    elif direction == "DOWN" and player_position[0] < len(grid) - 1:
        new_position[0] += 1
    elif direction == "LEFT" and player_position[1] > 0:
        new_position[1] -= 1
    elif direction == "RIGHT" and player_position[1] < len(grid[0]) - 1:
        new_position[1] += 1

    # Kiểm tra xem vị trí mới có hợp lệ không (không đi vào ô cấm)
    if grid[new_position[0]][new_position[1]] != 1:
        # Đặt lại ô hiện tại của người chơi
        grid[player_position[0]][player_position[1]] = 0
        # Cập nhật vị trí mới của người chơi
        player_position = tuple(new_position)
        # Đặt lại ô mới của người chơi
        grid[player_position[0]][player_position[1]] = 2
        draw_grid()
        steps_taken += 1

        if player_position == destination:
            print("Congratulations! You've reached the destination!")
            elapsed_time = (pygame.time.get_ticks() - start_time) / 1000
            print(f"Steps: {steps_taken}")
            print(f"Time: {elapsed_time:.2f} seconds")
            reached_destination = True

def draw_grid():
    global time_end
    for row in range(33):
        for column in range(33):
            if grid[row][column] == 1:
                color = three
            elif grid[row][column] == 2:
                color = one
            elif grid[row][column] == 3:
                color = five
            elif grid[row][column] == 4:
                color = one
            elif grid[row][column] == 5:
                color = six
            elif grid[row][column] == 6:
                color = seven
            else:
                color = four
            pygame.draw.rect(screen, color, [margin + (margin + width) * column, margin + (margin + height) * row, width, height])
    
    # Hiển thị thời gian và số bước đi trực tiếp trên cửa sổ
    font = pygame.font.SysFont(None, 26)
    steps_text = font.render(f"Steps: {steps_taken}", True, (255, 255, 255))

    if not reached_destination:
        elapsed_time = (pygame.time.get_ticks() - start_time) / 1000
        time_text = font.render(f"Time: {elapsed_time:.2f} seconds", True, (255, 255, 255))
        screen.blit(time_text, (730, 20))
    screen.blit(steps_text, (730, 0))

def draw_button(text, x, y, width, height, inactive_color, active_color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        pygame.draw.rect(screen, active_color, (x, y, width, height))
        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(screen, inactive_color, (x, y, width, height))

    small_text = pygame.font.SysFont(None, 20)
    text_surf, text_rect = text_objects(text, small_text)
    text_rect.center = ((x + (width / 2)), (y + (height / 2)))
    screen.blit(text_surf, text_rect)

def text_objects(text, font):
    text_surface = font.render(text, True, (0, 0, 0))
    return text_surface, text_surface.get_rect()

def reset_game():
    global steps_taken, elapsed_time, player_position, destination, start_time, reached_destination
    steps_taken = 0
    elapsed_time = 0
    player_position = (0, 0)
    destination = (0, 0)
    start_time = pygame.time.get_ticks()
    reached_destination = False  # Reset biến khi reset game
    loadgrid()

loadgrid()
start_time = pygame.time.get_ticks()

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                print("Exit")
                pygame.quit()
            if event.key == pygame.K_UP:
                move_player("UP")
            elif event.key == pygame.K_DOWN:
                move_player("DOWN")
            elif event.key == pygame.K_LEFT:
                move_player("LEFT")
            elif event.key == pygame.K_RIGHT:
                move_player("RIGHT")
            elif event.key == pygame.K_w:
                move_player("UP")
            elif event.key == pygame.K_s:
                move_player("DOWN")
            elif event.key == pygame.K_a:
                move_player("LEFT")
            elif event.key == pygame.K_d:
                move_player("RIGHT")
            if event.key == pygame.K_r:
                reset_game()

    screen.fill(two)
    draw_grid()

    # Vẽ nút reset
    draw_button("Reset", 770, 670, 80, 40, (128, 128, 128), (169, 169, 169), reset_game)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
