import pygame, random

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 128, 0)

#Спрайт для курсора мыши
class Muse(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        self.image = pygame.Surface((1, 1))
        self.image = image
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.rect = pygame.Rect(self.rect.x, self.rect.y, 1, 1)
    def update(self, x, y):
        self.rect.x = x
        self.rect.y = y

#Спрайт для мипла
class Mipl(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image = image
        self.image = pygame.transform.scale(self.image, (20,20))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.rect = pygame.Rect(self.rect.x, self.rect.y, 20, 20)

#Персонаж
class Igrok():
    names = "1234567"
    def __init__(self, color, player_sprites):
        self.mipls = 8
        self.mipls_pos = []
        if color == RED:
            cvet = "red"
        elif color == BLUE:
            cvet = "blue"
        elif color == GREEN:
            cvet = "green"
        elif color == BLACK:
            cvet = "black"
        else:
            cvet = "orange"
        self.image = pygame.image.load("img/" + cvet + "_mipl.jpg").convert()
        self.player_sprites = player_sprites
        self.color = color
        self.ochki = 0
        self.name = Igrok.names[0]
        Igrok.names = Igrok.names[1:]

    #Добавляет мипла на поле
    def add_mipl(self, x, y):
        if self.mipls > 0:
            mipl = Mipl(self.image, x, y)
            self.player_sprites.add(mipl)
            self.mipls_pos.append([mipl])
            self.mipls += -1

    def pokaz(self, x, y):
        return Mipl(self.image, x, y).image

     #Удаляет мипла с поля
    def del_mipl(self, mipl):
        self.mipls += 1
        #print(mipl)
        #print(self.mipls_pos)
        self.mipls_pos.remove([mipl])
        mipl.remove(self.player_sprites)

    def otmena(self):
        self.mipls += 1
        m = self.mipls_pos.pop(-1)[0]
        m.remove(self.player_sprites)

    def add_ochki(self, tile, result, game):
        if tile == "g" and game == 1:
            result = result * 2
            self.ochki += result
        elif tile == "d":
            self.ochki += result
        elif tile == "g" and game == 2:
            self.ochki += result
        elif tile == "m":
            self.ochki += result
        print("Игрок {}, получил {} очков за {}".format(self.name, result, tile))

    def sbros(self):
        Igrok.names = "1234567"

if __name__ == "__main__":
    print("Вы запустили этот модуль напрямую (а не импортировали его).")
    input("\n\nНажмите Enther для выхода.")