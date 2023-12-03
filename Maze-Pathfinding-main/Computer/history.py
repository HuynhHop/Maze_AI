import pygame
import numpy as np
from queue import PriorityQueue
import pygame_gui
import sys


def read_data_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            data = file.read()
            return data
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        return None
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

def setup_ui(manager, data):
    width, height = 1100, 650

    textbox_size = (width - 40, height - 80)
    textbox_rect = pygame.Rect((20, 20), textbox_size)

    textbox = pygame_gui.elements.UITextBox(html_text=data, relative_rect=textbox_rect, manager=manager)

    return textbox

def history():
    pygame.init()

    width, height = 1100, 600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("History")

    manager = pygame_gui.UIManager((width, height))

    file_path = "data_node.txt"
    data = read_data_from_file(file_path)

    if data is not None:
        textbox = setup_ui(manager, data)

    clock = pygame.time.Clock()

    while True:
        time_delta = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        manager.process_events(event)

        manager.update(time_delta)

        screen.fill((255, 255, 255))

        manager.draw_ui(screen)

        pygame.display.flip()

history()