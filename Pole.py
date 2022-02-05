import pygame, random

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
#Создаёт начальное поле, заполненное фоном
class Pole(pygame.sprite.Sprite):
    def __init__(self, frames1, frames2, tiles_sprites, pole_sprites, pl_tiles):
        super().__init__()
        self.tiles = []
        for i in range(72):
            self.tiles.append("")
        self.tiles_sprites, self.pole_sprites, self.pl_tiles = tiles_sprites, pole_sprites, pl_tiles
        self.postavl = []
        self.isp_tile = []
        self.frames1 = frames1
        self.frames2 = frames2
        self.image = pygame.Surface((80,80))
        self.image = self.frames2[0]
        self.rect = pygame.Rect(0, 0, 80, 80)
        self.dlin = len(self.frames1)
        self.not_frames = []
        for i in range(self.dlin):
            self.not_frames.append(i)
        self.pole = []
        for i in range(self.dlin):
            a = []
            for i in range(self.dlin):
                a.append("")
            self.pole.append(a)
        for i in range(self.dlin):
            for j in range(self.dlin):
                if self.pole[i][j] == "":
                    self.image = pygame.Surface((80, 80))
                    if i%2 == 0:
                        self.image = self.frames2[j%2]
                    else:
                        self.image = self.frames2[2+ j % 2]
                    self.rect = self.image.get_rect()
                    self.rect.x = j * 80
                    self.rect.y = i * 80
                    self.border = pygame.Rect(0, 0, 80, 80)
                    pygame.draw.rect(self.image, BLACK, self.border, 1)
                    pl = Platform(self.image, self.rect.x, self.rect.y)
                    self.pole_sprites.add(pl)
                else:
                    self.image = pygame.Surface((80, 80))
                    self.image = self.frames1[self.pole[i][j]]
                    self.rect = self.image.get_rect()
                    self.rect.x = j * 80
                    self.rect.y = i * 80
                    self.border = pygame.Rect(0, 0, 80, 80)
                    pygame.draw.rect(self.image, BLACK, self.border, 1)
                    pl = Platform(self.image, self.rect.x, self.rect.y)
                    self.tiles_sprites.add(pl)
                    self.pl_tiles.append(pl)
        #self.plisa = [2,8,5,14,4]
    #Выбирает номер для следующего тайла
    def num(self, r):
        if r == 0:
            num = 0
        else:
            num = random.choice(self.not_frames)
            #num = self.plisa.pop(-1)
        self.num_of_tile = num
        self.sled_tile()

    #Создаёт картинку для следующего тайла
    def sled_tile(self):
        self.image = pygame.Surface((80, 80))
        self.image = self.frames1[self.num_of_tile]

    #Выводит новый тайл
    def new_tile(self, col, row):
        if self.pole[row][col] == "":
            if self.num_of_tile == 0 or self.pole[row-1][col] != "" or self.pole[row][col-1] != "" or self.pole[row+1][col] != "" or self.pole[row][col+1] != "":
                num = self.num_of_tile
                self.pole[row][col] = num
                self.not_frames.remove(num)
                self.image = pygame.Surface((80, 80))
                self.image = self.frames1[num]
                self.rect = self.image.get_rect()
                self.rect.x = row * 80
                self.rect.y = col * 80
                self.border = pygame.Rect(0, 0, 80, 80)
                pygame.draw.rect(self.image, BLACK, self.border, 1)
                pl = Platform_Tile(self.image, self.rect.x, self.rect.y)
                self.tiles_sprites.add(pl)
                self.pl_tiles.append(pl)
                self.isp_tile.append((self.num_of_tile, col, row))
                self.tiles[num] = pl
                return 1
            else:
                return 0
        else:
            return 0

    #Возврящает ход на 1 назад (Удаляет с поля последний поставленный тайл)
    def otmena(self):
        a = self.isp_tile.pop(-1)
        self.num_of_tile = a[0]
        self.not_frames.append(a[0])
        self.pole[a[2]][a[1]] = ""
        self.pl_tiles.pop(-1).kill()

#Получает изображение фона и формирует его для показа
class Fon(pygame.sprite.Sprite):
    frames = []
    def __init__(self, images, columns, rows):
        super().__init__()
        self.cut_image(images, columns, rows)

    def cut_image(self, images, columns, rows):
        for k in images:
            self.rect = pygame.Rect(0, 0, k.get_width() // columns, k.get_height() // rows)
            for j in range(rows):
                for i in range(columns):
                    frame_location = (self.rect.w * i, self.rect.h * j)
                    self.frames.append(k.subsurface(pygame.Rect(frame_location, self.rect.size)))
    def sbros(self):
        Fon.frames = []

#Получает изображение тайлов и формирует из них список
class Tiles(pygame.sprite.Sprite):
    frames = []
    def __init__(self, images, columns, rows):
        super().__init__()
        self.cut_image(images, columns, rows)
        self.frames[0], self.frames[len(self.frames) - 1] = self.frames[len(self.frames) - 1], self.frames[0]

    def cut_image(self, images, columns, rows):
        for k in images:
            self.rect = pygame.Rect(0, 0, k.get_width() // columns, k.get_height() // rows)
            for j in range(rows):
                for i in range(columns):
                    frame_location = (self.rect.w * i, self.rect.h * j)
                    self.frames.append(k.subsurface(pygame.Rect(frame_location, self.rect.size)))
    def sbros(self):
        Tiles.frames = []

#Спрайт для фона
class Platform(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

#Спрайт для тайла
class Platform_Tile(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

if __name__ == "__main__":
    print("Вы запустили этот модуль напрямую (а не импортировали его).")
    input("\n\nНажмите Enther для выхода.")