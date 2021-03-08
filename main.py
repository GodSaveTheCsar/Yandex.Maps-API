import requests
import os
import sys
import keyboard
import requests
import pygame
import pygame.locals as pl

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
COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')
FONT = pygame.font.Font(None, 20)
delta = "0.002"
running = True
lon = "37.530887"
lat = "55.703118"
l = 'map'
pts = list()


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
    string_rendered = FONT.render(text, 1, pygame.Color('black'))
    intro_rect = string_rendered.get_rect()
    intro_rect.x = x
    intro_rect.y = y
    display.blit(string_rendered, intro_rect)


class TextInput:
    def __init__(
            self,
            initial_string="",
            font_family="",
            font_size=15,
            antialias=True,
            text_color=(0, 0, 0),
            cursor_color=(0, 0, 1),
            repeat_keys_initial_ms=400,
            repeat_keys_interval_ms=35,
            max_string_length=40,
            password=False):
        """
        :param initial_string: Initial text to be displayed
        :param font_family: name or list of names for font (see pygame.font.match_font for precise format)
        :param font_size:  Size of font in pixels
        :param antialias: Determines if antialias is applied to font (uses more processing power)
        :param text_color: Color of text (duh)
        :param cursor_color: Color of cursor
        :param repeat_keys_initial_ms: Time in ms before keys are repeated when held
        :param repeat_keys_interval_ms: Interval between key press repetition when held
        :param max_string_length: Allowed length of text
        """

        # Text related vars:
        self.antialias = antialias
        self.text_color = text_color
        self.font_size = font_size
        self.max_string_length = max_string_length
        self.password = password
        self.input_string = initial_string  # Inputted text

        if not os.path.isfile(font_family):
            font_family = pygame.font.match_font(font_family)

        self.font_object = pygame.font.Font(font_family, font_size)

        # Text-surface will be created during the first update call:
        self.surface = pygame.Surface((1, 1))
        self.surface.set_alpha(0)

        # Vars to make keydowns repeat after user pressed a key for some time:
        self.keyrepeat_counters = {}  # {event.key: (counter_int, event.unicode)} (look for "***")
        self.keyrepeat_intial_interval_ms = repeat_keys_initial_ms
        self.keyrepeat_interval_ms = repeat_keys_interval_ms

        # Things cursor:
        self.cursor_surface = pygame.Surface((int(self.font_size/20 + 1), self.font_size))
        self.cursor_surface.fill(cursor_color)
        self.cursor_position = len(initial_string)  # Inside text
        self.cursor_visible = True  # Switches every self.cursor_switch_ms ms
        self.cursor_switch_ms = 500  # /|\
        self.cursor_ms_counter = 0

        self.clock = pygame.time.Clock()

    def update(self, event):
        if event.type == pygame.KEYDOWN:
            self.cursor_visible = True  # So the user sees where he writes

            # If none exist, create counter for that key:
            if event.key not in self.keyrepeat_counters:
                if not event.key == pl.K_RETURN:  # Filters out return key, others can be added as necessary
                    self.keyrepeat_counters[event.key] = [0, event.unicode]

            if event.key == pl.K_BACKSPACE:
                self.input_string = (
                        self.input_string[:max(self.cursor_position - 1, 0)]
                        + self.input_string[self.cursor_position:]
                )

                # Subtract one from cursor_pos, but do not go below zero:
                self.cursor_position = max(self.cursor_position - 1, 0)
            elif event.key == pl.K_DELETE:
                self.input_string = (
                        self.input_string[:self.cursor_position]
                        + self.input_string[self.cursor_position + 1:]
                )

            elif event.key == pl.K_RETURN:
                return True

            elif event.key == pl.K_RIGHT:
                # Add one to cursor_pos, but do not exceed len(input_string)
                self.cursor_position = min(self.cursor_position + 1, len(self.input_string))

            elif event.key == pl.K_LEFT:
                # Subtract one from cursor_pos, but do not go below zero:
                self.cursor_position = max(self.cursor_position - 1, 0)

            elif event.key == pl.K_END:
                self.cursor_position = len(self.input_string)

            elif event.key == pl.K_HOME:
                self.cursor_position = 0

            elif len(self.input_string) < self.max_string_length or self.max_string_length == -1:
                # If no special key is pressed, add unicode of key to input_string
                self.input_string = (
                        self.input_string[:self.cursor_position]
                        + event.unicode
                        + self.input_string[self.cursor_position:]
                )
                self.cursor_position += len(event.unicode)  # Some are empty, e.g. K_UP

        elif event.type == pl.KEYUP:
            # *** Because KEYUP doesn't include event.unicode, this dict is stored in such a weird way
            if event.key in self.keyrepeat_counters:
                del self.keyrepeat_counters[event.key]

        # Update key counters:
        for key in self.keyrepeat_counters:
            self.keyrepeat_counters[key][0] += self.clock.get_time()  # Update clock

            # Generate new key events if enough time has passed:
            if self.keyrepeat_counters[key][0] >= self.keyrepeat_intial_interval_ms:
                self.keyrepeat_counters[key][0] = (
                        self.keyrepeat_intial_interval_ms
                        - self.keyrepeat_interval_ms
                )

                event_key, event_unicode = key, self.keyrepeat_counters[key][1]
                pygame.event.post(pygame.event.Event(pl.KEYDOWN, key=event_key, unicode=event_unicode))

        # Re-render text surface:
        string = self.input_string
        if self.password:
            string = "*"*len(self.input_string)
        self.surface = self.font_object.render(string, self.antialias, self.text_color)

        # Update self.cursor_visible
        self.cursor_ms_counter += self.clock.get_time()
        if self.cursor_ms_counter >= self.cursor_switch_ms:
            self.cursor_ms_counter %= self.cursor_switch_ms
            self.cursor_visible = not self.cursor_visible

        if self.cursor_visible:
            cursor_y_pos = self.font_object.size(self.input_string[:self.cursor_position])[0]
            # Without this, the cursor is invisible when self.cursor_position > 0:
            if self.cursor_position > 0:
                cursor_y_pos -= self.cursor_surface.get_width()
            self.surface.blit(self.cursor_surface, (cursor_y_pos, 0))

    def get_surface(self):
        return self.surface

    def get_text(self):
        return self.input_string

    def get_cursor_position(self):
        return self.cursor_position

    def set_text_color(self, color):
        self.text_color = color

    def set_cursor_color(self, color):
        self.cursor_surface.fill(color)

    def clear_text(self):
        self.input_string = ""
        self.cursor_position = 0



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
        global l, lon, lat
        if self.x <= pos[0] <= self.x + self.width:
            if self.y <= pos[1] <= self.y + self.height:
                if self.text == 'схема':
                    l = 'map'
                elif self.text == 'спутник':
                    l = 'sat'
                elif self.text == 'гибрид':
                    l = 'sat,skl'
                elif self.text == 'Искать':
                    try:
                        response = requests.get(f"http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode={textinput.input_string}&format=json")
                        json_response = response.json()
                        toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
                        toponym_address = toponym['Point']['pos']
                        lon = toponym_address.split()[0]
                        lat = toponym_address.split()[1]
                        pts.append(','.join(toponym_address.split()) + ',flag')
                    except Exception:
                        print('Упс...')



class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


if __name__ == '__main__':
    sat = Button(WIDTH//10, HEIGHT//10, 'спутник')
    skl = Button(WIDTH//10, HEIGHT//10, 'гибрид')
    map = Button(WIDTH//10, HEIGHT//10, 'схема')
    search = Button(WIDTH//10, HEIGHT//10, 'Искать')
    textinput = TextInput()
    display.fill((255, 255, 255))
    clock = pygame.time.Clock()
    api_server = "http://static-maps.yandex.ru/1.x/"
    in_search_field = False
    while running:
        params = {
            "ll": ",".join([str(lon), str(lat)]),
            "spn": ",".join([str(delta), str(delta)]),
            "l": l,
            "pt": '`'.join(pts)
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
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                os.remove("map.png")
            if event.type == pygame.MOUSEBUTTONDOWN:
                sat.check(event.pos)
                skl.check(event.pos)
                map.check(event.pos)
                search.check(event.pos)
                if 0 <= event.pos[0] <= 200:
                    if 0 <= event.pos[1] <= 25:
                        in_search_field = True
                else:
                    in_search_field = False
            if in_search_field:
                textinput.update(event)
        BackGround = Background('map.png', (0, 0))
        display.blit(BackGround.image, BackGround.rect)
        pygame.draw.rect(display, 'black', (0, 0, 200, 25), width=2)
        pygame.draw.rect(display, 'white', (2, 2, 195, 22))
        sat.draw(WIDTH - sat.width, 0)
        skl.draw(WIDTH - sat.width - skl.width, 0)
        map.draw(WIDTH - sat.width - 2*map.width, 0)
        search.draw(200, 0)
        display.blit(textinput.get_surface(), (10, 10))
        pygame.display.update()
        clock.tick(120)

