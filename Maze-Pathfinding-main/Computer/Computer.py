import pygame
import numpy as np
from queue import PriorityQueue
import sys
import pygame_gui
import subprocess

#colors
one = (79, 189, 186) #Xanh
two = (206, 171, 147) #Màu nền
three = (227, 202, 165) #Màu tường
four = (255, 251, 233) #Màu đường 
five = (246, 137, 137) #Màu đỏ đích
six = (255, 0, 0) #Màu đỏ đỉnh duyệt
seven = (0, 255, 0) #Màu đường đã duyệt xanh

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
Nodes_explored = 0
# Trước khi vào hàm a_star
start_time = 0
elapsed_time = 0

map_name = "0"
algorithm_name = "algorithm_name"


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
             
def neighbourr1():
    global grid, neighbour
    neighbour = {}

    for i in range(len(grid)):
        for j in range(len(grid)):
            current_node = (i, j)
            neighbour[current_node] = []

            if i > 0 and grid[i - 1][j] != 1:
                neighbour[current_node].append((i - 1, j))
            if j > 0 and grid[i][j - 1] != 1:
                neighbour[current_node].append((i, j - 1))
            if i < len(grid) - 1 and grid[i + 1][j] != 1:
                neighbour[current_node].append((i + 1, j))
            if j < len(grid[0]) - 1 and grid[i][j + 1] != 1:
                neighbour[current_node].append((i, j + 1))
            
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

##############    VẼ BUTTON     ####################################################################################################

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
    button_rect = pygame.Rect(730, 690, 120, 20)  # Rectangle for the Reset button
    return button_rect.collidepoint(mouse_pos)

# Function to draw the Reset button
def draw_reset_button():
    pygame.draw.rect(screen, (100, 100, 100), [730, 690, 120, 20])  # Reset button background
    font = pygame.font.SysFont(None, 18)  # Font size
    text = font.render("Reset", True, (255, 255, 255))
    screen.blit(text, (735, 695))

def is_over_history_button(mouse_pos):
    button_rect = pygame.Rect(730, 640, 120, 20)  # Rectangle for the Reset button
    return button_rect.collidepoint(mouse_pos)

# Function to draw the Reset button
def draw_history_button():
    pygame.draw.rect(screen, (100, 100, 100), [730, 640, 120, 20])  # Reset button background
    font = pygame.font.SysFont(None, 18)  # Font size
    text = font.render("History", True, (255, 255, 255))
    screen.blit(text, (735, 645))

def is_over_bfs_button(mouse_pos):
    button_rect = pygame.Rect(730, 150, 120, 20)  # Smaller BFS button rectangle, positioned below A*
    return button_rect.collidepoint(mouse_pos)

# Function to check if the mouse is over the Greedy button
def is_over_greedy_button(mouse_pos):
    button_rect = pygame.Rect(730, 180, 120, 20)  # Smaller Greedy button rectangle, positioned below BFS
    return button_rect.collidepoint(mouse_pos)

# Function to draw the BFS button
def draw_bfs_button():
    pygame.draw.rect(screen, (100, 100, 100), [730, 150, 120, 20])  # Smaller BFS button background, positioned below A*
    font = pygame.font.SysFont(None, 18)  # Smaller font size
    text = font.render("BFS", True, (255, 255, 255))
    screen.blit(text, (735, 155))

# Function to draw the Greedy button
def draw_greedy_button():
    pygame.draw.rect(screen, (100, 100, 100), [730, 180, 120, 20])  # Smaller Greedy button background, positioned below BFS
    font = pygame.font.SysFont(None, 18)  # Smaller font size
    text = font.render("Greedy", True, (255, 255, 255))
    screen.blit(text, (735, 185))

def is_over_bi_bfs_button(mouse_pos):
    button_rect = pygame.Rect(730, 210, 120, 20)  # Bi-BFS button rectangle, positioned below Greedy
    return button_rect.collidepoint(mouse_pos)

def draw_bi_bfs_button():
    pygame.draw.rect(screen, (100, 100, 100), [730, 210, 120, 20])  # Bi-BFS button background, positioned below Greedy
    font = pygame.font.SysFont(None, 18)  # Smaller font size
    text = font.render("Bidirectional", True, (255, 255, 255))
    screen.blit(text, (735, 215))

def is_over_uniform_cost_search_button(mouse_pos):
    button_rect = pygame.Rect(730, 240, 120, 20)  # Uniform Cost button rectangle, positioned below Bi-BFS
    return button_rect.collidepoint(mouse_pos)

def draw_uniform_cost_search_button():
    pygame.draw.rect(screen, (100, 100, 100), [730, 240, 120, 20])  # Uniform Cost button background, positioned below Bi-BFS
    font = pygame.font.SysFont(None, 18)  # Smaller font size
    text = font.render("Uniform Cost", True, (255, 255, 255))
    screen.blit(text, (735, 245))

def is_over_bellman_ford_button(mouse_pos):
    button_rect = pygame.Rect(730, 120, 120, 20)  # Bellman-Ford button rectangle, positioned below Uniform Cost Search
    return button_rect.collidepoint(mouse_pos)

def draw_bellman_ford_button():
    pygame.draw.rect(screen, (100, 100, 100), [730, 120, 120, 20])  # Bellman-Ford button background, positioned below Uniform Cost Search
    font = pygame.font.SysFont(None, 18)  # Smaller font size
    text = font.render("Bellman-Ford", True, (255, 255, 255))
    screen.blit(text, (735, 125))

def is_over_wall_button(mouse_pos):
    button_rect = pygame.Rect(730, 270, 120, 20)  # Uniform Cost button rectangle, positioned below Bi-BFS
    return button_rect.collidepoint(mouse_pos)

def draw_wall_button():
    pygame.draw.rect(screen, (100, 100, 100), [730, 270, 120, 20])  # Uniform Cost button background, positioned below Bi-BFS
    font = pygame.font.SysFont(None, 18)  # Smaller font size
    text = font.render("Wall-Following", True, (255, 255, 255))
    screen.blit(text, (735, 275))

def is_hill_climbing_button(mouse_pos):
    button_rect = pygame.Rect(730, 300, 120, 20)  # Uniform Cost button rectangle, positioned below Bi-BFS
    return button_rect.collidepoint(mouse_pos)

def draw_hill_climbing_button():
    pygame.draw.rect(screen, (100, 100, 100), [730, 300, 120, 20])  # Uniform Cost button background, positioned below Bi-BFS
    font = pygame.font.SysFont(None, 18)  # Smaller font size
    text = font.render("Hill- Climbing", True, (255, 255, 255))
    screen.blit(text, (735, 305))

##########     VẼ BUTTON     ################################################################################################################################
# def hill_climbing():
#     global grid, neighbour
#     global steps_taken, vertices_explored, start_time, elapsed_time
#     start_time = pygame.time.get_ticks()
#     neighbourr()

#     start, end = S_E(grid, 0, 0)
#     current = start
#     path_cost = 0
#     visited = {current}
#     path = {current: None}

#     while current != end:
#         neighbors = neighbour[current[0] * len(grid[0]) + current[1]]
#         neighbors.sort(key=lambda x: h(x, end))  # Sort neighbors by heuristic value (distance to the goal)

#         next_step = None
#         for nei in neighbors:
#             if nei not in visited:
#                 next_step = nei
#                 break

#         if next_step is not None:
#             visited.add(next_step)
#             grid[next_step[0]][next_step[1]] = 6  # Visualize the exploration
#             draw_grid()
#             # pygame.time.delay(50)  # Adjust the delay as needed

#             path_cost += 1
#             path[next_step] = current
#             current = next_step
#         else:
#             print("No valid move. Stuck in local optima.")
#             break
#     if current == end:
#         print("finishing")
#         short_path(path, end)  # Return the path information
#     end_time = pygame.time.get_ticks()
#     elapsed_time = (end_time - start_time) / 1000.0
#     print(f"Algorithm finished in {elapsed_time:.2f} seconds")
#     return False

def hill_climbing():
    global grid, neighbour
    global steps_taken, Nodes_explored, start_time, elapsed_time
    global map_name
    global algorithm_name

    algorithm_name = "hill_climbing"

    neighbourr()
    start_time = pygame.time.get_ticks()

    start, end = S_E(grid, 0, 0)
    current = start
    visited = set()
    came_from = {}

        # Mở tệp để ghi
    with open("data_node.txt", "a") as file:
        file.write(f"Map: {map_name}\n")
        file.write(f"Algorithm: {algorithm_name}\n")
        file.write(f"Start: {start}\n")
        file.write(f"End: {end}\n")
        while current != end:
            visited.add(current)

            grid[current[0]][current[1]] = 6  # Visualize the exploration
            draw_grid()
            file.write(f"({current[0]}, {current[1]}) ")  # Ghi tọa độ của node vào tệp

            neighbors = neighbour[current[0] * len(grid[0]) + current[1]]
            neighbors.sort(key=lambda x: heuristic(x, end))

            found = False
            for nei in neighbors:
                if nei not in visited:
                    found = True
                    came_from[nei] = current
                    current = nei
                    Nodes_explored += 1  # Đếm mỗi lần duyệt một đỉnh mới
                    break

            if not found:
                # Stuck in local minimum, backtrack
                if current == start:
                    # No more moves to explore, end the search
                    break
                else:
                    current = came_from[current]
                    grid[current[0]][current[1]] = 6  # Visualize backtracking
                    draw_grid()

        # Xuống hàng sau mỗi lần chạy thuật toán
        file.write("\n")

    # Đóng tệp sau khi vòng lặp kết thúc
    file.close()

    if current == end:
        print("finishing")
        short_path(came_from, end)
        with open("data_node.txt", "a") as file:
        # Sau khi vòng lặp kết thúc
            end_time = pygame.time.get_ticks()
            elapsed_time = (end_time - start_time) / 1000.0
            print(f"Algorithm finished in {elapsed_time:.2f} seconds")
            file.write(f"Running Time: {elapsed_time:.2f} seconds\n")
            file.write("\n")
        # Đóng tệp sau khi vòng lặp kết thúc
        file.close()
        return True
    else:
        return False


def heuristic(current, goal):
    # Hàm h(trạng thái hiện tại, trạng thái đích)
    return abs(current[0] - goal[0]) + abs(current[1] - goal[1])

def wall_following():
    global grid, neighbour
    global steps_taken, Nodes_explored, start_time, elapsed_time
    global map_name
    global algorithm_name

    
    algorithm_name = "wall_following"
    start_time = pygame.time.get_ticks()
    neighbourr()

    start, end = S_E(grid, 0, 0)
    current = start
    came_from = {}
    visited = set()

    # Mở tệp để ghi
    with open("data_node.txt", "a") as file:
        file.write(f"Map: {map_name}\n")
        file.write(f"Algorithm: {algorithm_name}\n")
        file.write(f"Start: {start}\n")
        file.write(f"End: {end}\n")
        while current != end:
            visited.add(current)
            grid[current[0]][current[1]] = 6  # Visualize the exploration
            file.write(f"({current[0]}, {current[1]}) ")  # Ghi tọa độ của node vào tệp
            draw_grid()
            # pygame.time.delay(15)  # Adjust the delay as needed

            wall_follow_neighbours = get_wall_follow_neighbours(current, grid)
            unvisited_neighbours = [nei for nei in wall_follow_neighbours if nei not in visited]

            if unvisited_neighbours:
                next_cell = max(unvisited_neighbours, key=lambda x: h(x, end)) # đi sang phải
                # next_cell = min(unvisited_neighbours, key=lambda x: h(x, end)) # đi sang trái
                came_from[next_cell] = current
                current = next_cell
            else:
                # Trở lại ô trước đó nếu không có ô lân cận chưa được thăm
                current = came_from[current]
                Nodes_explored += 1
                grid[current[0]][current[1]] = 5  # Visualize backtracking
                draw_grid()
                #pygame.time.delay(50)  # Uncomment if needed for a delay during backtracking
        # Xuống hàng sau mỗi lần chạy thuật toán
        file.write("\n")
  
        print("finishing")
        short_path(came_from, end)  # Visualize the short path
        end_time = pygame.time.get_ticks()
        elapsed_time = (end_time - start_time) / 1000.0
        print(f"Algorithm finished in {elapsed_time:.2f} seconds")
        file.write(f"Running Time: {elapsed_time:.2f} seconds\n")
        file.write("\n")

    # Đóng tệp sau khi vòng lặp kết thúc
    file.close()


def get_wall_follow_neighbours(current, grid):
    # Lấy tất cả các ô lân cận để theo dõi theo bức tường
    neighbours = []
    x, y = current
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Ngang và dọc

    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]) and grid[nx][ny] != 1:
            neighbours.append((nx, ny))

    return neighbours


def bellman_ford():
    global grid, neighbour
    global steps_taken, Nodes_explored, start_time, elapsed_time
    global map_name
    global algorithm_name
  
    algorithm_name = "bellman_ford"
    neighbourr1()
    start_time = pygame.time.get_ticks()

    start, end = S_E(grid, 0, 0)
    distance = {node: float('inf') for node in neighbour}
    distance[start] = 0
    came_from = {}
    with open("data_node.txt", "a") as file:
        file.write(f"Map: {map_name}\n")
        file.write(f"Algorithm: {algorithm_name}\n")
        file.write(f"Start: {start}\n")
        file.write(f"End: {end}\n")
        for _ in range(len(neighbour) - 1):
            for node in neighbour:
                for nei in neighbour[node]:
                    new_distance = distance[node] + 1
                    if new_distance < distance[nei]:
                        distance[nei] = new_distance
                        came_from[nei] = node
                        grid[nei[0]][nei[1]] = 6  # Visualize the exploration
                        draw_grid()
                        file.write(f"({nei[0]}, {nei[1]}) ")  # Ghi tọa độ của node vào tệp
                        # pygame.time.delay(15)  # Adjust the delay as needed

        # Check for negative cycles
        for node in neighbour:
            for nei in neighbour[node]:
                if distance[node] + 1 < distance[nei]:
                    print("Negative cycle found!")
                    return False

        # Reconstruct the shortest path
        current = end
        while current != start:
            grid[current[0]][current[1]] = 4
            
            draw_grid()
            #pygame.time.delay(50)  # Adjust the delay as needed
            current = came_from[current]

        # Update the metrics
        Nodes_explored = len(distance)
        steps_taken = distance[end]
        file.write("\n")
        # Sau khi vòng lặp kết thúc
        end_time = pygame.time.get_ticks()
        elapsed_time = (end_time - start_time) / 1000.0
        print(f"Algorithm finished in {elapsed_time:.2f} seconds")
        file.write(f"Running Time: {elapsed_time:.2f} seconds\n")
        file.write("\n")

    # Đóng tệp sau khi vòng lặp kết thúc
    file.close()
    return True

def uniform_cost_search():
    global grid, neighbour
    global steps_taken, Nodes_explored, start_time, elapsed_time
    global map_name
    global algorithm_name

    algorithm_name = "uniform_cost_search"
    neighbourr()
    start_time = pygame.time.get_ticks()

    start, end = S_E(grid, 0, 0)
    count = 0
    priority_queue = PriorityQueue()
    priority_queue.put((0, count, start))
    visited = set()
    came_from = {}

    cost_so_far = {start: 0}
    with open("data_node.txt", "a") as file:
        file.write(f"Map: {map_name}\n")
        file.write(f"Algorithm: {algorithm_name}\n")
        file.write(f"Start: {start}\n")
        file.write(f"End: {end}\n")
        while not priority_queue.empty():
            current_cost, _, current = priority_queue.get()
            file.write(f"({current[0]}, {current[1]}) ")  # Ghi tọa độ của node vào tệp
            if current == end:
                print("finishing")
                short_path(came_from, end)
                file.write("\n")
                # Sau khi vòng lặp kết thúc
                end_time = pygame.time.get_ticks()
                elapsed_time = (end_time - start_time) / 1000.0
                print(f"Algorithm finished in {elapsed_time:.2f} seconds")
                file.write(f"Running Time: {elapsed_time:.2f} seconds\n")
                file.write("\n")
                return True

            if current not in visited:
                visited.add(current)
                grid[current[0]][current[1]] = 5  # Visualize the exploration
                draw_grid()
                # pygame.time.delay(15)

                for nei in neighbour[current[0] * len(grid[0]) + current[1]]:
                    new_cost = cost_so_far[current] + 1
                    if nei not in visited or new_cost < cost_so_far[nei]:
                        cost_so_far[nei] = new_cost
                        count += 1
                        priority_queue.put((new_cost, count, nei))
                        came_from[nei] = current  # Store the path information

            if current != start:
                Nodes_explored += 1
                grid[current[0]][current[1]] = 6  # Visualize backtracking
                draw_grid()

    # Đóng tệp sau khi vòng lặp kết thúc
    file.close()
    return False
    
def a_star():
    global grid, neighbour
    global steps_taken, Nodes_explored, start_time, elapsed_time
    global map_name
    global algorithm_name

    algorithm_name = "a_star"
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

    with open("data_node.txt", "a") as file:
        file.write(f"Map: {map_name}\n")
        file.write(f"Algorithm: {algorithm_name}\n")
        file.write(f"Start: {start}\n")
        file.write(f"End: {end}\n")
        while not open_set.empty():
            current = open_set.get()[2]
            file.write(f"({current[0]}, {current[1]}) ")  # Ghi tọa độ của node vào tệp
            open_set_his.remove(current)
            if current == end:
                print("finishing")
                short_path(came_from, end)
                # Sau khi vòng lặp kết thúc
                file.write("\n")
                end_time = pygame.time.get_ticks()
                elapsed_time = (end_time - start_time) / 1000.0
                print(f"Algorithm finished in {elapsed_time:.2f} seconds")
                file.write(f"Running Time: {elapsed_time:.2f} seconds\n")
                file.write("\n")
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
                        pygame.time.delay(15)

            if current != start:
                Nodes_explored += 1
                grid[current[0]][current[1]] = 6
                draw_grid()
                #pygame.time.delay(100)
    # Đóng tệp sau khi vòng lặp kết thúc
    file.close()

    return False

def dfs_step_by_step():
    global grid, neighbour
    global grid, neighbour
    global steps_taken, Nodes_explored, start_time, elapsed_time
    global map_name
    global algorithm_name

    algorithm_name = "dfs"
    start_time = pygame.time.get_ticks()
    neighbourr()

    start, end = S_E(grid, 0, 0)
    stack = [start]
    visited = set()
    came_from = {}

    with open("data_node.txt", "a") as file:
        file.write(f"Map: {map_name}\n")
        file.write(f"Algorithm: {algorithm_name}\n")
        file.write(f"Start: {start}\n")
        file.write(f"End: {end}\n")
        while stack:
            current = stack.pop()
            file.write(f"({current[0]}, {current[1]}) ")  # Ghi tọa độ của node vào tệp
            if current == end:
                print("finishing")
                short_path(came_from, end)  # Visualize the short path
                # Sau khi vòng lặp kết thúc
                file.write("\n")
                end_time = pygame.time.get_ticks()
                elapsed_time = (end_time - start_time) / 1000.0
                print(f"Algorithm finished in {elapsed_time:.2f} seconds")
                file.write(f"Running Time: {elapsed_time:.2f} seconds\n")
                file.write("\n")
                return True

            if current not in visited:
                visited.add(current)
                grid[current[0]][current[1]] = 5  # Visualize the exploration
                draw_grid()
                # pygame.time.delay(15) # Adjust the delay as needed

                for nei in neighbour[current[0] * len(grid[0]) + current[1]]:
                    if nei not in visited:
                        stack.append(nei)
                        came_from[nei] = current  # Store the path information

            if current != start:
                Nodes_explored += 1
                grid[current[0]][current[1]] = 6  # Visualize backtracking
                draw_grid()  # Thêm hàm vẽ sau khi cập nhật ô
                #pygame.time.delay(100)  # Uncomment if needed for a delay during backtracking

    # Đóng tệp sau khi vòng lặp kết thúc
    file.close()

    return False

def bfs():
    global grid, neighbour
    global steps_taken, Nodes_explored, start_time, elapsed_time
    global map_name
    global algorithm_name

    algorithm_name = "bfs"
    start_time = pygame.time.get_ticks()
    neighbourr()

    start, end = S_E(grid, 0, 0)
    queue = [start]
    visited = set()
    came_from = {}
    with open("data_node.txt", "a") as file:
        file.write(f"Map: {map_name}\n")
        file.write(f"Algorithm: {algorithm_name}\n")
        file.write(f"Start: {start}\n")
        file.write(f"End: {end}\n")
        while queue:
            current = queue.pop(0)
            file.write(f"({current[0]}, {current[1]}) ")  # Ghi tọa độ của node vào tệp
            if current == end:
                print("finishing")
                short_path(came_from, end)  # Visualize the short path
                # Sau khi vòng lặp kết thúc
                file.write("\n")
                end_time = pygame.time.get_ticks()
                elapsed_time = (end_time - start_time) / 1000.0
                print(f"Algorithm finished in {elapsed_time:.2f} seconds")
                file.write(f"Running Time: {elapsed_time:.2f} seconds\n")
                file.write("\n")
                return True

            if current not in visited:
                visited.add(current)
                grid[current[0]][current[1]] = 5  # Visualize the exploration
                draw_grid()
                # pygame.time.delay(15)   # Adjust the delay as needed

                for nei in neighbour[current[0] * len(grid[0]) + current[1]]:
                    if nei not in visited:
                        queue.append(nei)
                        came_from[nei] = current  # Store the path information

            if current != start:
                Nodes_explored += 1
                grid[current[0]][current[1]] = 6  # Visualize backtracking
                draw_grid()
                # pygame.time.delay(50)  # Uncomment if needed for a delay during backtracking

    # Đóng tệp sau khi vòng lặp kết thúc
    file.close()
    return False

def greedy():
    global grid, neighbour
    global steps_taken, Nodes_explored, start_time, elapsed_time
    global map_name
    global algorithm_name

    algorithm_name = "greedy"
    start_time = pygame.time.get_ticks()
    neighbourr()

    start, end = S_E(grid, 0, 0)
    priority_queue = [(h(start, end), start)]
    visited = set()
    came_from = {}
    with open("data_node.txt", "a") as file:
        file.write(f"Map: {map_name}\n")
        file.write(f"Algorithm: {algorithm_name}\n")
        file.write(f"Start: {start}\n")
        file.write(f"End: {end}\n")
        while priority_queue:
            current = priority_queue.pop(0)[1]
            file.write(f"({current[0]}, {current[1]}) ")  # Ghi tọa độ của node vào tệp
            if current == end:
                print("finishing")
                short_path(came_from, end)  # Visualize the short path
                # Sau khi vòng lặp kết thúc
                file.write("\n")
                end_time = pygame.time.get_ticks()
                elapsed_time = (end_time - start_time) / 1000.0
                print(f"Algorithm finished in {elapsed_time:.2f} seconds")
                file.write(f"Running Time: {elapsed_time:.2f} seconds\n")
                file.write("\n")
                return True

            if current not in visited:
                visited.add(current)
                grid[current[0]][current[1]] = 5  # Visualize the exploration
                draw_grid()
                # pygame.time.delay(15)  # Adjust the delay as needed

                for nei in neighbour[current[0] * len(grid[0]) + current[1]]:
                    if nei not in visited:
                        priority_queue.append((h(nei, end), nei))
                        priority_queue.sort(key=lambda x: x[0])  # Sort the queue based on heuristic value
                        came_from[nei] = current  # Store the path information

            if current != start:
                Nodes_explored += 1
                grid[current[0]][current[1]] = 6  # Visualize backtracking
                draw_grid()
                # pygame.time.delay(50)  # Uncomment if needed for a delay during backtracking
    # Đóng tệp sau khi vòng lặp kết thúc
    file.close()
    return False

# Bidirectional Search Algorithm- Duyệt từ điểm đầu và điểm đích ngược lại
def bi_bfs():
    global grid, neighbour
    global steps_taken, Nodes_explored, start_time, elapsed_time
    global map_name
    global algorithm_name    
    algorithm_name = "Bidirectional"
    start_time = pygame.time.get_ticks()
    neighbourr()

    start, end = S_E(grid, 0, 0)
    start_queue = [start]
    end_queue = [end]
    start_visited = set()
    end_visited = set()
    start_came_from = {}
    end_came_from = {}

    steps_current_start = []
    steps_current_end = []

    with open("data_node.txt", "a") as file:
        file.write(f"Map: {map_name}\n")
        file.write(f"Algorithm: {algorithm_name}\n")
        file.write(f"Start: {start}\n")
        file.write(f"End: {end}\n")
        while start_queue and end_queue:
            current_start = start_queue.pop(0)
            steps_current_start.append(current_start)
            if current_start in end_visited:
                # Tìm điểm gặp nhau
                meeting_point = current_start
                short_path(start_came_from, meeting_point)
                short_path(end_came_from, meeting_point)
                # Ghi các bước của current_start vào tệp tin
                file.write("Steps of Current Start: ")
                for step in steps_current_start:
                    file.write(f"({step[0]}, {step[1]}) ")

                # Ghi các bước của current_end vào tệp tin
                file.write("\nSteps of Current End: ")
                for step in steps_current_end:
                    file.write(f"({step[0]}, {step[1]}) ")
                # Sau khi vòng lặp kết thúc
                file.write("\n")
                end_time = pygame.time.get_ticks()
                elapsed_time = (end_time - start_time) / 1000.0
                print(f"Algorithm finished in {elapsed_time:.2f} seconds")
                file.write(f"Running Time: {elapsed_time:.2f} seconds\n")
                file.write("\n")
                return True

            if current_start not in start_visited:
                start_visited.add(current_start)
                grid[current_start[0]][current_start[1]] = 5 
                draw_grid()
                # pygame.time.delay(15)

                for nei in neighbour[current_start[0] * len(grid[0]) + current_start[1]]:
                    if nei not in start_visited:
                        start_queue.append(nei)
                        start_came_from[nei] = current_start  # Lưu trữ thông tin đường dẫn

            current_end = end_queue.pop(0)
            steps_current_end.append(current_end)

            if current_end in start_visited:
                # Tìm điểm gặp nhau 
                meeting_point = current_end
                short_path(start_came_from, meeting_point)
                short_path(end_came_from, meeting_point)
                # Sau khi vòng lặp kết thúc
                        # Ghi các bước của current_start vào tệp tin
                file.write("Steps of Current Start: ")
                for step in steps_current_start:
                    file.write(f"({step[0]}, {step[1]}) ")

                # Ghi các bước của current_end vào tệp tin
                file.write("\nSteps of Current End: ")
                for step in steps_current_end:
                    file.write(f"({step[0]}, {step[1]}) ")
                end_time = pygame.time.get_ticks()
                file.write("\n")
                elapsed_time = (end_time - start_time) / 1000.0
                print(f"Algorithm finished in {elapsed_time:.2f} seconds")
                file.write(f"Running Time: {elapsed_time:.2f} seconds\n")
                file.write("\n")
                return True

            if current_end not in end_visited:
                end_visited.add(current_end)
                grid[current_end[0]][current_end[1]] = 5  
                draw_grid()

                for nei in neighbour[current_end[0] * len(grid[0]) + current_end[1]]:
                    if nei not in end_visited:
                        end_queue.append(nei)
                        end_came_from[nei] = current_end  # Lưu trữ thông tin đường dẫn
            if current_start != start:
                Nodes_explored += 1
                grid[current_start[0]][current_start[1]] = 6  # Trực quan hóa việc quay lại
                draw_grid()

            if current_end != end:
                Nodes_explored += 1
                grid[current_end[0]][current_end[1]] = 6  # Trực quan hóa việc quay lại
                draw_grid()
        # Đóng tệp sau khi vòng lặp kết thúc
    file.close()

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
    try:
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
                    steps_taken = 0
                    Nodes_explored = 0
                    elapsed_time = 0
                    map_name = "Load Map"
                if event.key == pygame.K_f:
                    print("Filling Maze")
                    grid = [[1 for x in range(33)] for y in range(33)]
                if event.key == pygame.K_1:
                    print("Loading Maze 1")
                    loadgrid(1)
                    steps_taken = 0
                    Nodes_explored = 0
                    elapsed_time = 0
                    map_name = "1"
                if event.key == pygame.K_2:
                    print("Loading Maze 2")
                    loadgrid(2)
                    steps_taken = 0
                    Nodes_explored = 0
                    elapsed_time = 0
                    map_name = "2"
                if event.key == pygame.K_3:
                    print("Loading Maze 3")
                    loadgrid(3)
                    steps_taken = 0
                    Nodes_explored = 0
                    elapsed_time = 0
                    map_name = "3"
                if event.key == pygame.K_4:
                    print("Loading Maze 4")
                    loadgrid(4)
                    steps_taken = 0
                    Nodes_explored = 0
                    elapsed_time = 0
                    map_name = "4"
                if event.key == pygame.K_5:
                    print("Loading Maze 5")
                    loadgrid(5)
                    steps_taken = 0
                    Nodes_explored = 0
                    elapsed_time = 0
                    map_name = "5"
                if event.key == pygame.K_r:
                    grid = [[0 for x in range(33)] for y in range(33)]
                    steps_taken = 0
                    Nodes_explored = 0
                    elapsed_time = 0
                    map_name = "0"
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()  # Move this line inside the event loop
                if is_over_a_star_button(pos):
                    print("Running A* Algorithm")
                    a_star()
                    # dfs_step_by_step();
                elif is_over_dfs_button(pos):
                    print("Running DFS Algorithm")
                    dfs_step_by_step()
                elif is_over_bfs_button(pos):
                    print("Running BFS Algorithm")
                    bfs()
                elif is_over_greedy_button(pos):
                    print("Running Greedy Algorithm")
                    greedy()  
                elif is_over_bi_bfs_button(pos):
                    print("Running Bi-BFS Algorithm")
                    bi_bfs()       
                elif is_over_uniform_cost_search_button(pos):
                    print("Running Uniform Cost Search")
                    uniform_cost_search() 
                elif is_over_bellman_ford_button(pos):
                    print("Running Bellman-Ford Algorithm")
                    bellman_ford()
                elif is_over_wall_button(pos):
                    print("Running Wall-Following Algorithm")
                    wall_following()
                    # hill_climbing()  
                elif is_hill_climbing_button(pos):
                    hill_climbing()
                elif is_over_history_button(pos):
                    print("History")
                    subprocess.call(["python", "D:/Maze-Pathfinding-main/Computer/history.py"])
                elif is_over_reset_button(pos):
                    print("Resetting Maze")
                    grid = [[0 for x in range(33)] for y in range(33)]
                    steps_taken = 0
                    Nodes_explored = 0
                    elapsed_time = 0
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
        Nodes_text = font.render(f"Nodes: {Nodes_explored}", True, (255, 255, 255))
        time_text = font.render(f"Time: {elapsed_time:.2f} s", True, (255, 255, 255))

        screen.blit(steps_text, (730, 0))
        screen.blit(Nodes_text, (730, 20))
        screen.blit(time_text, (730, 40))

        draw_a_star_button()
        draw_dfs_button()
        draw_reset_button()
        draw_bfs_button()
        draw_greedy_button()
        draw_bi_bfs_button()
        draw_uniform_cost_search_button()
        draw_bellman_ford_button()
        draw_wall_button()
        draw_hill_climbing_button()
        draw_history_button()

        pygame.display.flip()
        clock.tick(60)
    except:
        pass
pygame.quit()