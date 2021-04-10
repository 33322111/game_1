import math
import pygame as pg
import random
import time
import os
from pygame.locals import *


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    image = pg.image.load(fullname).convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


pg.init()
back = "white"
diff_bg = (255, 255, 0)
size = width, height = 800, 600
screen = pg.display.set_mode(size, FULLSCREEN)
pg.mouse.set_visible(0)
table = load_image("table2.png", 2)
pg.display.update()
play = load_image("player.png", -1)
plx = width / 2
ply = height / 2
gamer = pg.Rect(plx, ply, play.get_rect().width, play.get_rect().height)
song1 = pg.mixer.Sound(os.path.join('data', "babax_noise.mp3"))  # добавим музыку
win = 2
complication = "Normal"
best = [0, 0, 0]  # счет
lives = 1
running = True
while running:
    screen.blit(table, (0, 0))
    blue_ball = load_image("blue_ball.png", -1)
    blue_rectan = pg.Rect(random.randint(0, width - blue_ball.get_rect().width),
                          random.randint(0, height - blue_ball.get_rect().height), blue_ball.get_rect().width,
                          blue_ball.get_rect().height)
    red_ball = load_image("red_ball.png", -1)
    red_rectan = pg.Rect(random.randint(0, width - red_ball.get_rect().width),
                         random.randint(0, height - red_ball.get_rect().height), red_ball.get_rect().width,
                         red_ball.get_rect().height)
    green_ball = load_image("green_ball.png", -1)
    green_rectan = pg.Rect(random.randint(0, width - green_ball.get_rect().width),
                           random.randint(0, height - green_ball.get_rect().height), green_ball.get_rect().width,
                           green_ball.get_rect().height)
    babax = load_image("babax.png", -1)
    red_angle = random.randint(0, 360)
    green_angle = random.randint(0, 360)
    blue_angle = random.randint(0, 360)
    ball_pictures = [red_ball, green_ball, blue_ball]
    balls = [red_rectan, green_rectan, blue_rectan]
    balls_angles = [red_angle, green_angle, blue_angle]
    angle_player = 0
    fl_gamer = False
    fl_gamer_left = False
    fl_gamer_right = False
    cursor_speed = 3.5
    ball_speed = 4
    counter_spawn = 150
    time_counter = 0
    clock = pg.time.Clock()
    fps = 50
    time_count = 0
    flag = True
    running2 = True
    ending = False
    while running2:
        for event in pg.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    flag = False
                    running2 = False
                    running = False
                if event.key == K_SPACE:
                    running2 = False
                if event.key == K_DOWN and complication != "Easy":
                    if complication == "Hard":
                        complication = "Normal"
                    else:
                        complication = "Easy"
                if event.key == K_UP and complication != "Hard":
                    if complication == "Easy":
                        complication = "Normal"
                    else:
                        complication = "Hard"
        if complication == "Easy":
            counter_spawn = 250
            diff_bg = (0, 255, 0)
            lives = 7
            win = 1
        if complication == "Normal":
            counter_spawn = 150
            diff_bg = (255, 255, 0)
            lives = 5
            win = 2
        if complication == "Hard":
            diff_bg = (240, 7, 62)
            counter_spawn = 50
            lives = 2
            win = 6
        screen.fill((100, 100, 100))
        text_title = pg.font.SysFont(None, 125)
        text_phrase = pg.font.SysFont(None, 75)
        text_phrase2 = pg.font.SysFont(None, 25)
        title = text_title.render("Побег", True, "black")
        screen.blit(title, (40, 40))
        s1 = text_phrase.render("Нажмите пробел, чтобы начать", True, "black", (255, 255, 255))
        s2 = text_phrase.render("Нажмите esc, чтобы выйти", True, "black", (255, 255, 255))
        s3 = text_phrase.render(complication, True, "black", diff_bg)
        s4 = text_phrase2.render("Воспользуйтесь стрелками, чтобы изменить уровень", True, "black")
        s5 = text_phrase.render("Уровень:", True, "black")
        screen.blit(s1, (10, 315))
        screen.blit(s2, (65, 390))
        screen.blit(s3, (500, 100))
        screen.blit(s4, (350, 215))
        screen.blit(s5, (470, 10))
        pg.draw.polygon(screen, "black", ((500, 90), (525, 65), (550, 90)))
        pg.draw.polygon(screen, "black", ((500, 167), (525, 192), (550, 167)))
        pg.display.update()
    # Начало основного цикла
    while flag == 1:
        time_count += 1  # время
        if fl_gamer_left:
            angle_player += 5
        if fl_gamer_right:
            angle_player -= 5
        if fl_gamer:
            b = math.cos(math.radians(angle_player)) * cursor_speed
            a = math.sin(math.radians(angle_player)) * cursor_speed
            gamer.top += round(b)
            gamer.left += round(a)
        pg.display.update()
        for event in pg.event.get():
            if event.type == QUIT:
                flag = False
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    flag = False
                if event.key == K_UP or event.key == K_w:
                    fl_gamer = True
                if event.key == K_LEFT or event.key == K_a:
                    fl_gamer_left = True
                if event.key == K_RIGHT or event.key == K_d:
                    fl_gamer_right = True
            if event.type == KEYUP:
                if event.key == K_UP or event.key == K_w:
                    fl_gamer = False
                if event.key == K_LEFT or event.key == K_a:
                    fl_gamer_left = False
                if event.key == K_RIGHT or event.key == K_d:
                    fl_gamer_right = False
        # Обработка нажатия
        for i in range(len(balls)):
            counter = 0
            if balls[i].top <= 0 or balls[i].bottom >= height:
                counter += 1
                balls_angles[i] = 360 - balls_angles[i]
                b = math.cos(math.radians(balls_angles[i])) * ball_speed
                a = math.sin(math.radians(balls_angles[i])) * ball_speed
                balls[i].left += b
                balls[i].top += a
            if balls[i].left <= 0 or balls[i].right >= width:
                counter += 1
                balls_angles[i] = 180 - balls_angles[i]
                b = math.cos(math.radians(balls_angles[i])) * ball_speed
                a = math.sin(math.radians(balls_angles[i])) * ball_speed
                balls[i].left += b
                balls[i].top += a
            if counter == 0:
                b = math.cos(math.radians(balls_angles[i])) * ball_speed
                a = math.sin(math.radians(balls_angles[i])) * ball_speed
                balls[i].left += b
                balls[i].top += a
        # Логика шаров
        screen.blit(table, (0, 0))
        rectan_player = play.get_rect().center
        neu_player = pg.transform.rotate(play, angle_player - 180)
        neu_player.get_rect().center = rectan_player
        rectan_player = play.get_rect()
        center_neu = neu_player.get_rect().center
        center_diff = (gamer.center[0] - center_neu[0], gamer.center[1] - center_neu[1])
        # Команды для игрока
        for i in range(len(balls)):
            screen.blit(ball_pictures[i], balls[i])
        screen.blit(neu_player, center_diff)
        time_counter += 1
        if time_counter >= counter_spawn:
            balls.append(pg.Rect(random.randint(0, width - red_ball.get_rect().width),
                                 random.randint(0, height - red_ball.get_rect().height), red_ball.get_rect().width,
                                 red_ball.get_rect().height))
            ball_pictures.append(ball_pictures[random.randint(0, 2)])
            balls_angles.append(random.randint(0, 360))
            time_counter = 0
        # Команды для рестарта игры
        for i in balls:
            if gamer.colliderect(i):
                lives -= 1
                if lives < 1:
                    screen.blit(babax, (
                        gamer.left - babax.get_rect().width / 2 + 12,
                        gamer.top - babax.get_rect().height / 2 + 12))
                    pg.display.update()
                    song1.play()
                    time.sleep(1)
                    ending = True
                    flag = False
                gamer.left = width / 2 - gamer.width / 2
                gamer.top = height / 2 - gamer.height / 2
        pg.display.update()
        clock.tick(fps)
        if not gamer.colliderect(0, 0, width, height):
            lives -= 1
            if lives < 1:
                ending = True
                flag = False
            gamer.left = width / 2 - gamer.width / 2
            gamer.top = height / 2 - gamer.height / 2
        # Проверка границ
    # Конец
    flag = True
    while ending and flag:
        for event in pg.event.get():
            if event.type == KEYDOWN:
                flag = False
        screen.blit(table, (0, 0))
        bas_font = pg.font.SysFont(None, 100)  # 150)
        text = bas_font.render("Вы проиграли!", True, "black")
        c = time_count
        time_text = text_phrase.render("Ваш счет: " + str(int((round(c / fps, 2))) * win), True, "black")
        esc_text = text_phrase.render("Нажмите, чтобы продолжить.", True, "black")
        best.append(round((c / fps) * win))
        best = list(set(best))
        best.append(0)
        best.sort(reverse=True)
        best = best[:3]
        lines = open(os.path.join('data', 'результат игры.txt')).read().splitlines()
        ch = text_phrase.render(f"Рекорд: {lines[0].split()[1]}", True, "black")
        screen.blit(text, (50, 100))
        screen.blit(ch, (75, 400))
        screen.blit(time_text, (75, 300))
        screen.blit(esc_text, (40, 500))
        pg.display.update()
        if int((round(c / fps, 2))) * win > int(lines[0].split()[1]):
            f = open(os.path.join('data', 'результат игры.txt'), 'w')
            f.write(f"Рекорд: {int((round(c / fps, 2))) * win}")
            f.close()
pg.quit()
