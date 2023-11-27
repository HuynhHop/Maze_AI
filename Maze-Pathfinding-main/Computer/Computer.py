import pygame
import numpy as np
from queue import PriorityQueue
import time

#colors
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
neighbour=[]

player_position = (0, 0)  # Vị trí ban đầu của đối tượng
destination = (0, 0)  # Vị trí của điểm đến (đích)

# Các biến theo dõi thông số
steps_taken = 0
vertices_explored = 0
# Trước khi vào hàm a_star
start_time = pygame.time.get_ticks()
elapsed_time = 0


def savegrid():
    global grid
    np.savetxt(r"D:\Maze-Pathfinding-main\Map\maze.txt",grid)
def loadgrid(index):
    global grid
    if(index ==0):
        grid = np.loadtxt(r"D:\Maze-Pathfinding-main\Map\maze.txt").tolist()
    elif(index ==1):
        grid = np.loadtxt(r'D:\Maze-Pathfinding-main\Map\Maze1\maze.txt').tolist()
    elif(index ==2):
        grid = np.loadtxt(r'D:\Maze-Pathfinding-main\Map\Maze2\maze.txt').tolist()
    elif(index ==3):
        grid = np.loadtxt(r'D:\Maze-Pathfinding-main\Map\Maze3\maze.txt').tolist()
    elif(index ==4):
        grid = np.loadtxt(r'D:\Maze-Pathfinding-main\Map\Maze4\maze.txt').tolist()
    elif(index ==5):
        grid = np.loadtxt(r'D:\Maze-Pathfinding-main\Map\Maze5\maze.txt').tolist()
            
def neighbourr():
    global grid,neighbour
    neighbour = [[]for col in range(len(grid)) for row in range(len(grid))]
    count=0
    for i in range(len(grid)):
        for j in range(len(grid)):
            neighbour[count] == []
            if (i > 0 and grid[i - 1][j] != 1):
                neighbour[count].append((i-1,j))
            if (j > 0 and grid[i][j - 1] != 1):
                neighbour[count].append((i,j-1))
            if (i < len(grid) - 1 and grid[i + 1][j] != 1):
                neighbour[count].append((i+1,j))
            if (j < len(grid) - 1 and grid[i][j + 1] != 1):
                neighbour[count].append((i,j+1))
            count+=1    
            
def h(p1, p2):
	x1, y1 = p1
	x2, y2 = p2
	return abs(x1 - x2) + abs(y1 - y2)

def S_E(maze,start,end):
    for x in range(len(grid)):
        for y in range(len(grid[x])):
            if(grid[x][y]==2):
                start =x,y
            if(grid[x][y]==3):
                end =x,y
       
    return start,end

def short_path(came_from, current):
     global steps_taken
     grid[current[0]][current[1]] = 4
     while current in came_from:
         current = came_from[current]
         grid[current[0]][current[1]] = 4
         draw_grid()
         steps_taken += 1

# Function to check if the mouse is over the A* button
def is_over_a_star_button(mouse_pos):
    button_rect = pygame.Rect(730, 60, 120, 20)  # Smaller A* button rectangle
    return button_rect.collidepoint(mouse_pos)

# Function to check if the mouse is over the BFS button
def is_over_dfs_button(mouse_pos):
    button_rect = pygame.Rect(730, 90, 120, 20)  # Smaller BFS button rectangle, positioned below A*
    return button_rect.collidepoint(mouse_pos)

# Function to draw the A* button
def draw_a_star_button():
    pygame.draw.rect(screen, (100, 100, 100), [730, 60, 120, 20])  # Smaller A* button background
    font = pygame.font.SysFont(None, 18)  # Smaller font size
    text = font.render("A*", True, (255, 255, 255))
    screen.blit(text, (735, 65))

# Function to draw the BFS button
def draw_dfs_button():
    pygame.draw.rect(screen, (100, 100, 100), [730, 90, 120, 20])  # Smaller BFS button background, positioned below A*
    font = pygame.font.SysFont(None, 18)  # Smaller font size
    text = font.render("DFS", True, (255, 255, 255))
    screen.blit(text, (735, 95))

def is_over_reset_button(mouse_pos):
    button_rect = pygame.Rect(730, 120, 120, 20)  # Rectangle for the Reset button
    return button_rect.collidepoint(mouse_pos)

# Function to draw the Reset button
def draw_reset_button():
    pygame.draw.rect(screen, (100, 100, 100), [730, 120, 120, 20])  # Reset button background
    font = pygame.font.SysFont(None, 18)  # Font size
    text = font.render("Reset", True, (255, 255, 255))
    screen.blit(text, (765, 125))


def a_star():
    global grid, neighbour
    global steps_taken, vertices_explored, start_time, elapsed_time
    start_time = pygame.time.get_ticks()
    neighbourr()

    start, end = S_E(grid, 0, 0)
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    open_set_his = {start}
    came_from = {}

    g_score = [float("inf") for row in grid for spot in row]
    g_score[start[0] * len(grid[0]) + start[1]] = 0
    f_score = [float("inf") for row in grid for spot in row]
    f_score[start[0] * len(grid[0]) + start[1]] = h(start, end)

    while not open_set.empty():
        current = open_set.get()[2]
        open_set_his.remove(current)
        if current == end:
            print("finishing")
            short_path(came_from, end)
            # Sau khi vòng lặp kết thúc
            end_time = pygame.time.get_ticks()
            elapsed_time = (end_time - start_time) / 1000.0
            print(f"Algorithm finished in {elapsed_time:.2f} seconds")
            return True
        
        for nei in neighbour[current[0] * len(grid[0]) + current[1]]:
            temp_g_score = g_score[current[0] * len(grid[0]) + current[1]] + 1
            if temp_g_score < g_score[nei[0] * len(grid[0]) + nei[1]]:
                came_from[nei] = current
                g_score[nei[0] * len(grid[0]) + nei[1]] = temp_g_score
                f_score[nei[0] * len(grid[0]) + nei[1]] = temp_g_score + h(nei, end)
                if nei not in open_set_his:
                    count += 1
                    open_set.put((f_score[nei[0] * len(grid[0]) + nei[1]], count, nei))
                    open_set_his.add(nei)
                    grid[nei[0]][nei[1]] = 5
                    draw_grid()  # Thêm hàm vẽ sau khi cập nhật ô
                    #pygame.time.delay(100)

        if current != start:
            vertices_explored += 1
            grid[current[0]][current[1]] = 6
            draw_grid()
            #pygame.time.delay(100)

    # Sau khi vòng lặp kết thúc
    end_time = pygame.time.get_ticks()
    elapsed_time = (end_time - start_time) / 1000.0
    print(f"Algorithm finished in {elapsed_time:.2f} seconds")

    return False

def dfs_step_by_step():
    global grid, neighbour
    global grid, neighbour
    global steps_taken, vertices_explored, start_time, elapsed_time
    neighbourr()

    start, end = S_E(grid, 0, 0)
    stack = [start]
    visited = set()
    came_from = {}

    while stack:
        current = stack.pop()

        if current == end:
            print("finishing")
            short_path(came_from, end)  # Visualize the short path
            # Sau khi vòng lặp kết thúc
            end_time = pygame.time.get_ticks()
            elapsed_time = (end_time - start_time) / 1000.0
            print(f"Algorithm finished in {elapsed_time:.2f} seconds")
            return True

        if current not in visited:
            visited.add(current)
            grid[current[0]][current[1]] = 5  # Visualize the exploration
            draw_grid()
            #pygame.time.delay(50)  # Adjust the delay as needed

            for nei in neighbour[current[0] * len(grid[0]) + current[1]]:
                if nei not in visited:
                    stack.append(nei)
                    came_from[nei] = current  # Store the path information

        if current != start:
            vertices_explored += 1
            grid[current[0]][current[1]] = 6  # Visualize backtracking
            draw_grid()  # Thêm hàm vẽ sau khi cập nhật ô
            #pygame.time.delay(50)  # Uncomment if needed for a delay during backtracking

    # Sau khi vòng lặp kết thúc
    end_time = pygame.time.get_ticks()
    elapsed_time = (end_time - start_time) / 1000.0
    print(f"Algorithm finished in {elapsed_time:.2f} seconds")

    return False



def draw_grid():
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
    pygame.display.flip()



while not done:
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
             if event.key == pygame.K_ESCAPE:
                    print("Exit")
                    pygame.quit()
             if event.key == pygame.K_s:
                 print("Saving Maze")
                 savegrid()
             if event.key == pygame.K_l:
                 print("Loading Maze")
                 loadgrid(0)
             if event.key == pygame.K_f:
                 print("Filling Maze")
                 grid = [[1 for x in range(33)] for y in range(33)]
             if event.key == pygame.K_1:
                 print("Loading Maze 1")
                 loadgrid(1)
             if event.key == pygame.K_2:
                 print("Loading Maze 2")
                 loadgrid(2)
             if event.key == pygame.K_3:
                 print("Loading Maze 3")
                 loadgrid(3)
             if event.key == pygame.K_4:
                 print("Loading Maze 4")
                 loadgrid(4)
             if event.key == pygame.K_5:
                 print("Loading Maze 5")
                 loadgrid(5)
             if event.key == pygame.K_r:
                grid = [[0 for x in range(33)] for y in range(33)]
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = pygame.mouse.get_pos()  # Move this line inside the event loop
            if is_over_a_star_button(pos):
                print("Running A* Algorithm")
                a_star()
                # dfs_step_by_step();
            elif is_over_dfs_button(pos):
                print("Running DFS Algorithm")
                dfs_step_by_step();                
            elif is_over_reset_button(pos):
                print("Resetting Maze")
                grid = [[0 for x in range(33)] for y in range(33)]
        if pygame.mouse.get_pressed()[2]:
            column = pos[0] // (width + margin)
            row = pos[1] // (height + margin)
            if((sum(x.count(2) for x in grid)) < 1 or (sum(x.count(3) for x in grid)) < 1):
                if((sum(x.count(2) for x in grid)) == 0):
                    if(grid[row][column] == 2):
                        grid[row][column] = 0
                    elif(grid[row][column] == 3):
                        grid[row][column] = 0
                    else:
                        grid[row][column]  = 2
                else:
                    if(grid[row][column] == 3):
                        grid[row][column] = 0
                    elif(grid[row][column] == 2):
                        grid[row][column] = 0
                    else:
                        grid[row][column]  = 3
            else:
                if(grid[row][column] == 2):
                    grid[row][column] = 0
                if(grid[row][column] == 3):
                    grid[row][column] = 0
                if(grid[row][column] == 1):
                    grid[row][column] = 0
        if pygame.mouse.get_pressed()[0]:
            column = pos[0] // (width + margin)
            row = pos[1] // (height + margin)

            # Kiểm tra xem row và column có nằm trong phạm vi hợp lệ không
            if 0 <= row < len(grid) and 0 <= column < len(grid[0]):
                print("left click")
                grid[row][column] = 1
        
                
    pos = pygame.mouse.get_pos()
    x = pos[0]
    y = pos[1]
    screen.fill(two)
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

    # Hiển thị các thông số trực tiếp trên cửa sổ
    font = pygame.font.SysFont(None, 26)
    steps_text = font.render(f"Steps: {steps_taken}", True, (255, 255, 255))
    vertices_text = font.render(f"Vertices: {vertices_explored}", True, (255, 255, 255))
    time_text = font.render(f"Time: {elapsed_time:.2f} ms", True, (255, 255, 255))

    screen.blit(steps_text, (730, 0))
    screen.blit(vertices_text, (730, 20))
    screen.blit(time_text, (730, 40))

    draw_a_star_button()
    draw_dfs_button()
    draw_reset_button()
    
    pygame.display.flip()
    clock.tick(60)
pygame.quit()


# import pygame
# import numpy as np
# from queue import PriorityQueue
# import time

# #colors
# one = (79, 189, 186)
# two = (206, 171, 147)
# three = (227, 202, 165)
# four = (255, 251, 233)
# five = (246, 137, 137)
# six = (255, 0, 0)
# seven = (0, 255, 0)

# pygame.init()

# size = (900, 730)
# screen = pygame.display.set_mode(size)

# pygame.display.set_caption("MAZE")

# width = 20
# height = 20
# margin = 2

# grid = [[0 for x in range(33)] for y in range(33)]

# done = False
# clock = pygame.time.Clock()
# found = False
# neighbour=[]

# player_position = (0, 0)  # Vị trí ban đầu của đối tượng
# destination = (0, 0)  # Vị trí của điểm đến (đích)

# # Các biến theo dõi thông số
# steps_taken = 0
# vertices_explored = 0
# # Trước khi vào hàm a_star
# start_time = pygame.time.get_ticks()
# elapsed_time = 0


# def savegrid():
#     global grid
#     np.savetxt(r"D:\Maze-Pathfinding-main\maze.txt",grid)
# def loadgrid(index):
#     global grid
#     if(index ==0):
#         grid = np.loadtxt(r"D:\Maze-Pathfinding-main\maze.txt").tolist()
#     elif(index ==1):
#         grid = np.loadtxt(r'D:\Maze-Pathfinding-main\Maze1\maze.txt').tolist()
#     elif(index ==2):
#         grid = np.loadtxt(r'D:\Maze-Pathfinding-main\Maze2\maze.txt').tolist()
#     elif(index ==3):
#         grid = np.loadtxt(r'D:\Maze-Pathfinding-main\Maze3\maze.txt').tolist()
#     elif(index ==4):
#         grid = np.loadtxt(r'D:\Maze-Pathfinding-main\Maze4\maze.txt').tolist()
#     elif(index ==5):
#         grid = np.loadtxt(r'D:\Maze-Pathfinding-main\Maze5\maze.txt').tolist()
            
# def neighbourr():
#     global grid,neighbour
#     neighbour = [[]for col in range(len(grid)) for row in range(len(grid))]
#     count=0
#     for i in range(len(grid)):
#         for j in range(len(grid)):
#             neighbour[count] == []
#             if (i > 0 and grid[i - 1][j] != 1):
#                 neighbour[count].append((i-1,j))
#             if (j > 0 and grid[i][j - 1] != 1):
#                 neighbour[count].append((i,j-1))
#             if (i < len(grid) - 1 and grid[i + 1][j] != 1):
#                 neighbour[count].append((i+1,j))
#             if (j < len(grid) - 1 and grid[i][j + 1] != 1):
#                 neighbour[count].append((i,j+1))
#             count+=1    
            
# def h(p1, p2):
# 	x1, y1 = p1
# 	x2, y2 = p2
# 	return abs(x1 - x2) + abs(y1 - y2)

# def S_E(maze,start,end):
#     for x in range(len(grid)):
#         for y in range(len(grid[x])):
#             if(grid[x][y]==2):
#                 start =x,y
#             if(grid[x][y]==3):
#                 end =x,y
       
#     return start,end

# def short_path(came_from, current):
#      global steps_taken
#      grid[current[0]][current[1]] = 4
#      while current in came_from:
#          current = came_from[current]
#          grid[current[0]][current[1]] = 4
#          draw_grid()
#          steps_taken += 1
        

# def a_star():
#     global grid, neighbour
#     global steps_taken, vertices_explored, start_time, elapsed_time
#     start_time = pygame.time.get_ticks()
#     neighbourr()

#     start, end = S_E(grid, 0, 0)
#     count = 0
#     open_set = PriorityQueue()
#     open_set.put((0, count, start))
#     open_set_his = {start}
#     came_from = {}

#     g_score = [float("inf") for row in grid for spot in row]
#     g_score[start[0] * len(grid[0]) + start[1]] = 0
#     f_score = [float("inf") for row in grid for spot in row]
#     f_score[start[0] * len(grid[0]) + start[1]] = h(start, end)

#     while not open_set.empty():
#         current = open_set.get()[2]
#         open_set_his.remove(current)
#         if current == end:
#             print("finishing")
#             short_path(came_from, end)
#             # Sau khi vòng lặp kết thúc
#             end_time = pygame.time.get_ticks()
#             elapsed_time = (end_time - start_time) / 1000.0
#             print(f"Algorithm finished in {elapsed_time:.2f} seconds")
#             return True
        
#         for nei in neighbour[current[0] * len(grid[0]) + current[1]]:
#             temp_g_score = g_score[current[0] * len(grid[0]) + current[1]] + 1
#             if temp_g_score < g_score[nei[0] * len(grid[0]) + nei[1]]:
#                 came_from[nei] = current
#                 g_score[nei[0] * len(grid[0]) + nei[1]] = temp_g_score
#                 f_score[nei[0] * len(grid[0]) + nei[1]] = temp_g_score + h(nei, end)
#                 if nei not in open_set_his:
#                     count += 1
#                     open_set.put((f_score[nei[0] * len(grid[0]) + nei[1]], count, nei))
#                     open_set_his.add(nei)
#                     grid[nei[0]][nei[1]] = 5
#                     draw_grid()  # Thêm hàm vẽ sau khi cập nhật ô
#                     #pygame.time.delay(100)

#         if current != start:
#             vertices_explored += 1
#             grid[current[0]][current[1]] = 6
#             draw_grid()
#             #pygame.time.delay(100)

#     # Sau khi vòng lặp kết thúc
#     end_time = pygame.time.get_ticks()
#     elapsed_time = (end_time - start_time) / 1000.0
#     print(f"Algorithm finished in {elapsed_time:.2f} seconds")

#     return False

# def dfs_step_by_step():
#     global grid, neighbour
#     global grid, neighbour
#     global steps_taken, vertices_explored, start_time, elapsed_time
#     neighbourr()

#     start, end = S_E(grid, 0, 0)
#     stack = [start]
#     visited = set()
#     came_from = {}

#     while stack:
#         current = stack.pop()

#         if current == end:
#             print("finishing")
#             short_path(came_from, end)  # Visualize the short path
#             # Sau khi vòng lặp kết thúc
#             end_time = pygame.time.get_ticks()
#             elapsed_time = (end_time - start_time) / 1000.0
#             print(f"Algorithm finished in {elapsed_time:.2f} seconds")
#             return True

#         if current not in visited:
#             visited.add(current)
#             grid[current[0]][current[1]] = 5  # Visualize the exploration
#             draw_grid()
#             #pygame.time.delay(50)  # Adjust the delay as needed

#             for nei in neighbour[current[0] * len(grid[0]) + current[1]]:
#                 if nei not in visited:
#                     stack.append(nei)
#                     came_from[nei] = current  # Store the path information

#         if current != start:
#             vertices_explored += 1
#             grid[current[0]][current[1]] = 6  # Visualize backtracking
#             draw_grid()  # Thêm hàm vẽ sau khi cập nhật ô
#             #pygame.time.delay(50)  # Uncomment if needed for a delay during backtracking

#     # Sau khi vòng lặp kết thúc
#     end_time = pygame.time.get_ticks()
#     elapsed_time = (end_time - start_time) / 1000.0
#     print(f"Algorithm finished in {elapsed_time:.2f} seconds")

#     return False



# def draw_grid():
#     for row in range(33):
#         for column in range(33):
#             if grid[row][column] == 1:
#                 color = three
#             elif grid[row][column] == 2:
#                 color = one
#             elif grid[row][column] == 3:
#                 color = five
#             elif grid[row][column] == 4:
#                 color = one
#             elif grid[row][column] == 5:
#                 color = six
#             elif grid[row][column] == 6:
#                 color = seven
#             else:
#                 color = four
#             pygame.draw.rect(screen, color, [margin + (margin + width) * column, margin + (margin + height) * row, width, height])
#     pygame.display.flip()



# while not done:
#     for event in pygame.event.get(): 
#         if event.type == pygame.QUIT:
#             done = True
#         elif event.type == pygame.KEYDOWN:
#              if event.key == pygame.K_ESCAPE:
#                     print("Exit")
#                     pygame.quit()
#              if event.key == pygame.K_s:
#                  print("Saving Maze")
#                  savegrid()
#              if event.key == pygame.K_l:
#                  print("Loading Maze")
#                  loadgrid(0)
#              if event.key == pygame.K_f:
#                  print("Filling Maze")
#                  grid = [[1 for x in range(33)] for y in range(33)]
#              if event.key == pygame.K_1:
#                  print("Loading Maze 1")
#                  loadgrid(1)
#              if event.key == pygame.K_2:
#                  print("Loading Maze 2")
#                  loadgrid(2)
#              if event.key == pygame.K_3:
#                  print("Loading Maze 3")
#                  loadgrid(3)
#              if event.key == pygame.K_4:
#                  print("Loading Maze 4")
#                  loadgrid(4)
#              if event.key == pygame.K_5:
#                  print("Loading Maze 5")
#                  loadgrid(5)
#              if event.key == pygame.K_RETURN:
#                 if((sum(x.count(2) for x in grid)) == 1):
#                     print("Solving")
#                     #dfs_step_by_step()
#                     a_star()
#              if event.key == pygame.K_r:

#                 grid = [[0 for x in range(33)] for y in range(33)]
#         if pygame.mouse.get_pressed()[2]:
#             column = pos[0] // (width + margin)
#             row = pos[1] // (height + margin)
#             if((sum(x.count(2) for x in grid)) < 1 or (sum(x.count(3) for x in grid)) < 1):
#                 if((sum(x.count(2) for x in grid)) == 0):
#                     if(grid[row][column] == 2):
#                         grid[row][column] = 0
#                     elif(grid[row][column] == 3):
#                         grid[row][column] = 0
#                     else:
#                         grid[row][column]  = 2
#                 else:
#                     if(grid[row][column] == 3):
#                         grid[row][column] = 0
#                     elif(grid[row][column] == 2):
#                         grid[row][column] = 0
#                     else:
#                         grid[row][column]  = 3
#             else:
#                 if(grid[row][column] == 2):
#                     grid[row][column] = 0
#                 if(grid[row][column] == 3):
#                     grid[row][column] = 0
#                 if(grid[row][column] == 1):
#                     grid[row][column] = 0
#         if pygame.mouse.get_pressed()[0]:
#             # if(event.button == 1):
#             column = pos[0] // (width + margin)
#             row = pos[1] // (height + margin)
#             print("left click")
#             grid[row][column] = 1
        
                
#     pos = pygame.mouse.get_pos()
#     x = pos[0]
#     y = pos[1]
#     screen.fill(two)
#     for row in range(33):
#         for column in range(33):
#             if grid[row][column] == 1:
#                 color = three
#             elif grid[row][column] == 2:
#                 color = one
#             elif grid[row][column] == 3:
#                 color = five
#             elif grid[row][column] == 4:
#                 color = one
#             elif grid[row][column] == 5:
#                 color = six
#             elif grid[row][column] == 6:
#                 color = seven
#             else:
#                 color = four
#             pygame.draw.rect(screen, color, [margin + (margin + width) * column, margin + (margin + height) * row, width, height])

#     # Hiển thị các thông số trực tiếp trên cửa sổ
#     font = pygame.font.SysFont(None, 26)
#     steps_text = font.render(f"Steps: {steps_taken}", True, (255, 255, 255))
#     vertices_text = font.render(f"Vertices: {vertices_explored}", True, (255, 255, 255))
#     time_text = font.render(f"Time: {elapsed_time:.2f} ms", True, (255, 255, 255))

#     screen.blit(steps_text, (730, 0))
#     screen.blit(vertices_text, (730, 20))
#     screen.blit(time_text, (730, 40))

#     pygame.display.flip()
#     clock.tick(60)
# pygame.quit()
