import pygame
#Камера, для номрального отображения поля
class Camera(object):
    def __init__(self, camera_func, wigth, height):
        self.camera_func = camera_func
        self.state = pygame.Rect(0,0, wigth, height)
        self.full = 1
    def apply(self, target):
        return target.rect.move(self.state.topleft)
    def update(self, target):
        self.state = self.camera_func(self.state, target.rect, self.full)

def camera_func(camera, target_rect, full):
    if full == 1:
        infoObject = pygame.display.Info()
        size = width, height = (infoObject.current_w - 80-20, infoObject.current_h-80)
    else:
        width, height = (800, 600)
    l= -target_rect.x + width/2 -40
    t= -target_rect.y+  height/2 -40
    w, h = camera.width, camera.height
    l= min(0, l)
    l=max(-(camera.width-width),l)
    t=max(-(camera.height-height),t)
    t=min(0,t)
    return pygame.Rect(l,t,w,h)

if __name__ == "__main__":
    print("Вы запустили этот модуль напрямую (а не импортировали его).")
    input("\n\nНажмите Enther для выхода.")