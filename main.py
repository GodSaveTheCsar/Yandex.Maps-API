import requests
import os
import sys
import keyboard
import requests
import pygame

pygame.init()

count = 0
dell = {'0.002': '0.0029', '0.007': '0.0125', '0.012': '0.0220', '0.022': '0.0690', '0.047': '0.09', '0.092': '0.17',
        '0.202': '0.34', '0.702': '1.34',
        '1.402': '2.59', '2.802': '5.4', '19.02': '23', '22.702': '35'}
dell2 = {'0.002': '0.0058', '0.007': '0.0250', '0.012': '0.0460', '0.022': '0.1380', '0.047': '0.18', '0.092': '0.34',
         '0.202': '0.68', '0.702': '2.68',
         '1.402': '5.18', '2.802': '10.8', '19.02': '46', '22.702': '70'}
slave = ['0.002', '0.007', '0.012', '0.022', '0.047', '0.092', '0.202', '0.702', '1.402', '2.802', '19.02', '22.702']
WIDTH, HEIGHT = 600, 450
display = pygame.display.set_mode((WIDTH, HEIGHT))
delta = "0.002"
running = True
lon = "37.530887"
lat = "55.703118"
l = 'map'


def up():
    global dell
    global lat
    if float(dell[slave[count]]) + float(lat) < 85:
        lat = float(dell[slave[count]]) + float(lat)
    else:
        print('предел')


def down():
    global dell
    global lat

    if float(lat) - float(dell[slave[count]]) > -85:
        lat = float(lat) - float(dell[slave[count]])
    else:
        print('предел')


def right():
    global dell2
    global lon

    if float(dell2[slave[count]]) + float(lon) < 200:
        lon = float(dell2[slave[count]]) + float(lon)
    else:
        print('предел')


def left():
    global dell2
    global lon

    if float(lon) - float(dell2[slave[count]]) > -200:
        lon = float(lon) - float(dell2[slave[count]])
    else:
        print('предел')


def Hot_key():
    global slave
    global count
    global delta

    if count < 11:
        count += 1
        delta = slave[count]
    else:
        print('предел')


def Hot_key2():
    global slave
    global count
    global delta

    if count > 0:
        count -= 1
        delta = slave[count]
    else:
        print('предел')


keyboard.add_hotkey('PAGEUP', Hot_key)
keyboard.add_hotkey('PAGEDOWN', Hot_key2)
keyboard.add_hotkey('UP', up)
keyboard.add_hotkey('DOWN', down)
keyboard.add_hotkey('LEFT', left)
keyboard.add_hotkey('RIGHT', right)


def print_text(text, x, y):
    font = pygame.font.Font(None, 20)
    string_rendered = font.render(text, 1, pygame.Color('black'))
    intro_rect = string_rendered.get_rect()
    intro_rect.x = x
    intro_rect.y = y
    display.blit(string_rendered, intro_rect)


class Button:
    def __init__(self, width, height, text):
        self.width = width
        self.height = height
        self.text = text
        self.inactive_color = (41, 150, 150)
        self.active_color = (9, 190, 150)

    def draw(self, x, y):
        self.x = x
        self.y = y
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x < mouse[0] < x + self.width:
            if y < mouse[1] < y + self.height:
                pygame.draw.rect(display, self.inactive_color, (x, y, self.width, self.height))
                if click[0] == 1:
                    pygame.time.delay(150)
            else:
                pygame.draw.rect(display, self.active_color, (x, y, self.width, self.height))

        else:
            pygame.draw.rect(display, self.active_color, (x, y, self.width, self.height))
        print_text(self.text, x, y + self.height//2)

    def check(self, pos):
        global l
        if (self.x, self.y) <= pos <= (self.x + self.width, self.y + self.height):
            if self.text == 'схема':
                l = 'map'
            elif self.text == 'спутник':
                l = 'sat'
            else:
                l = 'sat,skl'


class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


def getImage():
    display.fill((255, 255, 255))
    global delta
    global lon
    global lat
    global button
    clock = pygame.time.Clock()
    api_server = "http://static-maps.yandex.ru/1.x/"

    params = {
        "ll": ",".join([str(lon), str(lat)]),
        "spn": ",".join([str(delta), str(delta)]),
        "l": l
    }
    response = requests.get(api_server, params=params)

    if not response:
        print("Ошибка выполнения запроса:")
        print(api_server, params)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)

    # Запишем полученное изображение в файл.
    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)

    BackGround = Background('map.png', (0, 0))
    display.blit(BackGround.image, BackGround.rect)
    sat.draw(WIDTH - sat.width, 0)
    skl.draw(WIDTH - sat.width - skl.width, 0)
    map.draw(WIDTH - sat.width - 2*map.width, 0)
    pygame.display.update()
    clock.tick(60)


if __name__ == '__main__':
    sat = Button(WIDTH//10, HEIGHT//10, 'спутник')
    skl = Button(WIDTH//10, HEIGHT//10, 'гибрид')
    map = Button(WIDTH//10, HEIGHT//10, 'схема')
    while running:
        getImage()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                os.remove("map.png")
            if event.type == pygame.MOUSEBUTTONDOWN:
                sat.check(event.pos)
                skl.check(event.pos)
                map.check(event.pos)
