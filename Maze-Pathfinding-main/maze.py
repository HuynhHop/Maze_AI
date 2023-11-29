import subprocess
import pygame
import sys

# Khởi tạo Pygame
pygame.init()

# Kích thước của cửa sổ trò chơi
screen_width = 640
screen_height = 360

# Màu sắc
ORANGE = (255, 165, 0)

# Tạo cửa sổ
screen = pygame.display.set_mode((screen_width, screen_height))

class StartButtonFrame(pygame.sprite.Sprite):
    def __init__(self, image_path, x, y):
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

# Vẽ text
def draw_text(text, size, color, x, y):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    screen.blit(text_surface, text_rect)

#CÁC ĐƯỜNG DẪN $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# Đường dẫn đến hình ảnh PNG bạn muốn sử dụng làm nền
background_image = "D:/Maze-Pathfinding-main/Display/backround.jpg"
# Đường dẫn đến hình ảnh nút bắt đầu trò chơi
start_button_image = "D:/Maze-Pathfinding-main/Display/nut_startgame_menu (1).png"
# Đường dẫn đến hình ảnh option frame
option_button_image = "D:/Maze-Pathfinding-main/Display/khung_option (1) (1).png"
# Đường dẫn đến hình ảnh nút back
back_button_image = "D:/Maze-Pathfinding-main/Display/nut_back (1).png"
# Đường dẫn đến hình ảnh nút Person
person_button_image = "D:/Maze-Pathfinding-main/Display/nut_nguoi_choi_png (1).png"
# Đường dẫn đến hình ảnh nút Computer
computer_button_image = "D:/Maze-Pathfinding-main/Display/nut_may_choi.png"
# Đường dẫn đến hình ảnh nút Level
level_button_image = "D:/Maze-Pathfinding-main/Display/nut_chon_level.png"
# Đường dẫn đến hình ảnh nút Computer
newgame_button_image = "D:/Maze-Pathfinding-main/Display/nut_new_game.png"
# Đường dẫn đến hình ảnh nút level 1 2 3 4 5 6 7 8 9
level1_button_image = "D:/Maze-Pathfinding-main/Display/level_1.png"
level2_button_image = "D:/Maze-Pathfinding-main/Display/level_2.png"
level3_button_image = "D:/Maze-Pathfinding-main/Display/level_3.png"
level4_button_image = "D:/Maze-Pathfinding-main/Display/level_4.png"
level5_button_image = "D:/Maze-Pathfinding-main/Display/level_5.png"
level6_button_image = "D:/Maze-Pathfinding-main/Display/level_6.png"
level7_button_image = "D:/Maze-Pathfinding-main/Display/level_7.png"
level8_button_image = "D:/Maze-Pathfinding-main/Display/level_8.png"
level9_button_image = "D:/Maze-Pathfinding-main/Display/level_9.png"
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$


#LOAD CÁC HÌNH ẢNH ****************************************************************************************************
# Load hình ảnh nền
background = pygame.image.load(background_image)
# Load hình ảnh nút bắt đầu trò chơi
start_button = pygame.image.load(start_button_image)
start_button_frame = StartButtonFrame(start_button_image, 180, 260)
# Load hình ảnh khung option
option_button = pygame.image.load(option_button_image)
option_button_frame = StartButtonFrame(option_button_image, 225, 150)
# Load hình ảnh nút back
back_button = pygame.image.load(back_button_image)
back_button_frame = StartButtonFrame(back_button_image, 380, 290)
# Load hình ảnh nút Person
person_button = pygame.image.load(person_button_image)
person_button_frame = StartButtonFrame(person_button_image, 260, 180)
# Load hình ảnh nút Computer
computer_button = pygame.image.load(computer_button_image)
computer_button_frame = StartButtonFrame(computer_button_image, 260, 250)
# Load hình ảnh nút Level
level_button = pygame.image.load(level_button_image)
level_button_frame = StartButtonFrame(level_button_image, 260, 180)
# Load hình ảnh nút Newgame
newgame_button = pygame.image.load(newgame_button_image)
newgame_button_frame = StartButtonFrame(newgame_button_image, 260, 250)
# Load hình ảnh nút Level 1 2 3 4 5 6 7 8 9
level1_button = pygame.image.load(level1_button_image)
level1_button_frame = StartButtonFrame(level1_button_image, 240, 180)
level2_button = pygame.image.load(level2_button_image)
level2_button_frame = StartButtonFrame(level2_button_image, 300, 180)
level3_button = pygame.image.load(level3_button_image)
level3_button_frame = StartButtonFrame(level3_button_image, 360, 180)
level4_button = pygame.image.load(level4_button_image)
level4_button_frame = StartButtonFrame(level4_button_image, 240, 220)
level5_button = pygame.image.load(level5_button_image)
level5_button_frame = StartButtonFrame(level5_button_image, 300, 220)
level6_button = pygame.image.load(level6_button_image)
level6_button_frame = StartButtonFrame(level6_button_image, 360, 220)
level7_button = pygame.image.load(level7_button_image)
level7_button_frame = StartButtonFrame(level7_button_image, 240, 260)
level8_button = pygame.image.load(level8_button_image)
level8_button_frame = StartButtonFrame(level8_button_image, 300, 260)
level9_button = pygame.image.load(level9_button_image)
level9_button_frame = StartButtonFrame(level9_button_image, 360, 260)
#****************************************************************************************************************************


#BIẾN THEO DÕI TRẠNG THÁI HIỆN TẠI CỦA TRÒ CHƠI !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
is_option_screen = False
is_level_screen = False
is_level123_screen = False
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not is_option_screen:
                if start_button_frame.rect.collidepoint(event.pos):
                    is_option_screen = True
            elif is_option_screen and not is_level_screen:
                if back_button_frame.rect.collidepoint(event.pos):
                    is_option_screen = False
                elif person_button_frame.rect.collidepoint(event.pos):
                    is_level_screen = True
                elif computer_button_frame.rect.collidepoint(event.pos):
                    subprocess.call(["python", "D:/Maze-Pathfinding-main/Computer/Computer.py"])
            elif is_level_screen and not is_level123_screen:
                if back_button_frame.rect.collidepoint(event.pos):
                    is_level_screen = False
                elif level_button_frame.rect.collidepoint(event.pos):
                    is_level123_screen = True
                elif newgame_button_frame.rect.collidepoint(event.pos):
                    subprocess.call(["python", "D:/Maze-Pathfinding-main/Player/level1.py"])
            elif is_level123_screen:
                if back_button_frame.rect.collidepoint(event.pos):
                    is_level123_screen = False  # Thoát khỏi màn hình Level1, Level2, Level3
                elif level1_button_frame.rect.collidepoint(event.pos):
                    subprocess.call(["python", "D:/Maze-Pathfinding-main/Player/level1.py"])
                elif level2_button_frame.rect.collidepoint(event.pos):
                    subprocess.call(["python", "D:/Maze-Pathfinding-main/Player/level2.py"])
                elif level3_button_frame.rect.collidepoint(event.pos):
                    subprocess.call(["python", "D:/Maze-Pathfinding-main/Player/level3.py"])
                elif level4_button_frame.rect.collidepoint(event.pos):
                    subprocess.call(["python", "D:/Maze-Pathfinding-main/Player/level4.py"])
                elif level5_button_frame.rect.collidepoint(event.pos):
                    subprocess.call(["python", "D:/Maze-Pathfinding-main/Player/level5.py"])
                elif level6_button_frame.rect.collidepoint(event.pos):
                    subprocess.call(["python", "D:/Maze-Pathfinding-main/Player/level6.py"])
                elif level7_button_frame.rect.collidepoint(event.pos):
                    subprocess.call(["python", "D:/Maze-Pathfinding-main/Player/level7.py"])
                elif level8_button_frame.rect.collidepoint(event.pos):
                    subprocess.call(["python", "D:/Maze-Pathfinding-main/Player/level8.py"])
                elif level9_button_frame.rect.collidepoint(event.pos):
                    print("Thành công - Chọn Level9")

    # Vẽ hình ảnh nền lên cửa sổ
    screen.blit(background, (0, 0))
    draw_text("MAZE", 70, ORANGE, 230 + 100, 60)

    if not is_option_screen:
        # Nếu không ở màn hình option, vẽ nút bắt đầu trò chơi lên cửa sổ
        screen.blit(start_button, start_button_frame.rect.topleft)
    elif is_option_screen and not is_level_screen:
        # Nếu ở màn hình option, vẽ khung option, nút back, Person_button, và Computer_button lên cửa sổ
        screen.blit(option_button, option_button_frame.rect.topleft)
        screen.blit(back_button, back_button_frame.rect.topleft)
        screen.blit(person_button, person_button_frame.rect.topleft)
        screen.blit(computer_button, computer_button_frame.rect.topleft)
    elif is_level_screen and not is_level123_screen:
        # Nếu ở màn hình Level, vẽ khung option, nút back, Level_button, và Newgame_button lên cửa sổ
        screen.blit(option_button, option_button_frame.rect.topleft)
        screen.blit(back_button, back_button_frame.rect.topleft)
        screen.blit(level_button, level_button_frame.rect.topleft)
        screen.blit(newgame_button, newgame_button_frame.rect.topleft)
    elif is_level123_screen:
        # Nếu ở màn hình Level123, vẽ khung option, nút back, Level1_button lên cửa sổ
        screen.blit(option_button, option_button_frame.rect.topleft)
        screen.blit(back_button, back_button_frame.rect.topleft)
        screen.blit(level1_button, level1_button_frame.rect.topleft)
        screen.blit(level2_button, level2_button_frame.rect.topleft)
        screen.blit(level3_button, level3_button_frame.rect.topleft)
        screen.blit(level4_button, level4_button_frame.rect.topleft)
        screen.blit(level5_button, level5_button_frame.rect.topleft)
        screen.blit(level6_button, level6_button_frame.rect.topleft)
        screen.blit(level7_button, level7_button_frame.rect.topleft)
        screen.blit(level8_button, level8_button_frame.rect.topleft)
        screen.blit(level9_button, level9_button_frame.rect.topleft)
    # Cập nhật cửa sổ
    pygame.display.flip()

# Kết thúc Pygame
pygame.quit()
sys.exit()