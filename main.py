import requests
import os
import sys
import keyboard
import requests
import pygame

count = 0
dell = {'0.002': '0.0029', '0.007': '0.0125', '0.012': '0.0220', '0.022': '0.0690', '0.047': '0.09', '0.092': '0.17', '0.202': '0.34', '0.702': '1.34',
        '1.402': '2.59', '2.802': '5.4', '19.02': '23', '22.702': '35'}
dell2 = {'0.002': '0.0058', '0.007': '0.0250', '0.012': '0.0460', '0.022': '0.1380', '0.047': '0.18', '0.092': '0.34', '0.202': '0.68', '0.702': '2.68',
        '1.402': '5.18', '2.802': '10.8', '19.02': '46', '22.702': '70'}
slave = ['0.002', '0.007', '0.012', '0.022', '0.047', '0.092', '0.202', '0.702', '1.402', '2.802', '19.02', '22.702']
display = pygame.display.set_mode((600, 450))
delta = "0.002"
running = True
lon = "37.530887"
lat = "55.703118"


def up():
    global dell
    global lat
    if  float(dell[slave[count]]) + float(lat) < 85:
        lat = float(dell[slave[count]]) + float(lat)
    else:
        print('придел')


def down():
    global dell
    global lat


    if float(lat) - float(dell[slave[count]]) > -85:
        lat = float(lat) - float(dell[slave[count]])
    else:
        print('придел')


def right():
    global dell2
    global lon


    if float(dell2[slave[count]]) + float(lon) < 200:
        lon = float(dell2[slave[count]]) + float(lon)
    else:
        print('придел')


def left():
    global dell2
    global lon

    if float(lon) - float(dell2[slave[count]]) > -200:
        lon = float(lon) - float(dell2[slave[count]])
    else:
        print('придел')


def Hot_key():
    global slave
    global count
    global delta


    if count < 11:
        count += 1
        delta = slave[count]
    else:
        print('придел')



def Hot_key2():
    global slave
    global count
    global delta

    if count > 0:
        count -= 1
        delta = slave[count]
    else:
        print('придел')


keyboard.add_hotkey('PAGEUP', Hot_key)
keyboard.add_hotkey('PAGEDOWN', Hot_key2)
keyboard.add_hotkey('UP', up)
keyboard.add_hotkey('DOWN', down)
keyboard.add_hotkey('LEFT', left)
keyboard.add_hotkey('RIGHT', right)


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


    api_server = "http://static-maps.yandex.ru/1.x/"

    params = {
        "ll": ",".join([str(lon), str(lat)]),
        "spn": ",".join([str(delta), str(delta)]),
        "l": "map"
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
    pygame.display.update()



if __name__ == '__main__':
    while running:
        getImage()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                os.remove("map.png")

