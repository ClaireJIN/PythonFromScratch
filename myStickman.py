from tkinter import *
import time
import random

class Game:
    def __init__(self):
        self.tk = Tk()
        self.tk.title('StickMan')
        self.canvas = Canvas(self.tk, width=500, height=500)
        self.canvas.pack()
        self.canvas.update()
        self.window_width = self.canvas.winfo_width()
        self.window_height = self.canvas.winfo_height()
        self.bg = PhotoImage(file='background.gif')
        for i in range(0, 5):
            for j in range(0, 5):
                self.canvas.create_image(i * 100, j * 100, anchor='nw', image=self.bg)
        self.sprites = []
        self.running = True

    def mainloop(self):
        if self.running:
            while 1:
                for sprite in self.sprites:
                    sprite.move()
                g.tk.update_idletasks()
                g.tk.update()
                time.sleep(0.1)


class Coord:
    def __init__(self, x1=0, y1=0, x2=0, y2=0):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

def within_x(co1, co2):
    if (co1.x1 > co2.x1 and co1.x1 < co2.x2) \
            or (co1.x2 > co2.x1 and co1.x2 < co2.x2) \
            or (co2.x1 > co1.x1 and co2.x1 < co1.x2) \
            or (co2.x2 > co1.x1 and co2.x2 < co1.x1):
        return True
    else:
        return False


def within_y(co1, co2):
    if (co1.y1 > co2.y1 and co1.y1 < co2.y2) \
            or (co1.y2 > co2.y1 and co1.y2 < co2.y2) \
            or (co2.y1 > co1.y1 and co2.y1 < co1.y2) \
            or (co2.y2 > co1.y1 and co2.y2 < co1.y1):
        return True
    else:
        return False


def collided_left(co1, co2):
    if within_y(co1, co2):
        if co1.x1 <= co2.x2 and co1.x1 >= co2.x1:
            return True
    return False


def collided_right(co1, co2):
    if within_y(co1, co2):
        if co1.x2 >= co2.x1 and co1.x2 <= co2.x2:
            return True
    return False


def collided_top(co1, co2):
    if within_x(co1, co2):
        if co1.y1 <= co2.y2 and co1.y1 >= co2.y1:
            return True
    return False


def collided_bottom(co1, co2, y=0):
    if within_x(co1, co2):
        y_calc = co1.y2 + y
        if y_calc >= co2.y1 and y_calc <= co2.y2:
            return True
    return False

class Sprite:
    def __init__(self, game):
        self.game = game
        self.coordinates = Coord()
        self.width = None
        self.height = None
        self.endgame = False

    def move(self):
        pass

class Platform(Sprite):
    def __init__(self, game, photo_image, x, y, width, height):
        Sprite.__init__(self, game)
        self.photo_image = photo_image
        self.image = game.canvas.create_image(x, y, image=self.photo_image, anchor='nw')
        self.coordinates = Coord(x, y, x + width, y + height)
        self.width = width
        self.height = height


class Figure(Sprite):
    def __init__(self, game):
        Sprite.__init__(self, game)
        self.left_figures = [
            PhotoImage(file='figure-L1.gif'),
            PhotoImage(file='figure-L2.gif'),
            PhotoImage(file='figure-L3.gif')
        ]

        self.right_figures = [
            PhotoImage(file='figure-R1.gif'),
            PhotoImage(file='figure-R2.gif'),
            PhotoImage(file='figure-R3.gif')
        ]

        self.image = self.game.canvas.create_image(480, 460, anchor='nw', image=self.left_figures[2])
        self.x_speed = -2
        self.y_speed = 0
        self.current_picture_num = -1
        self.current_image_add = 1
        self.game.canvas.bind_all('<KeyPress-Left>', self.turn_left)
        self.game.canvas.bind_all('<KeyPress-Right>', self.turn_right)
        self.game.canvas.bind_all('<space>', self.jump)
        self.jump_count = 0
        self.width = 27
        self.height = 30
        self.doorClosed = PhotoImage(file='door2.gif')

    def getCoords(self):
        x1 = self.game.canvas.coords(self.image)[0]
        y1 = self.game.canvas.coords(self.image)[1]
        x2 = x1 + 27
        y2 = y1 + 30

        self.coordinates = Coord(x1, y1, x2, y2)

    def animate(self):
        self.current_picture_num += self.current_image_add
        if self.current_picture_num == 2:
            self.current_image_add = -1
        if self.current_picture_num == 0:
            self.current_image_add = 1

        if self.y_speed == 0:
            if self.x_speed < 0:
                self.game.canvas.itemconfig(self.image, image=self.left_figures[self.current_picture_num])
            elif self.x_speed > 0:
                self.game.canvas.itemconfig(self.image, image=self.right_figures[self.current_picture_num])
        elif self.x_speed < 0:
            self.game.canvas.itemconfig(self.image, image=self.left_figures[2])
        elif self.x_speed > 0:
            self.game.canvas.itemconfig(self.image, image=self.right_figures[2])

    def turn_left(self, evt):
            self.x_speed = -3

    def turn_right(self, evt):
            self.x_speed = 3

    def jump(self, evt):
        if self.y_speed == 0:
            self.jump_count = 0
            self.y_speed = -4

    def move(self):
        self.animate()
        '''jump'''
        if self.y_speed < 0:
            self.jump_count += 1
            if self.jump_count > 20:
                self.y_speed = 4
        if self.y_speed > 0:
            self.jump_count -= 1

        left = True
        right = True
        top = True
        bottom = True
        falling = True

        '''collide the walls'''
        if self.game.canvas.coords(self.image)[0] < 0 and self.x_speed < 0:
            self.x_speed = 0
            left = False
        elif self.game.canvas.coords(self.image)[0] + self.width > self.game.window_width and self.x_speed > 0:
            self.x_speed = 0
            right = False
        if self.game.canvas.coords(self.image)[1] < 0 and self.y_speed < 0:
            self.y_speed = 0
            top = False
        elif self.game.canvas.coords(self.image)[1] + self.height > self.game.window_height and self.y_speed > 0:
            self.y_speed = 0
            bottom = False

        '''collide the platforms'''
        self.getCoords()
        co = self.coordinates
        for sprite in self.game.sprites:
            if sprite == self:
                continue
            sprite_co = sprite.coordinates
            if top and self.y_speed < 0 and collided_top(co, sprite_co):
                self.y_speed = -self.y_speed
                top = False

            if bottom and self.y_speed > 0 and collided_bottom(co, sprite_co, self.y_speed):
                self.y_speed = sprite_co.y1 - co.y2
                if self.y_speed < 0:
                    self.y_speed = 0
                bottom = False
                top = False

            '''the figure is at the bottom and it cannot fall down'''
            if bottom and falling and self.y_speed == 0 and co.y2 < self.game.window_height and collided_bottom(co,
                                                                                                          sprite_co, 1):
                falling = False

            if left and self.x_speed < 0 and collided_left(co, sprite_co):
                self.x_speed = 0
                left = False
                if sprite.endgame:
                    self.game.canvas.itemconfig(sprite.image, image=self.doorClosed)
                    self.game.running = False

            if right and self.x_speed > 0 and collided_right(co, sprite_co):
                self.x_speed = 0
                right = False
                if sprite.endgame:
                    self.game.canvas.itemconfig(sprite.image, image=self.doorClosed)
                    self.game.running = False

        '''the figure has not fallen down or been on the floor, it would fall down'''
        if falling and bottom and self.y_speed == 0 and co.y2 < self.game.window_height:
            self.y_speed = 4

            '''if collided_right(co, sprite_co):
                self.x_speed = 0
            elif collided_left(co, sprite_co):
                self.x_speed = 0
            if self.top and self.y_speed and collided_top(co, sprite_co):
                self.y_speed = -self.y_speed
                self.top = False 
            elif self.bottom and self.y_speed > 0 and collided_bottom(co, sprite_co):
                self.y_speed = 0
                self.bottom = False'''

        self.game.canvas.move(self.image, self.x_speed, self.y_speed)

class Door(Sprite):
    def __init__(self, game, photo_image, x, y, width, height):
        Sprite.__init__(self, game)
        self.photo_image = photo_image
        self.image = game.canvas.create_image(x, y, image=self.photo_image, anchor='nw')
        self.coordinates = Coord(x, y, x + (width / 2), y + height)
        self.endgame = True


g = Game()
platform1 = Platform(g, PhotoImage(file="platform1.gif"), 0, 480, 100, 10)
platform2 = Platform(g, PhotoImage(file="platform1.gif"), 150, 440, 100, 10)
platform3 = Platform(g, PhotoImage(file="platform1.gif"), 300, 400, 100, 10)
platform4 = Platform(g, PhotoImage(file="platform1.gif"), 300, 160, 100, 10)
platform5 = Platform(g, PhotoImage(file="platform2.gif"), 175, 350, 66, 10)
platform6 = Platform(g, PhotoImage(file="platform2.gif"), 50, 300, 66, 10)
platform7 = Platform(g, PhotoImage(file="platform2.gif"), 170, 120, 66, 10)
platform8 = Platform(g, PhotoImage(file="platform2.gif"), 45, 60, 66, 10)
platform9 = Platform(g, PhotoImage(file="platform3.gif"), 170, 250, 32, 10)
platform10 = Platform(g, PhotoImage(file="platform3.gif"), 230, 200, 32, 10)
g.sprites.append(platform1)
g.sprites.append(platform2)
g.sprites.append(platform3)
g.sprites.append(platform4)
g.sprites.append(platform5)
g.sprites.append(platform6)
g.sprites.append(platform7)
g.sprites.append(platform8)
g.sprites.append(platform9)
g.sprites.append(platform10)

figure = Figure(g)
g.sprites.append(figure)

door = Door(g, PhotoImage(file="door1.gif"), 45, 30, 40, 35)
g.sprites.append(door)

g.mainloop()

























