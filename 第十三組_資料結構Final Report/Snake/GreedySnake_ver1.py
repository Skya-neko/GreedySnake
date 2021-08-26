import selfLinkList as listo
import pygame
import time
import random
import json
from pygame import gfxdraw

# 初始化pygame
pygame.init()
pygame.mixer.init(frequency=44100, buffer=512)

# 顏色參數
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (178, 34, 34)
green = (0, 255, 0)
blue = (50, 153, 213)
body = (14, 242, 170)
body_dark = (14, 200, 170)
grey = (204, 204, 204)
blue_light = (33, 150, 243)
white_light = (235, 235, 235)
BACKGROUND = 174, 222, 203

# 初始化參數
game_start = 3
notice_time = 0
music_playing = False
config = {'music_sound': True, 'effect_sound': True, 'show_fps': False, 'show_score': True, 'high_scores': [0, 0, 0, 0, 0, 0, 0, 0, 0]}

# 設定畫面大小
SCREEN_WIDTH = dis_width = 1200
SCREEN_HEIGHT = dis_height = 800
pygame.display.set_caption('Snake Game')
# TODO: Full Screen Mode
SCREEN_WIDTH, SCREEN_HEIGHT = int(pygame.display.Info().current_w), int(pygame.display.Info().current_h)
SCREEN = dis = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Snake Game')

# 載入圖片
star = pygame.image.load("./img/star.png")
star.convert()
snakeHead = pygame.image.load("./img/snake-head.png")
snakeHead.convert()
rewsnakeHead = pygame.image.load("./img/Nyan_smaller.png")
rewsnakeHead.convert()
rewsnakeBody = pygame.image.load("./img/rainbow_smaller.png")
rewsnakeBody.convert()
wall = pygame.image.load("./img/wall.png")
wall.convert()

# 載入音樂
MUSIC_SOUND = pygame.mixer.Sound('./sound/background.mp3')
CRASH_SOUND = pygame.mixer.Sound('./sound/crash.mp3')
EAT_SOUND = pygame.mixer.Sound('./sound/eat.mp3')
MUSIC_SOUND.set_volume(0.3)
CRASH_SOUND.set_volume(0.3)
EAT_SOUND.set_volume(0.3)

CONFIG_FILE = 'config.json'

# 設定時脈
clock = pygame.time.Clock()

# 蛇的參數
snake_block = 20

# 設定字型樣式
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

# 載入字型樣式
FONT_BOLD = './fonts/OpenSans-SemiBold.ttf'
FONT_REG = './fonts/OpenSans-Regular.ttf'
FONT_LIGHT = './fonts/OpenSans-Light.ttf'

# 設定字型大小
LARGE_TEXT = pygame.font.Font(FONT_REG, int(40 / 1080 * SCREEN_HEIGHT))
MENU_TEXT = pygame.font.Font(FONT_LIGHT, int(110 / 1080 * SCREEN_HEIGHT))
SMALL_TEXT = pygame.font.Font(FONT_BOLD, int(25 / 1440 * SCREEN_HEIGHT))
MEDIUM_TEXT = pygame.font.Font(FONT_LIGHT, int(35 / 1440 * SCREEN_HEIGHT))

# 設定物件尺寸
BUTTON_WIDTH = int(SCREEN_WIDTH * 0.625 // 3)
BUTTON_HEIGHT = int(SCREEN_HEIGHT * 5 // 81)
TOGGLE_WIDTH = int(BUTTON_WIDTH * 0.875)
TOGGLE_ADJ = int(BUTTON_WIDTH * 0.075)
button_x_start = (SCREEN_WIDTH - BUTTON_WIDTH) // 2
button_layout_4 = [(button_x_start, SCREEN_HEIGHT * 5 // 13, BUTTON_WIDTH, BUTTON_HEIGHT),
                   (button_x_start, SCREEN_HEIGHT * 6 // 13, BUTTON_WIDTH, BUTTON_HEIGHT),
                   (button_x_start, SCREEN_HEIGHT * 7 // 13, BUTTON_WIDTH, BUTTON_HEIGHT),
                   (button_x_start, SCREEN_HEIGHT * 8 // 13, BUTTON_WIDTH, BUTTON_HEIGHT)]


# 儲存config設定
def save_config():
    with open(CONFIG_FILE, 'w') as fp:
        json.dump(config, fp, indent=4)


# 載入config設定
try:
    with open(CONFIG_FILE) as f:
        _config = json.load(f)
except FileNotFoundError:
    _config = {}
save_file = False
for k, v in config.items():
    try:
        # 更新config設定
        config[k] = _config[k]
    except KeyError:
        save_file = True
if save_file:
    save_config()


# 定義文字Object
def text_objects(text, font, color=black):
    text_surface = font.render(text, True, color)
    return text_surface, text_surface.get_rect()


# 定義選擇Object
def draw_circle(surface, x, y, radius, color):
    gfxdraw.aacircle(surface, x, y, radius, color)
    gfxdraw.filled_circle(surface, x, y, radius, color)


# 定義按鈕Object
def button(text, x, y, w, h, click, inactive_color=body, active_color=body_dark, text_colour=white):
    mouse = pygame.mouse.get_pos()
    return_value = False
    if x < mouse[0] < x + w and y < mouse[1] < y + h:  # if mouse is hovering the button
        pygame.draw.rect(SCREEN, inactive_color, (x, y, w, h))
        if click and pygame.time.get_ticks() > 100: return_value = True
    else:
        pygame.draw.rect(SCREEN, active_color, (x, y, w, h))

    text_surf, text_rect = text_objects(text, SMALL_TEXT, color=text_colour)
    text_rect.center = (int(x + w / 2), int(y + h / 2))
    SCREEN.blit(text_surf, text_rect)
    return return_value


# 觸發選擇按鈕
def toggle_btn(text, x, y, w, h, click, text_colour=black, enabled=True, draw_toggle=True, enabled_color=blue_light,
               disabled_color=grey):
    mouse = pygame.mouse.get_pos()
    # draw_toggle and blit_text are used to reduce redundant drawing and blitting (improves quality)
    rect_height = h // 2
    if rect_height % 2 == 0: rect_height += 1
    if enabled and draw_toggle:
        pygame.draw.rect(SCREEN, white, (x + TOGGLE_WIDTH - h // 4, y, TOGGLE_ADJ + h, rect_height))
        pygame.draw.rect(SCREEN, enabled_color, (x + TOGGLE_WIDTH, y, TOGGLE_ADJ, rect_height))
        draw_circle(SCREEN, int(x + TOGGLE_WIDTH), y + h // 4, h // 4, enabled_color)
        draw_circle(SCREEN, int(x + TOGGLE_WIDTH + TOGGLE_ADJ), y + h // 4, h // 4, enabled_color)
        draw_circle(SCREEN, int(x + TOGGLE_WIDTH + TOGGLE_ADJ), y + h // 4, h // 5, white)  # small inner circle
    elif draw_toggle:
        pygame.draw.rect(SCREEN, white, (x + TOGGLE_WIDTH - h // 4, y, TOGGLE_ADJ + h, rect_height))
        pygame.draw.rect(SCREEN, disabled_color, (x + TOGGLE_WIDTH, y, TOGGLE_ADJ, rect_height))
        draw_circle(SCREEN, int(x + TOGGLE_WIDTH), y + h // 4, h // 4, disabled_color)
        draw_circle(SCREEN, int(x + TOGGLE_WIDTH + TOGGLE_ADJ), y + h // 4, h // 4, disabled_color)
        draw_circle(SCREEN, int(x + TOGGLE_WIDTH), y + h // 4, h // 5, white)  # small inner circle
    text_surf, text_rect = text_objects(text, MEDIUM_TEXT, color=text_colour)
    text_rect.topleft = (x, y)
    SCREEN.blit(text_surf, text_rect)
    return x < mouse[0] < x + w and y < mouse[1] < y + h and click and pygame.time.get_ticks() > 100


# -------------------------------------------------------------------------
# 目錄.
# -------------------------------------------------------------------------
def main_menu_setup():
    # 設定背景顏色
    SCREEN.fill(white)
    # 設定遊戲名稱
    text_surf, text_rect = text_objects('Snake Game', MENU_TEXT)
    text_rect.center = (int(SCREEN_WIDTH / 2), int(SCREEN_HEIGHT / 4))
    SCREEN.blit(text_surf, text_rect)
    # 設定背景圖片
    background_surf = pygame.image.load("./img/snake_smaller.png")
    background_rect = background_surf.get_rect()
    background_rect.center = (int(SCREEN_WIDTH / 5), int(SCREEN_HEIGHT / 2))
    SCREEN.blit(background_surf, background_rect)
    pygame.display.update()


def main_menu():
    start_game = view_hs = False
    # 設定背景資訊
    main_menu_setup()
    while True:
        click = False
        for event in pygame.event.get():
            # 點擊右上角關閉視窗
            if event.type == pygame.QUIT:
                return False
            # 按下Esc關閉視窗
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                click = True
        # 設定按鈕
        if button('S T A R T  G A M E', *button_layout_4[0], click):
            start_game = True
        elif button('V I E W  H I G H S C O R E S', *button_layout_4[1], click) or view_hs:
            if view_high_scores():
                view_hs = False
                main_menu_setup()
            else:
                return False
        elif button('S E T T I N G S', *button_layout_4[2], click):
            if settings_menu():
                main_menu_setup()
            else:
                return False
        elif button('Q U I T  G A M E', *button_layout_4[3], click):
            return False
        # 開始遊戲
        while start_game:
            gameResult = gameLoop()
            if gameResult == 'Restart':
                start_game = True
            elif gameResult == 'Main Menu':
                start_game = False
                main_menu_setup()
            else:
                return False

        pygame.display.update(button_layout_4)
        clock.tick(60)


# -------------------------------------------------------------------------
# 倒數計時.
# -------------------------------------------------------------------------
def countDownPage(t):
    # running = True
    # while running:
    if t > 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        mins, secs = divmod(t, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)

        # 設定背景顏色
        SCREEN.fill(white)
        # 設定倒數文字
        text_surf, text_rect = text_objects(timer, MENU_TEXT)
        text_rect.center = (int(SCREEN_WIDTH / 2), int(SCREEN_HEIGHT / 2))
        SCREEN.blit(text_surf, text_rect)

        pygame.display.update()
        time.sleep(1)
        t -= 1
        countDownPage(t)


# -------------------------------------------------------------------------
# 設定.
# -------------------------------------------------------------------------
def settings_menu():
    draw_ms_toggle = draw_ef_toggle = True
    # 設定背景顏色
    SCREEN.fill(white)
    # 設定畫面名稱
    text_surf, text_rect = text_objects('Settings', MENU_TEXT)
    text_rect.center = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 4))
    SCREEN.blit(text_surf, text_rect)
    pygame.display.update()
    while True:
        click = False
        for event in pygame.event.get():
            # 點擊右上角關閉視窗
            if event.type == pygame.QUIT:
                return False
            # 按下Esc關閉視窗
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                click = True
        # 設定按鈕
        if toggle_btn('Music Sound', *button_layout_4[0], click, enabled=config['music_sound'],
                      draw_toggle=draw_ms_toggle):
            config['music_sound'] = not config['music_sound']
            save_config()
            draw_ms_toggle = True
        elif toggle_btn('Effect Sound', *button_layout_4[1], click, enabled=config['effect_sound'],
                        draw_toggle=draw_ef_toggle):
            config['effect_sound'] = not config['effect_sound']
            save_config()
            draw_ef_toggle = True
        elif button('B A C K', *button_layout_4[2], click):
            return True
        else:
            draw_ms_toggle = draw_ef_toggle = False
        pygame.display.update(button_layout_4)
        clock.tick(60)


# -------------------------------------------------------------------------
# 暫停.
# -------------------------------------------------------------------------
def pause_menu_setup(background):
    # 設定背景顏色
    SCREEN.blit(background, (0, 0))
    background = SCREEN.copy()
    # 設定畫面名稱
    text_surf, text_rect = text_objects('Pause Menu', MENU_TEXT, color=white)
    text_rect.center = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 4))
    SCREEN.blit(text_surf, text_rect)
    pygame.display.update()
    return background


def pause_menu():
    paused = True
    # 設定背景顏色
    background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA, 32)
    background.fill((*white_light, 160))
    background = pause_menu_setup(background)
    while paused:
        click = False
        for event in pygame.event.get():
            # 點擊右上角關閉視窗
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                # 按下Esc關閉視窗
                if event.key == pygame.K_ESCAPE:
                    return False
                # 按下P鍵返回
                elif event.key == pygame.K_p:
                    return 'Resume'
            elif event.type == pygame.MOUSEBUTTONDOWN:
                click = True
        # 設定按鈕
        if button('R E S U M E', *button_layout_4[0], click):
            return 'Resume'
        if button('M A I N  M E N U', *button_layout_4[1], click):
            return 'Main Menu'
        if button('S E T T I N G S', *button_layout_4[2], click):
            if settings_menu():
                pause_menu_setup(background)
            else:
                return False
        elif button('Q U I T  G A M E', *button_layout_4[3], click):
            return False
        pygame.display.update(button_layout_4)
        clock.tick(60)
    return 'Resume'


# -------------------------------------------------------------------------
# 遊戲結束.
# -------------------------------------------------------------------------
def end_game_setup(score, isBest, surface_copy=None):
    if isBest:
        title = 'You got a highest score!'
    else:
        title = 'Game Over'
    if surface_copy is not None:
        SCREEN.blit(surface_copy, (0, 0))
    else:
        # 設定背景顏色
        background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA, 32)
        background.fill((255, 255, 255, 160))
        SCREEN.blit(background, (0, 0))
        # 設定畫面名稱
        text_surf, text_rect = text_objects(title, MENU_TEXT, red)
        text_rect.center = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 5))
        SCREEN.blit(text_surf, text_rect)
        # 設定遊戲分數
        text_surf, text_rect = text_objects(f'You scored {score}', LARGE_TEXT)
        text_rect.center = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT * 7 // 22))
        SCREEN.blit(text_surf, text_rect)
        surface_copy = pygame.display.get_surface().copy()
    pygame.display.update()
    return surface_copy


def end_game(score):
    score = score * 10
    view_hs = isBest = False
    # 儲存遊戲分數
    if save_score(score):
        isBest = True  # Show "You got a highest score!"
    # 設定背景資訊
    end_screen_copy = end_game_setup(score, isBest)

    while True:
        click = False
        for event in pygame.event.get():
            # 點擊右上角關閉視窗
            if event.type == pygame.QUIT:
                return False
            # 按下Esc關閉視窗
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                click = True
        # 設定按鈕
        if button('R E S T A R T', *button_layout_4[0], click):
            return 'Restart'
        if button('M A I N  M E N U', *button_layout_4[1], click):
            return 'Main Menu'
        elif button('V I E W  H I G H S C O R E S', *button_layout_4[2], click) or view_hs:
            if view_high_scores():
                view_hs = False
                end_game_setup(score, isBest, end_screen_copy)
            else:
                return False
        elif button('Q U I T  G A M E', *button_layout_4[3], click):
            return False
        pygame.display.update(button_layout_4)
        clock.tick(60)


# -------------------------------------------------------------------------
# 查看紀錄.
# -------------------------------------------------------------------------
def view_high_scores():
    on_high_scores = True
    # 設定背景顏色
    SCREEN.fill(white)
    # 設定畫面名稱
    text_surf, text_rect = text_objects('High Scores', MENU_TEXT)
    text_rect.center = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 6))
    SCREEN.blit(text_surf, text_rect)
    # 設定遊戲分數
    for i, score in enumerate(config['high_scores']):
        text_surf, text_rect = text_objects(str(score), LARGE_TEXT)
        text_rect.center = (SCREEN_WIDTH // 2, int(SCREEN_HEIGHT * (i / 1.5 + 3) // 11))
        SCREEN.blit(text_surf, text_rect)
    pygame.display.update()
    back_button_rect = ((SCREEN_WIDTH - BUTTON_WIDTH) // 2, SCREEN_HEIGHT * 4 // 5, BUTTON_WIDTH, BUTTON_HEIGHT)
    while on_high_scores:
        click = False
        for event in pygame.event.get():
            # 點擊右上角關閉視窗
            if event.type == pygame.QUIT:
                return False
            # 按下Esc關閉視窗
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                click = True
        # 設定按鈕
        if button('B A C K', *back_button_rect, click):
            return True
        pygame.display.update([back_button_rect])
        clock.tick(60)


# -------------------------------------------------------------------------
# 儲存分數.
# -------------------------------------------------------------------------
def save_score(user_score: int) -> bool:
    scores = config['high_scores']
    placement = None
    for i, score in enumerate(scores):
        if user_score > score:
            placement = i
            break
        elif user_score == score:
            break
    if placement is not None:
        scores.insert(placement, user_score)
        scores.pop()
        save_config()
        if placement == 0:
            return True
    return False


# -------------------------------------------------------------------------
# 更新分數.
# -------------------------------------------------------------------------
def load_score(score):
    score = score * 10
    text_surf, text_rect = text_objects('Score: ' + str(score), LARGE_TEXT, white)
    text_rect = (int(SCREEN_WIDTH * 0.02), int(SCREEN_HEIGHT * 0.02))
    dis.blit(text_surf, text_rect)


# -------------------------------------------------------------------------
# 提示分數.
# -------------------------------------------------------------------------
def notice_score(score, nx=0, ny=0, isSpeedUp=False):
    score = score * 10
    text_surf, text_rect = text_objects('+' + str(score), LARGE_TEXT, white)
    text_rect = (nx + 10), (ny + 10)
    dis.blit(text_surf, text_rect)
    if isSpeedUp:
        text_surf, text_rect = text_objects('Speed up', LARGE_TEXT, white)
        text_rect = (nx + 10), (ny + 40)
        dis.blit(text_surf, text_rect)


def our_snake(snake_list, i, eated):
    angle = 90 * i
    rotated_image = pygame.transform.rotate(snakeHead, angle)
    dis.blit(rotated_image, (snake_list[-1][0], snake_list[-1][1]))
    idx = 0
    for x in snake_list[:-1]:
        if x in eated:
            pygame.draw.rect(dis, yellow, [x[0], x[1], snake_block, snake_block])
            if idx == 0:
                del eated[0]
        else:
            color1 = 180 + idx * 10
            if color1 >= 255:
                color1 = 255
            pygame.draw.rect(dis, (body[0], color1, body[2]), [x[0], x[1], snake_block, snake_block])
        idx = idx + 1
    return eated


def rew_snake(rewsnake_list):
    dis.blit(rewsnakeHead, (rewsnake_list[rewsnake_list.count - 1][0], rewsnake_list[rewsnake_list.count - 1][1]))
    for x in rewsnake_list.iterate_item_end(rewsnake_list.count - 1):
        dis.blit(rewsnakeBody, (x[0], x[1]))


# Get the coordinate of food
def getCoordinate(dis):
    return round(random.randrange(0, dis - snake_block) / snake_block) * snake_block


# 取得新食物的位置
def getNewFoodPos(snake_List):
    food = [getCoordinate(dis_width), getCoordinate(dis_height)]
    if food in snake_List:
        return getNewFoodPos(snake_List)
    return food


# -------------------------------------------------------------------------
# 開始遊戲.
# -------------------------------------------------------------------------
def gameLoop():
    global music_playing, notice_time
    # 載入倒數畫面
    countDownPage(game_start)
    # 設定遊戲背景音樂
    if not music_playing and config['music_sound']:
        pygame.mixer.Channel(0).play(MUSIC_SOUND, loops=-1)
        music_playing = True

    # 設定蛇的初始位置
    nx = x1 = dis_width / 2
    ny = y1 = dis_height / 2

    # 設定蛇的初始方向
    x1_change = 0
    y1_change = -snake_block
    # 設定蛇的初始角度
    iRotate = 0
    # 設定蛇的初始速度
    snake_speed = 10

    # 初始遊戲分數
    score = 0

    eated = []
    snake_List = []
    Length_of_snake = 1
    Length_of_rewsnake = 1

    rewsnake_block = 20
    rewardX = 0  # round(random.randrange(0, 40 - rewsnake_block) / rewsnake_block) * rewsnake_block
    rewardY = round(random.randrange(0, dis_height - rewsnake_block) / rewsnake_block) * rewsnake_block
    rewsnake_List = listo.SingleLinkList()

    foodx = getCoordinate(dis_width)
    foody = getCoordinate(dis_height)

    wall_x = getCoordinate(dis_width)
    wall_y = getCoordinate(dis_height)
    wallPosition = []
    wallPosition.append([wall_x, wall_y])

    while True:
        for event in pygame.event.get():
            # 點擊右上角關閉視窗
            if event.type == pygame.QUIT:
                quit()
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    iRotate = 1
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    iRotate = 3
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    iRotate = 0
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    iRotate = 2
                    y1_change = snake_block
                    x1_change = 0
                # 按下P鍵暫停
                elif event.key == pygame.K_p:
                    # 暫停播放背景音樂
                    pygame.mixer.Channel(0).pause()
                    music_playing = False
                    pauseResult = pause_menu()
                    if pauseResult == 'Main Menu':
                        return 'Main Menu'
                    elif not pauseResult:
                        return False
                    # 重新檢查背景音樂播放的設定
                    if config['music_sound']:
                        pygame.mixer.Channel(0).unpause()
                        music_playing = True
                # 按下Esc關閉視窗
                elif event.key == pygame.K_ESCAPE:
                    return False

        # 遊戲結束:碰到牆壁
        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            # 設定遊戲結束音效
            if config['effect_sound']:
                pygame.mixer.Channel(1).play(CRASH_SOUND)
            # 停止背景音樂
            if music_playing:
                pygame.mixer.Channel(0).stop()
                music_playing = False
            return end_game(Length_of_snake - 1)

        x1 += x1_change
        y1 += y1_change
        dis.fill(black)
        dis.blit(star, (foodx, foody))
        for w in wallPosition:
            dis.blit(wall, (w[0], w[1]))

        snake_Head = [x1, y1]
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        # 遊戲結束:碰到自己身體
        for x in snake_List[:-1]:
            if x == snake_Head:
                # 設定遊戲結束音效
                if config['effect_sound']:
                    pygame.mixer.Channel(1).play(CRASH_SOUND)
                # 停止背景音樂
                if music_playing:
                    pygame.mixer.Channel(0).stop()
                    music_playing = False
                return end_game(Length_of_snake - 1)

        eated = our_snake(snake_List, iRotate, eated)

        # 更新目前得分數
        load_score(Length_of_snake - 1)
        # 更新通知分數
        if notice_time > 0:
            isSpeedUp = False
            if Length_of_snake % 3 == 0:
                isSpeedUp = True
            notice_score(score, nx, ny, isSpeedUp)
            notice_time -= 1

        # 設計加分小蛇
        if Length_of_snake % 3 == 0:
            # 設定加分小蛇的初始方向
            rewardXChange = rewsnake_block
            rewardYChange = 0

            rewardX += rewardXChange
            rewardY += rewardYChange

            rewsnake_Head = listo.SingleLinkList()
            rewsnake_Head.append(rewardX)
            rewsnake_Head.append(rewardY)
            rewsnake_List.append(rewsnake_Head)
            if rewsnake_List.count > Length_of_rewsnake:
                rewsnake_List.delete_item(rewsnake_List[0])

            rew_snake(rewsnake_List)
            # print(snake_List[-1], rewsnake_List[rewsnake_List.count - 1])

        pygame.display.update()

        # 當撞到障礙物時
        for w in wallPosition:
            wx = w[0]
            wy = w[1]
            if x1 == wx and y1 == wy:
                # 設定遊戲結束音效
                if config['effect_sound']:
                    pygame.mixer.Channel(1).play(CRASH_SOUND)
                # 停止背景音樂
                if music_playing:
                    pygame.mixer.Channel(0).stop()
                    music_playing = False
                return end_game(Length_of_snake - 1)

        # 當吃到星星時
        if x1 == foodx and y1 == foody:
            # 設定蛇加分音效
            if config['effect_sound']:
                pygame.mixer.Channel(1).play(EAT_SOUND)
            eated.append([foodx, foody])
            food = getNewFoodPos(snake_List)
            wallPosition.append(getNewFoodPos(snake_List))
            foodx = food[0]
            foody = food[1]

            # 設定通知資訊
            Length_of_snake += 1
            notice_time = 5
            score = 1
            nx = x1
            ny = y1

            # 更改更新速度
            if Length_of_snake % 3 == 0:
                snake_speed += Length_of_snake / 3 * 2

        # 當吃到加分小蛇時
        if Length_of_snake % 3 == 0:
            # print('第一層')
            if rewsnake_List.count > 2:
                # print('第二層')
                rewmatch = rewsnake_List[rewsnake_List.count - 1]
                rewmatch2 = rewsnake_List[rewsnake_List.count - 2]
                if (snake_List[-1][0] == rewmatch[0] and snake_List[-1][1] == rewmatch[1]) or (
                        snake_List[-1][0] == rewmatch2[0] and snake_List[-1][1] == rewmatch2[1]):
                    # 設定蛇加分音效
                    if config['effect_sound']:
                        pygame.mixer.Channel(1).play(EAT_SOUND)

                    # 設定通知資訊
                    Length_of_snake += 4
                    notice_time = 5
                    score = 4
                    nx = x1
                    ny = y1

                    # 更改更新速度
                    if Length_of_snake % 3 == 0:
                        snake_speed += Length_of_snake / 3 * 2

        # 設定加分小蛇身體長度
        if Length_of_rewsnake < 5:
            Length_of_rewsnake += 1

        # 設定加分小蛇的身體位置
        if Length_of_snake % 3 == 1:
            rewsnake_block = 20
            rewardX = 0  # round(random.randrange(0, 40 - rewsnake_block) / rewsnake_block) * rewsnake_block
            rewardY = round(random.randrange(0, dis_height - rewsnake_block) / rewsnake_block) * rewsnake_block
            rewsnake_List = listo.SingleLinkList()

        clock.tick(snake_speed)



# -------------------------------------------------------------------------
# 主程式.
# -------------------------------------------------------------------------
if __name__ == '__main__':
    if not main_menu():
        print('-----Final-----')
        pygame.mixer.Channel(0).stop()
        music_playing = False
        pygame.quit()
        quit()

    '''
    try:
        if not main_menu():
            print('-----Final-----')
            pygame.mixer.Channel(0).stop()
            music_playing = False
            pygame.quit()
            quit()

    except:
        print('-----Error-----')
        pygame.mixer.Channel(0).stop()
        music_playing = False
        pygame.quit()
        quit()
    '''
