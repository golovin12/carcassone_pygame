import cv2
import os
import pygame
import random

from Camera import *
from Player import *
from Pole import *

# Цвета тайлов + вспомогательные
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 128, 0)

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (10, 32)
pygame.init()
# Формирование окна с игрой
X, Y = 80, 80
infoObject = pygame.display.Info()
size = width, height = (infoObject.current_w - 80 - 20, infoObject.current_h - 80)
fullscr = 1
screen = pygame.display.set_mode((size[0] + 80, size[1]))
clock = pygame.time.Clock()
fps = 60
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 20)
lvl_w = 5760
lvl_h = 5760
camera = Camera(camera_func, lvl_w, lvl_h)
window = pygame.Surface(size)


# Для вывода текущего значения FPS
def update_fps():
    fps = str(int(clock.get_fps()))
    fps_text = myfont.render(fps, 1, RED)
    return fps_text


def fullscreen(full):
    global size, width, height, screen, camera, window, button1, button2
    if full == 1:
        size = width, height = (infoObject.current_w - 80 - 20, infoObject.current_h - 80)
        screen = pygame.display.set_mode((size[0] + 80, size[1]))
    else:
        size = width, height = (800, 600)
        screen = pygame.display.set_mode((size[0] + 80, size[1]))
    window = pygame.Surface(size)
    camera.full = full


# Загружает картинку в виде массива пикселей (каждый пиксель задан в RGB)
def load_image(images, a, b):
    image = []
    for i in images:
        fullname = "img/" + i
        try:
            if i[-3:] == "jpg" or i[-3:] == "png":
                image.append(pygame.transform.scale(pygame.image.load(fullname).convert(), (a * X, b * Y)))
            else:
                image.append(pygame.transform.scale(pygame.image.load(fullname).convert_alpha(), (a * X, b * Y)))
        except:
            print("Не удалось загрузить изображение:", i)
            raise SystemExit
    return image


def new_game():
    global running
    button1.sdvig((width / 2) - 350, (height / 2) - 50)
    button2.sdvig((width / 2) + 150, (height / 2) - 50)
    conec = True
    while conec:
        Mouse_x, Mouse_y = pygame.mouse.get_pos()
        muse.update(Mouse_x, Mouse_y)
        screen.fill((255, 255, 255))
        menu_fon = pygame.image.load("img/menu_fon.jpg").convert()
        menu_fon = pygame.transform.scale(menu_fon, (width + 80, height))
        screen.blit(menu_fon, (0, 0))

        if pygame.sprite.spritecollide(muse, button1_sprites, False):
            button1.update(but2)
        else:
            button1.update(but1)
        for e in button1_sprites:
            screen.blit(e.image, e.rect)

        if pygame.sprite.spritecollide(muse, button2_sprites, False):
            button2.update(but2)
        else:
            button2.update(but1)
        for e in button2_sprites:
            screen.blit(e.image, e.rect)

        textsurfaceb1 = myfont.render("НЕТ", False, RED)
        screen.blit(textsurfaceb1, ((width / 2) - 325, (height / 2) - 25))
        textsurfaceb3 = myfont.render("ДА", False, RED)
        screen.blit(textsurfaceb3, ((width / 2) + 175, (height / 2) - 25))
        pygame.draw.rect(screen, (255, 255, 255),
                         ((width / 2) - 247, (height / 2) - 265, 600, 90))
        pygame.draw.rect(screen, (255, 0, 0),
                         ((width / 2) - 247, (height / 2) - 265, 600, 90), 8)
        textsurfaceb2 = myfont.render("ВЫ ДЕЙСТВИТЕЛЬНО ХОТТЕ НАЧАТЬ НОВУЮ ИГРУ?", False, RED)
        screen.blit(textsurfaceb2, ((width / 2) - 222, (height / 2) - 250))
        textsurfaceb2 = myfont.render("(при этом сбросятся все результаты)", False, RED)
        screen.blit(textsurfaceb2, ((width / 2) - 135, (height / 2) - 220))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                conec = False
                running = False

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if pygame.sprite.spritecollide(muse, button1_sprites, False):
                        button1.rect.x, button1.rect.y = ((width + 80) / 2 - 260 / 2, (height / 2) - 140)
                        button2.rect.x, button2.rect.y = ((width + 80) / 2 - 260 / 2, (height / 2) + 20)
                        button2.sdvig(x=button2.rect.x, y=(height / 2) + 215)
                        conec = False
                        return 0
                    elif pygame.sprite.spritecollide(muse, button2_sprites, False):
                        conec = False
                        return 1
        pygame.display.flip()
        clock.tick(fps)


# Класс кнопки для Меню
class Button(pygame.sprite.Sprite):
    def __init__(self, image, pos_y):
        super().__init__()
        self.image = pygame.Surface((260, 80))
        self.image = image
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = (width + 80) / 2 - 260 / 2
        self.rect.y = pos_y
        self.rect = pygame.Rect(self.rect.x, self.rect.y, 260, 80)

    def update(self, image):
        self.image = image
        self.image.set_colorkey(WHITE)

    def sdvig(self, x=((width + 80) / 2 - 260 / 2), y=(height / 2) - 40):
        self.rect.x = x
        self.rect.y = y


# Класс персонажа, относительно которого двигается камера
class Person(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((80, 80))
        pole.sled_tile()
        self.image = pole.image
        self.rect = pygame.Rect(2880, 2880, 80, 80)
        self.border = pygame.Rect(0, 0, 80, 80)
        pygame.draw.rect(self.image, GREEN, self.border, 1)

    def update(self, x, y):
        if game_pos == 0:
            pole.sled_tile()
            self.image = pole.image
            self.border = pygame.Rect(0, 0, 80, 80)
            self.rect = self.rect.move(x * X, y * Y)
            if pygame.sprite.spritecollide(person, tiles_sprites, False):
                c = 1
            else:
                c = 0
            if c == 1:
                pygame.draw.rect(self.image, RED, self.border, 1)
            else:
                pygame.draw.rect(self.image, GREEN, self.border, 1)
        else:
            self.image = load_image(["no.png", ], 1, 1)[0]
            self.image.set_colorkey(WHITE)
            self.rect = self.rect.move(x * X, y * Y)
            screen.blit(self.image, self.rect)


# Класс, для проверки того, можно ли поставить тайл в определённую позицию
class For_prov():
    frames = []
    post_tile = {}

    def __init__(self, images, columns, rows):
        self.cut_image(images, columns, rows)
        self.frames[0], self.frames[len(self.frames) - 1] = self.frames[len(self.frames) - 1], self.frames[0]

    def cut_image(self, images, columns, rows):
        for k in images:
            pik = cv2.imread(k)
            for j in range(rows):
                for i in range(columns):
                    self.frames.append(pik[j * 80:j * 80 + 80, i * 80:i * 80 + 80:])

    def new_tile(self, y, x):
        moz = 0
        btile = []
        for i in [self.frames[pole.num_of_tile][0][39], self.frames[pole.num_of_tile][39][79],
                  self.frames[pole.num_of_tile][79][39], self.frames[pole.num_of_tile][39][0],
                  self.frames[pole.num_of_tile][39][39]]:
            (b, g, r) = i
            kr = 128
            btile.append((kr * (b // kr), kr * (g // kr), kr * (r // kr)))
        if pole.num_of_tile == 0:
            self.post_tile.update({pole.num_of_tile: btile + ["ad"]})
            return 0
        else:
            if pole.pole[x + 1][y] != "" and pole.pole[x + 1][y] in self.post_tile:
                moz -= 1
                if self.post_tile.get(pole.pole[x + 1][y])[3] == btile[1]:
                    moz += 1
            if pole.pole[x][y + 1] != "" and pole.pole[x][y + 1] in self.post_tile:
                moz -= 1
                if self.post_tile.get(pole.pole[x][y + 1])[0] == btile[2]:
                    moz += 1
            if pole.pole[x - 1][y] != "" and pole.pole[x - 1][y] in self.post_tile:
                moz -= 1
                if self.post_tile.get(pole.pole[x - 1][y])[1] == btile[3]:
                    moz += 1
            if pole.pole[x][y - 1] != "" and pole.pole[x][y - 1] in self.post_tile:
                moz -= 1
                if self.post_tile.get(pole.pole[x][y - 1])[2] == btile[0]:
                    moz += 1
            if moz == 0:
                self.post_tile.update({pole.num_of_tile: btile + ["ad"]})
            return moz

    def povorot(self):
        empty_img = cv2.imread(r"img/player1.png")
        for i in range(80):
            for j in range(80):
                empty_img[i][j] = self.frames[pole.num_of_tile][80 - j - 1][i]
        self.frames[pole.num_of_tile] = empty_img


for_prov = For_prov([r"img/b1_ram.jpg", r"img/b2_ram.jpg", r"img/b3_ram.jpg"], 4, 6)

doroga_schet = [[], [], [], []]


def isp_tileses_doroga():
    global doroga_schet
    for i in range(4):
        yield doroga_schet[i]


doroga_ms = [[], [], [], []]


def isp_mses_doroga():
    global doroga_ms
    for i in range(4):
        yield doroga_ms[i]


conec_doroga = [[], [], [], []]


def isp_conec_doroga():
    global conec_doroga
    for i in range(4):
        yield conec_doroga[i]


trbl_for_d = [[], [], [], [], []]


# Проверяет длину дороги относительно поставленного тайла и выводит всех тайлов, на этой дороге
def pravila_doroga(x, y, etap, isp_tiles=None, isp_ms=None, conecg=None, trbl=None):
    global conec_doroga, doroga_schet, doroga_ms, trbl_for_d
    white = (128, 128, 128)
    black = (0, 0, 0)
    a = for_prov.post_tile.get(pole.pole[x][y])
    poles = [pole.pole[x][y - 1], pole.pole[x + 1][y], pole.pole[x][y + 1], pole.pole[x - 1][y]]
    coords = [(x, y - 1), (x + 1, y), (x, y + 1), (x - 1, y)]
    colich = a[:4].count(white)
    br = isp_tileses_doroga()
    ms = isp_mses_doroga()
    cg = isp_conec_doroga()
    c = 0

    if isp_tiles == None:
        isp_tiles = next(br)
        isp_ms = next(ms)
        conecg = next(cg)
    else:
        isp_tiles = isp_tiles
        isp_ms = isp_ms
        conecg = conecg

    if etap == 4 and a[:4].count(white) > 2:
        c = 10
    if etap == 4 and a[:4].count(white) != 0:
        isp_tiles.append(pole.pole[x][y])

    for i in range(4):
        if etap == 4:
            trbl = trbl_for_d[i]
        else:
            trbl = trbl
        if poles[i] == "":
            if etap == 4 and c > 10:
                conecg = next(cg)
                isp_tiles = next(br)
                isp_ms = next(ms)
            if a[i] == white:
                conecg.append('')
            c += 1
        if poles[i] != "":
            t = for_prov.post_tile.get(poles[i])
            colich_next = t[:4].count(white)
            if a[i] == white and a[i] == t[:4][i - 2]:
                if etap == 4 and c > 10:
                    isp_tiles = next(br)
                    conecg = next(cg)
                    isp_tiles.append(pole.pole[x][y])
                    isp_ms = next(ms)
                if etap == 4 and (colich > 2 or colich == 1) and a[-1] != "ad" and (
                        (a[-1][1] == "bot" and a[2] == white and i == 2) or (
                        a[-1][1] == "left" and a[3] == white and i == 3) or (
                                a[-1][1] == "top" and a[0] == white and i == 0) or (
                                a[-1][1] == "right" and a[1] == white and i == 1)):
                    if [a[-1][0], a[-1][2]] not in isp_ms:
                        isp_ms.append([a[-1][0], a[-1][2]])
                        trbl_for_d[i].append("")
                elif etap == 4 and a[-1] != "ad" and colich == 2 and (
                        (a[-1][1] == "bot" and a[2] == white) or (a[-1][1] == "left" and a[3] == white) or (
                        a[-1][1] == "top" and a[0] == white) or (a[-1][1] == "right" and a[1] == white) or (
                                a[-1][1] == "center" and a[4] == white)):
                    if [a[-1][0], a[-1][2]] not in isp_ms:
                        isp_ms.append([a[-1][0], a[-1][2]])
                        trbl.append("")
                if colich_next == 2:
                    if poles[i] not in isp_tiles:
                        isp_tiles.append(poles[i])
                        if t[-1] != "ad" and (
                                (t[-1][1] == "bot" and t[2] == white) or (t[-1][1] == "left" and t[3] == white) or (
                                t[-1][1] == "top" and t[0] == white) or (t[-1][1] == "right" and t[1] == white) or (
                                        t[-1][1] == "center" and t[4] == white)):
                            isp_ms.append([t[-1][0], t[-1][2]])
                            trbl.append("")
                        pravila_doroga(coords[i][0], coords[i][1], i, isp_tiles, isp_ms, conecg, trbl)
                else:
                    if poles[i] not in isp_tiles:
                        isp_tiles.append(poles[i])
                        if t[-1] != "ad" and (
                                (t[-1][1] == "bot" and t[2] == white and i == 0) or (
                                t[-1][1] == "left" and t[3] == white and i == 1) or (
                                        t[-1][1] == "top" and t[0] == white and i == 2) or (
                                        t[-1][1] == "right" and t[1] == white and i == 3)):
                            isp_ms.append([t[-1][0], t[-1][2]])
                            trbl.append("")
                    elif poles[i] in isp_tiles and t[-1] != "ad" and [t[-1][0], t[-1][2]] not in isp_ms:
                        if (t[-1][1] == "bot" and t[2] == white and i == 0) or (
                                t[-1][1] == "left" and t[3] == black and i == 1) or (
                                t[-1][1] == "top" and t[0] == white and i == 2) or (
                                t[-1][1] == "right" and t[1] == white and i == 3):
                            isp_ms.append([t[-1][0], t[-1][2]])
                            trbl.append("")
                c += 1
    # print("AAAAAA")
    # print(doroga_ms)
    # print(doroga_schet)
    # print(conec_doroga)
    for i in range(3):
        for j in range(3 - i):
            if len(doroga_schet[i]) != 0:
                if colich > 2 and sorted(doroga_schet[i]) == sorted(doroga_schet[i + 1 + j]):
                    for lis in doroga_ms[i + 1 + j]:
                        if lis not in doroga_ms[i]:
                            doroga_ms[i].append(lis)
                    doroga_ms[i + 1 + j] = []
                    doroga_schet[i + 1 + j] = []
                    conec_doroga[i + 1 + j] = []
    if etap == 4:
        for i in range(4):
            if len(trbl_for_d[i]) != 0:
                trbl_for_d[4].extend(trbl_for_d[i])


# Функция, отвечающая за проверку правил, связанных с маныстырём
monastirs = {}


def pravila_monastir(x, y):
    global conecm, monastirs
    isp = []
    white = (128, 128, 128)
    black = (0, 0, 0)
    green = (0, 128, 0)
    a = for_prov.post_tile.get(pole.pole[x][y])
    if (a[4] == black and a[-1][1] == "center") and (
            a[:-2].count(green) == 4 or (a[:-2].count(green) == 3 and a[:-2].count(white) == 1)):
        monastirs[pole.pole[x][y]] = [a[-1][0], a[-1][2]]
        for i in range(3):
            for j in range(3):
                if i == 1 and j == 1:
                    continue
                elif pole.pole[x - 1 + i][y - 1 + j] != "" and pole.pole[x - 1 + i][y - 1 + j] not in monastirs[
                    pole.pole[x][y]]:
                    monastirs[pole.pole[x][y]] = monastirs[pole.pole[x][y]] + [pole.pole[x - 1 + i][y - 1 + j]]
                    isp.append([monastirs[pole.pole[x][y]], len(monastirs[pole.pole[x][y]])])
    for i in range(3):
        for j in range(3):
            if i == 1 and j == 1:
                continue
            elif pole.pole[x - 1 + i][y - 1 + j] in monastirs and pole.pole[x][y] not in monastirs[
                pole.pole[x - 1 + i][y - 1 + j]]:
                monastirs[pole.pole[x - 1 + i][y - 1 + j]] = monastirs[pole.pole[x - 1 + i][y - 1 + j]] + [
                    pole.pole[x][y]]
                isp.append(
                    [monastirs[pole.pole[x - 1 + i][y - 1 + j]], len(monastirs[pole.pole[x - 1 + i][y - 1 + j]])])
    return isp


gorod_schet = [[], []]


def isp_tileses():
    global gorod_schet
    for i in range(2):
        yield gorod_schet[i]


gorod_ms = [[], []]


def isp_mses():
    global gorod_ms
    for i in range(2):
        yield gorod_ms[i]


conec_g = [[], []]


def isp_conec():
    global conec_g
    for i in range(2):
        yield conec_g[i]


trbl_for_g = [[], [], [], [], []]


def pravila_gorod(x, y, etap, isp_tiles=None, isp_ms=None, conecg=None, trbl=None):
    global conec_g, gorod_schet, gorod_ms, trbl_for_g
    black = (0, 0, 0)
    a = for_prov.post_tile.get(pole.pole[x][y])
    poles = [pole.pole[x][y - 1], pole.pole[x + 1][y], pole.pole[x][y + 1], pole.pole[x - 1][y]]
    coords = [(x, y - 1), (x + 1, y), (x, y + 1), (x - 1, y)]
    colich = a[:4].count(black)
    br = isp_tileses()
    ms = isp_mses()
    cg = isp_conec()
    c = 0

    if isp_tiles == None:
        isp_tiles = next(br)
        isp_ms = next(ms)
        conecg = next(cg)
    else:
        isp_tiles = isp_tiles
        isp_ms = isp_ms
        conecg = conecg

    if etap == 4 and a[:4].count(black) == 2 and a[4] != black:
        c = 10
    if etap == 4 and a[:4].count(black) != 0:
        isp_tiles.append(pole.pole[x][y])
    for i in range(4):
        if etap == 4:
            trbl = trbl_for_g[i]
        else:
            trbl = trbl
        if a[i] == black and poles[i] == "":
            if etap == 4 and c > 10:
                conecg = next(cg)
                isp_tiles = next(br)
                isp_ms = next(ms)
            conecg.append('')
            c += 1
        if poles[i] != "":
            t = for_prov.post_tile.get(poles[i])
            colich_next = t[:4].count(black)
            if a[i] == black and a[i] == t[:4][i - 2]:
                if etap == 4 and c > 10:
                    isp_tiles = next(br)
                    conecg = next(cg)
                    isp_tiles.append(pole.pole[x][y])
                    isp_ms = next(ms)
                if etap == 4 and a[4] != black and a[-1] != "ad" and (
                        (a[-1][1] == "bot" and a[2] == black and i == 2) or (
                        a[-1][1] == "left" and a[3] == black and i == 3) or (
                                a[-1][1] == "top" and a[0] == black and i == 0) or (
                                a[-1][1] == "right" and a[1] == black and i == 1)):
                    if [a[-1][0], a[-1][2]] not in isp_ms:
                        isp_ms.append([a[-1][0], a[-1][2]])
                        trbl.append("")
                elif etap == 4 and a[-1] != "ad" and a[4] == black and (
                        (a[-1][1] == "bot" and a[2] == black) or (a[-1][1] == "left" and a[3] == black) or (
                        a[-1][1] == "top" and a[0] == black) or (a[-1][1] == "right" and a[1] == black) or (
                                a[-1][1] == "center" and a[4] == black)):
                    if [a[-1][0], a[-1][2]] not in isp_ms:
                        isp_ms.append([a[-1][0], a[-1][2]])
                        trbl.append("")
                if colich_next >= 3 or (colich_next == 2 and t[4] == black):
                    if poles[i] not in isp_tiles:
                        isp_tiles.append(poles[i])
                        if t[-1] != "ad" and (
                                (t[-1][1] == "bot" and t[2] == black) or (t[-1][1] == "left" and t[3] == black) or (
                                t[-1][1] == "top" and t[0] == black) or (t[-1][1] == "right" and t[1] == black) or (
                                        t[-1][1] == "center" and t[4] == black)):
                            isp_ms.append([t[-1][0], t[-1][2]])
                            trbl.append("")
                        pravila_gorod(coords[i][0], coords[i][1], i, isp_tiles, isp_ms, conecg, trbl)
                else:
                    if poles[i] not in isp_tiles:
                        isp_tiles.append(poles[i])
                        if t[-1] != "ad" and (
                                (t[-1][1] == "bot" and t[2] == black and i == 0) or (
                                t[-1][1] == "left" and t[3] == black and i == 1) or (
                                        t[-1][1] == "top" and t[0] == black and i == 2) or (
                                        t[-1][1] == "right" and t[1] == black and i == 3)):
                            isp_ms.append([t[-1][0], t[-1][2]])
                            trbl.append("")
                    elif poles[i] in isp_tiles and t[-1] != "ad" and [t[-1][0], t[-1][2]] not in isp_ms:
                        if (t[-1][1] == "bot" and t[2] == black and i == 0) or (
                                t[-1][1] == "left" and t[3] == black and i == 1) or (
                                t[-1][1] == "top" and t[0] == black and i == 2) or (
                                t[-1][1] == "right" and t[1] == black and i == 3):
                            isp_ms.append([t[-1][0], t[-1][2]])
                            trbl.append("")
                c += 1
    if colich != 0 and sorted(gorod_schet[0]) == sorted(gorod_schet[1]):
        for lis in gorod_ms[1]:
            if lis not in gorod_ms[0]:
                gorod_ms[0].append(lis)
        gorod_ms[1] = []
        gorod_schet[1] = []
        gorod_schet[0].append(gorod_schet[0][0])
        conec_g[1] = []
    if etap == 4:
        for i in range(4):
            if len(trbl_for_g[i]) != 0:
                trbl_for_g[4].extend(trbl_for_g[i])


def result(ochki, game):
    if len(ochki) != 0:
        ochki = ochki
        itog = {}
        for i in ochki:
            itog[i[1].name] = [ochki.count(i), i[1], i[0], i[2]]
        ostatok = []
        for i in itog:
            ostatok.append([itog[i][0], i, itog[i][1], itog[i][2], itog[i][3]])
        ostatok.sort(reverse=True)
        maximum = ostatok[0][0]
        for i in ostatok:
            if i[0] != maximum:
                ostatok.remove(i)
        for i in ostatok:
            i[2].add_ochki(i[3], i[4], game)


# Функция, для отображения игрового поля во время игры
def pokaz(do_mipl):
    camera.update(person)
    for e in pole_sprites:
        window.blit(e.image, camera.apply(e))
    for e in tiles_sprites:
        window.blit(e.image, camera.apply(e))
    for e in player_sprites:
        window.blit(e.image, camera.apply(e))
    window.blit(person.image, camera.apply(person))
    screen.blit(textsurface1, (width + 5, 0))
    textsurface2 = myfont.render(str(len(pole.not_frames)), False, RED)
    screen.blit(textsurface2, (width + 30, 30))
    pole.sled_tile()
    textsurface3 = myfont.render("Миплы:", False, mipls[(len(pole.not_frames) - do_mipl) % len(mipls)].color)
    screen.blit(textsurface3, (width, 190))
    textsurface4 = myfont.render(str(mipls[(len(pole.not_frames) - do_mipl) % len(mipls)].mipls), False,
                                 mipls[(len(pole.not_frames) - do_mipl) % len(mipls)].color)
    screen.blit(textsurface4, (width + 30, 220))
    textsurface5 = myfont.render("Очки:", False, mipls[(len(pole.not_frames) - do_mipl) % len(mipls)].color)
    screen.blit(textsurface5, (width + 10, 250))
    textsurface6 = myfont.render(str(mipls[(len(pole.not_frames) - do_mipl) % len(mipls)].ochki), False,
                                 mipls[(len(pole.not_frames) - do_mipl) % len(mipls)].color)
    screen.blit(textsurface6, (width + 30, 280))
    screen.blit(window, (0, 0))
    screen.blit(pole.image, (width, 80))
    textsurface7 = myfont.render("Игрок" + str(mipls[(len(pole.not_frames) - do_mipl) % len(mipls)].name) + ":", False,
                                 mipls[(len(pole.not_frames) - do_mipl) % len(mipls)].color)
    screen.blit(textsurface7, (width + 2, 160))


# Функция для перемещения персонажа
def move(x, y):
    screen.fill((255, 255, 255))
    if x == -1 and person.rect.x > 0 or x == 1 and person.rect.x < 5680 or y == -1 and person.rect.y > 0 or y == 1 and person.rect.y < 5680:
        person.update(x, y)
    else:
        person.update(0, 0)
    pokaz(1)


# Функция, которая отвечает за возможность поставить мипла
def new_mipl():
    import math
    global running, game, trbl_for_d, doroga_schet, doroga_ms, conec_doroga, conec_g, gorod_schet, gorod_ms, trbl_for_g
    new = True
    Mouse_x, Mouse_y = 0, 0
    while new == True:
        a = len(pole.not_frames) % len(mipls)
        if (Mouse_x, Mouse_y) != pygame.mouse.get_pos():
            screen.fill((255, 255, 255))
            pokaz(0)
        muse.update(Mouse_x - camera.state.x, Mouse_y - camera.state.y)
        Mouse_x, Mouse_y = pygame.mouse.get_pos()
        if muse.rect.colliderect(tiles_sprites.sprites()[-1].rect):
            screen.blit(mipls[a].pokaz(Mouse_x, Mouse_y), (Mouse_x - 10, Mouse_y - 10))
        screen.blit(load_image(["Kark.png", ], 1, 1)[0], (width, 80))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                new = False

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    Mouse_x, Mouse_y = pygame.mouse.get_pos()
                    muse.update(Mouse_x - camera.state.x, Mouse_y - camera.state.y)
                    if pole.pole[muse.rect.x // 80][muse.rect.y // 80] != "":
                        pravila_doroga(muse.rect.x // 80, muse.rect.y // 80, 4)
                        pravila_gorod(muse.rect.x // 80, muse.rect.y // 80, 4)
                        white = (128, 128, 128)
                        black = (0, 0, 0)
                        num = pole.pole[muse.rect.x // 80][muse.rect.y // 80]
                        inf = for_prov.post_tile.get(num)
                        colichd = inf[:4].count(white)
                        colichg = inf[:4].count(black)
                        sx = muse.rect.x
                        sy = muse.rect.y
                        til = pole.tiles[num]
                        tile_x = til.rect.x + 40
                        tile_y = til.rect.y + 40
                        myradians = math.atan2(tile_y - sy, tile_x - sx)
                        mydegrees = math.degrees(myradians)
                        dlina = math.sqrt((tile_x - sx) ** 2 + (tile_y - sy) ** 2)
                        min_dlin = 15
                        if mydegrees >= 45 and mydegrees < 135 and (
                                dlina > min_dlin or (
                                dlina <= min_dlin and inf[:-2].count(white) >= 2 and inf[0] == white)):
                            polozd = 0
                        elif mydegrees >= 135 or mydegrees < -135 and (
                                dlina > min_dlin or (
                                dlina <= min_dlin and inf[:-2].count(white) >= 2 and inf[1] == white)):
                            polozd = 1
                        elif mydegrees < -45 and mydegrees >= -135 and (
                                dlina > min_dlin or (
                                dlina <= min_dlin and inf[:-2].count(white) >= 2 and inf[2] == white)):
                            polozd = 2
                        elif mydegrees < 45 and mydegrees >= -45 and (
                                dlina > min_dlin or (
                                dlina <= min_dlin and inf[:-2].count(white) >= 2 and inf[3] == white)):
                            polozd = 3
                        else:
                            polozd = 4
                        if len(tiles_sprites.sprites()) != 0 and muse.rect.colliderect(
                                tiles_sprites.sprites()[-1].rect) and (
                                (polozd == 4 and inf[4] == black and inf[:4].count(white) <= 1 and inf[:4].count(
                                    black) == 0)
                                or (inf[:4].count(white) != 0 and (
                                (len(trbl_for_d[polozd]) == 0 and inf[polozd] == white and
                                 (colichd == 1 or colichd > 2)) or (colichd == 2 and len(trbl_for_d[0]) == 0 and
                                                                    len(trbl_for_d[1]) == 0 and len(
                                    trbl_for_d[2]) == 0 and
                                                                    len(trbl_for_d[3]) == 0 and inf[polozd] == white)))
                                or (inf[:4].count(black) != 0 and (
                                (len(trbl_for_g[polozd]) == 0 and inf[polozd] == black and
                                 (colichg == 1 or (colichg == 2 and inf[4] != black))) or
                                (((colichg == 2 and inf[4] == black) or colichg > 2) and
                                 len(trbl_for_g[0]) == 0 and len(trbl_for_g[1]) == 0 and
                                 len(trbl_for_g[2]) == 0 and len(trbl_for_g[3]) == 0 and inf[polozd] == black)))):
                            # or (inf[polozd] != white and inf[polozd] != black)
                            mipls[a].add_mipl(muse.rect.x - 10, muse.rect.y - 10)
                            if mydegrees >= 45 and mydegrees < 135 and (
                                    dlina > min_dlin or (
                                    dlina <= min_dlin and inf[:-2].count(white) >= 2 and inf[0] == white)):
                                ba = for_prov.post_tile.get(num)[:-1] + [
                                    [player_sprites.sprites()[-1], "top", mipls[a]]]
                            elif mydegrees >= 135 or mydegrees < -135 and (
                                    dlina > min_dlin or (
                                    dlina <= min_dlin and inf[:-2].count(white) >= 2 and inf[1] == white)):
                                ba = for_prov.post_tile.get(num)[:-1] + [
                                    [player_sprites.sprites()[-1], "right", mipls[a]]]
                            elif mydegrees < -45 and mydegrees >= -135 and (
                                    dlina > min_dlin or (
                                    dlina <= min_dlin and inf[:-2].count(white) >= 2 and inf[2] == white)):
                                ba = for_prov.post_tile.get(num)[:-1] + [
                                    [player_sprites.sprites()[-1], "bot", mipls[a]]]
                            elif mydegrees < 45 and mydegrees >= -45 and (
                                    dlina > min_dlin or (
                                    dlina <= min_dlin and inf[:-2].count(white) >= 2 and inf[3] == white)):
                                ba = for_prov.post_tile.get(num)[:-1] + [
                                    [player_sprites.sprites()[-1], "left", mipls[a]]]
                            else:
                                ba = for_prov.post_tile.get(num)[:-1] + [
                                    [player_sprites.sprites()[-1], "center", mipls[a]]]
                            for_prov.post_tile.update({num: ba})
                            move(0, 0)
                            new = False
                        conec_doroga = [[], [], [], []]
                        doroga_schet = [[], [], [], []]
                        doroga_ms = [[], [], [], []]
                        trbl_for_d = [[], [], [], [], []]
                        conec_g = [[], []]
                        gorod_schet = [[], []]
                        gorod_ms = [[], []]
                        trbl_for_g = [[], [], [], [], []]
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game = 2
                    button1.rect.x, button1.rect.y = ((width + 80) / 2 - 260 / 2, (height / 2) - 140)
                    button2.rect.x, button2.rect.y = ((width + 80) / 2 - 260 / 2, (height / 2) + 20)
                    button2.sdvig(y=(height / 2) + 215)
                    new = False
                elif event.key == pygame.K_SPACE:
                    new = False

        pygame.draw.rect(screen, (255, 255, 255), (width + 30, 500, 80, 80))
        screen.blit(update_fps(), (width + 30, 500))
        pygame.display.flip()
        clock.tick(fps)


# Создание основных классов, необходимых для работы игры и добавление в спрайты
pole_sprites = pygame.sprite.Group()
tiles_sprites = pygame.sprite.Group()
person_sprites = pygame.sprite.Group()
b = Tiles(load_image(["b1.jpg", "b2.jpg", "b3.jpg"], 4, 6), 4, 6)
f = Fon(load_image(["igr_pole.jpg", ], 2, 2), 2, 2)
pl_tiles = []
pole = Pole(b.frames, f.frames, tiles_sprites, pole_sprites, pl_tiles)
pole.num(0)
person = Person()
person_sprites.add(person)
screen.fill((255, 255, 255))
textsurface1 = myfont.render("Тайлы:", False, RED)
# Создание кнопок для Меню
but1 = pygame.image.load("img/button1.png").convert()
but2 = pygame.image.load("img/button2.png").convert()
button1 = Button(but1, (height / 2) - 140)
button2 = Button(but1, (height / 2) + 20)
muse = Muse(pygame.image.load("img/muse.png").convert())
button1_sprites = pygame.sprite.Group()
button2_sprites = pygame.sprite.Group()
button1_sprites.add(button1)
button2_sprites.add(button2)
player_sprites = pygame.sprite.Group()
colors = [ORANGE, BLACK, RED, GREEN, BLUE]
pygame.display.set_icon(pygame.image.load("img/Kark.png").convert())
pygame.display.set_caption("Каркассон v.1.0")


# Функция, для вывода цвета
def new_igrok():
    global colors
    a = random.choice(colors)
    colors.remove(a)
    return a


mipls = []
kol_players = 2  # Начальное число игроков

game = 0  # Переменная, которая позволяет переходить между игрой и меню
game_pos = 0
running = True

# Ограничить отмену в пределах 2 ходов.
# Сделать меню с: выбором цвета и имени


# Основной цикл работы
while running:
    Mouse_x, Mouse_y = pygame.mouse.get_pos()
    # ___МЕНЮ___
    if game == 0:
        muse.update(Mouse_x, Mouse_y)
        screen.fill((255, 255, 255))
        menu_fon = pygame.image.load("img/menu_fon.jpg").convert()
        menu_fon = pygame.transform.scale(menu_fon, (width + 80, height))
        screen.blit(menu_fon, (0, 0))

        if pygame.sprite.spritecollide(muse, button1_sprites, False):
            textsurfaceb1 = myfont.render("НАЧАТЬ ИГРУ", False, RED)
            button1.update(but2)
        else:
            button1.update(but1)
            textsurfaceb1 = myfont.render("НАЧАТЬ ИГРУ", False, BLUE)

        if pygame.sprite.spritecollide(muse, button2_sprites, False):
            textsurfaceb2 = myfont.render("Добавить игроков", False, RED)
            button2.update(but2)
        else:
            textsurfaceb2 = myfont.render("Добавить игроков", False, BLUE)
            button2.update(but1)

        for e in button1_sprites:
            screen.blit(e.image, e.rect)
        for e in button2_sprites:
            screen.blit(e.image, e.rect)

        screen.blit(textsurfaceb1, ((width / 2) - 40, (height / 2) - 115))
        screen.blit(textsurfaceb2, ((width / 2) - 45, (height / 2) + 45))
        pygame.draw.ellipse(screen, WHITE, ((width / 2) - 85, (height / 2) + 133, 250, 45))
        textsurfacem1 = myfont.render("Количество игроков = " + str(kol_players), False, RED)
        screen.blit(textsurfacem1, ((width / 2) - 75, (height / 2) + 140))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if pygame.sprite.spritecollide(muse, button1_sprites, False):
                        button2.sdvig(y=(height / 2) + 215)
                        game = 1
                        for i in range(kol_players):
                            mipls.append(Igrok(new_igrok(), player_sprites))
                        move(0, 0)

                    if pygame.sprite.spritecollide(muse, button2_sprites, False):
                        if kol_players < 5:
                            kol_players += 1

                elif event.button == 3:
                    if pygame.sprite.spritecollide(muse, button2_sprites, False):
                        if kol_players > 2:
                            kol_players -= 1

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

                elif event.key == pygame.K_F11:
                    if fullscr == 1:
                        fullscr = 0
                    else:
                        fullscr = 1
                    fullscreen(fullscr)
                    button1.rect.x, button1.rect.y = ((width + 80) / 2 - 260 / 2, (height / 2) - 140)
                    button2.rect.x, button2.rect.y = ((width + 80) / 2 - 260 / 2, (height / 2) + 20)

        pygame.display.flip()
        clock.tick(fps)

    # ___ИГРА___
    elif len(pole.not_frames) > 0 and game == 1:
        a = len(pole.not_frames) % len(mipls)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    Mouse_x, Mouse_y = pygame.mouse.get_pos()
                    if pole.pole[(Mouse_x - camera.state.x) // 80][(Mouse_y - camera.state.y) // 80] != "":
                        print(pole.pole[(Mouse_x - camera.state.x) // 80][(Mouse_y - camera.state.y) // 80],
                              for_prov.post_tile.get(
                                  pole.pole[(Mouse_x - camera.state.x) // 80][(Mouse_y - camera.state.y) // 80])[:5])

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game = 2
                    button1.rect.x, button1.rect.y = ((width + 80) / 2 - 260 / 2, (height / 2) - 140)
                    button2.rect.x, button2.rect.y = ((width + 80) / 2 - 260 / 2, (height / 2) + 20)
                    button2.sdvig(x=button2.rect.x, y=(height / 2) + 215)

                if event.key == pygame.K_RIGHT:
                    move(1, 0)

                elif event.key == pygame.K_LEFT:
                    move(-1, 0)

                elif event.key == pygame.K_UP:
                    move(0, -1)

                elif event.key == pygame.K_DOWN:
                    move(0, 1)

                elif event.key == pygame.K_F11:
                    if fullscr == 1:
                        fullscr = 0
                    else:
                        fullscr = 1
                    fullscreen(fullscr)
                    move(0, 0)

                elif event.key == pygame.K_z:
                    if pole.num_of_tile != 0:
                        white = (128, 128, 128)
                        black = (0, 0, 0)
                        sbros = 2
                        for i in pole.isp_tile:
                            if pole.pole[i[-1] + 1][i[-2]] == "":
                                if for_prov.new_tile(i[-2], i[-1] + 1) == 0:
                                    print(pole.pole[i[-1]][i[-2]])
                                    sbros = 3
                                    break
                            if pole.pole[i[-1] - 1][i[-2]] == "":
                                if for_prov.new_tile(i[-2], i[-1] - 1) == 0:
                                    print(pole.pole[i[-1]][i[-2]])
                                    sbros = 3
                                    break
                            if pole.pole[i[-1]][i[-2] - 1] == "":
                                if for_prov.new_tile(i[-2] - 1, i[-1]) == 0:
                                    print(pole.pole[i[-1]][i[-2]])
                                    sbros = 3
                                    break
                            if pole.pole[i[-1]][i[-2] + 1] == "":
                                if for_prov.new_tile(i[-2] + 1, i[-1]) == 0:
                                    print(pole.pole[i[-1]][i[-2]])
                                    sbros = 3
                                    break
                        if sbros == 2:
                            print("Sbros")
                            pole.not_frames.remove(pole.num_of_tile)
                            if len(pole.not_frames) != 0:
                                pole.num(1)
                            move(0, 0)

                elif event.key == pygame.K_0:
                    for_prov.povorot()
                    pole.frames1[pole.num_of_tile] = pygame.transform.rotate(pole.frames1[pole.num_of_tile], -90)
                    move(0, 0)

                # elif event.key == pygame.K_z:
                # if len(pl_tiles) > 0:
                # if len(tiles_sprites.sprites()) != 0 and len(player_sprites.sprites()) != 0 and player_sprites.sprites()[-1].rect.colliderect(tiles_sprites.sprites()[-1].rect):
                # mipls[a].otmena()
                # hod_mipl = None
                # pole.otmena()
                # move(0, 0)

                elif event.key == pygame.K_SPACE:
                    moz = for_prov.new_tile(person.rect.y // 80, person.rect.x // 80)
                    if moz == 0:
                        pr = pole.new_tile(person.rect.y // 80, person.rect.x // 80)
                        if pr == 1:
                            if len(pole.not_frames) != 0:
                                pole.num(1)
                            new_mipl()

                            ochki = []
                            pravila_gorod(person.rect.x // 80, person.rect.y // 80, 4)
                            if len(gorod_ms[0]) != 0 and len(conec_g[0]) == 0:
                                for lk in gorod_ms[0]:
                                    ochki.append(["g", lk[1], len(gorod_schet[0])])
                                    lk[1].del_mipl(lk[0])
                                result(ochki, 1)
                                ochki = []
                            if len(gorod_ms[1]) != 0 and len(conec_g[1]) == 0:
                                for lk in gorod_ms[1]:
                                    ochki.append(["g", lk[1], len(gorod_schet[1])])
                                    lk[1].del_mipl(lk[0])
                                result(ochki, 1)
                                ochki = []
                            conec_g = [[], []]
                            gorod_schet = [[], []]
                            gorod_ms = [[], []]
                            trbl_for_g = [[], [], [], [], []]

                            isp_monas = pravila_monastir(person.rect.x // 80, person.rect.y // 80)
                            for k in range(len(isp_monas)):
                                if isp_monas[k][1] == 10:
                                    ochki.append(["m", isp_monas[k][0][1], isp_monas[k][1] - 1])
                                    isp_monas[k][0][1].del_mipl(isp_monas[k][0][0])
                                result(ochki, 1)
                                ochki = []

                            if for_prov.post_tile.get(pole.pole[person.rect.x // 80][person.rect.y // 80])[:-2].count(
                                    (128, 128, 128)) != 0:
                                pravila_doroga(person.rect.x // 80, person.rect.y // 80, 4)
                                for i in range(4):
                                    if len(doroga_ms[i]) != 0 and len(conec_doroga[i]) == 0:
                                        for lk in doroga_ms[i]:
                                            ochki.append(["d", lk[1], len(doroga_schet[i])])
                                            lk[1].del_mipl(lk[0])
                                    result(ochki, 1)
                                    ochki = []
                                conec_doroga = [[], [], [], []]
                                doroga_schet = [[], [], [], []]
                                doroga_ms = [[], [], [], []]
                                trbl_for_d = [[], [], [], [], []]
                        else:
                            for_prov.post_tile.pop(pole.num_of_tile)
                    move(0, 0)
        pygame.draw.rect(screen, (255, 255, 255), (width + 30, 500, 80, 80))
        screen.blit(update_fps(), (width + 30, 500))
        pygame.display.flip()
        clock.tick(fps)

    # __Пауза__
    elif game == 2:
        muse.update(Mouse_x, Mouse_y)
        screen.fill((255, 255, 255))
        menu_fon = pygame.image.load("img/menu_fon.jpg").convert()
        menu_fon = pygame.transform.scale(menu_fon, (width + 80, height))
        screen.blit(menu_fon, (0, 0))

        if pygame.sprite.spritecollide(muse, button1_sprites, False):
            button1.update(but2)
        else:
            button1.update(but1)
        for e in button1_sprites:
            screen.blit(e.image, e.rect)

        if pygame.sprite.spritecollide(muse, button2_sprites, False):
            button2.update(but2)
        else:
            button2.update(but1)
        for e in button2_sprites:
            screen.blit(e.image, e.rect)

        textsurfaceb1 = myfont.render("ПРОДОЛЖИТЬ ИГРУ", False, RED)
        screen.blit(textsurfaceb1, ((width / 2) - 64, (height / 2) - 115))
        textsurfaceb3 = myfont.render("НОВАЯ ИГРА", False, RED)
        screen.blit(textsurfaceb3, ((width / 2) - 30, (height / 2) + 240))
        pygame.draw.rect(screen, (255, 255, 255),
                         ((width / 2) - 80, (height / 2) - 45, 242, 30 * len(mipls) + 16))
        pygame.draw.rect(screen, (64, 128, 255),
                         ((width / 2) - 80, (height / 2) - 45, 242, 30 * len(mipls) + 16), 8)
        ots = 80
        for i in mipls:
            textsurfaceb2 = myfont.render("Игрок{} имеет {} очков".format(i.name, i.ochki), False, i.color)
            screen.blit(textsurfaceb2, ((width / 2) - 64, (height / 2) - 115 + ots))
            ots += 30

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if pygame.sprite.spritecollide(muse, button1_sprites, False):
                        game = 1
                        move(0, 0)
                    elif pygame.sprite.spritecollide(muse, button2_sprites, False):
                        if new_game():
                            screen = pygame.display.set_mode((size[0] + 80, size[1]))
                            camera = Camera(camera_func, lvl_w, lvl_h)
                            window = pygame.Surface(size)
                            for_prov = For_prov([r"img\b1_ram.jpg", r"img\b2_ram.jpg", r"img\b3_ram.jpg"], 4, 6)
                            monastirs = {}
                            pole_sprites = pygame.sprite.Group()
                            tiles_sprites = pygame.sprite.Group()
                            person_sprites = pygame.sprite.Group()
                            b.sbros()
                            f.sbros()
                            b = Tiles(load_image(["b1.jpg", "b2.jpg", "b3.jpg"], 4, 6), 4, 6)
                            f = Fon(load_image(["igr_pole.jpg", ], 2, 2), 2, 2)
                            pl_tiles = []
                            colors = [ORANGE, BLACK, RED, GREEN, BLUE]
                            pole = Pole(b.frames, f.frames, tiles_sprites, pole_sprites, pl_tiles)
                            pole.num(0)
                            person = Person()
                            person_sprites.add(person)
                            screen.fill((255, 255, 255))
                            textsurface1 = myfont.render("Тайлы:", False, RED)
                            button1.rect.x, button1.rect.y = ((width + 80) / 2 - 260 / 2, (height / 2) - 140)
                            button2.rect.x, button2.rect.y = ((width + 80) / 2 - 260 / 2, (height / 2) + 20)
                            player_sprites = pygame.sprite.Group()
                            mipls[0].sbros()
                            mipls = []
                            kol_players = 2
                            game = 0
                            game_pos = 0
                            running = True

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game = 1
                    move(0, 0)
                    # running = False

                elif event.key == pygame.K_F11:
                    if fullscr == 1:
                        fullscr = 0
                    else:
                        fullscr = 1
                    fullscreen(fullscr)
                    button1.rect.x, button1.rect.y = ((width + 80) / 2 - 260 / 2, (height / 2) - 140)
                    button2.rect.x, button2.rect.y = ((width + 80) / 2 - 260 / 2, (height / 2) + 20)
                    button2.sdvig(x=button2.rect.x, y=(height / 2) + 215)

        pygame.display.flip()
        clock.tick(fps)

    # Конец игры
    else:
        game_pos = 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game = 2
                    button1.rect.x, button1.rect.y = ((width + 80) / 2 - 260 / 2, (height / 2) - 140)
                    button2.rect.x, button2.rect.y = ((width + 80) / 2 - 260 / 2, (height / 2) + 20)
                    button2.sdvig(y=(height / 2) + 215)

                if event.key == pygame.K_RIGHT:
                    move(1, 0)

                elif event.key == pygame.K_LEFT:
                    move(-1, 0)

                elif event.key == pygame.K_UP:
                    move(0, -1)

                elif event.key == pygame.K_DOWN:
                    move(0, 1)

                elif event.key == pygame.K_F11:
                    if fullscr == 1:
                        fullscr = 0
                    else:
                        fullscr = 1
                    fullscreen(fullscr)
                    move(0, 0)

        screen.blit(window, (0, 0))
        pygame.display.flip()
        clock.tick(fps)
    clock.tick(fps)
pygame.quit()
