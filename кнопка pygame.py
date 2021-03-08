class Button:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.inactive_color = (41, 150, 150)
        self.active_color = (9, 190, 150)

    def draw(self, x, y, text, action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x < mouse[0] < x + self.width:
            if y < mouse[1] < y + self.height:
                pygame.draw.rect(display, self.inactive_color, (x, y, self.width, self.height))
                if click[0] == 1:
                    pygame.mixer.Sound.play(button_sound)
                    pygame.time.delay(150)
                    if action != None:
                        action()
            else:
                pygame.draw.rect(display, self.active_color, (x, y, self.width, self.height))

        else:
            pygame.draw.rect(display, self.active_color, (x, y, self.width, self.height))

        print_text(text, x + 5, y + 5)
#сам класс кнопки
button = Button(80, 40)
# создаешь класс кнопки перед циклом
button.draw(10, 100, 'Назад в меню', m)
# это отрисовка в цикле(m-это функиция которую ты вставляешь в кнопку, то есть пишешь имя функции вместо m)
