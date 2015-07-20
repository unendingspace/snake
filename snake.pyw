# -*- coding: utf-8 -*-

from Tkinter import *
from PIL import Image, ImageTk
from random import randrange
from time import sleep

class Game():

    def __init__(self):
        self.master = Tk()
        self.master.resizable(height = False, width = False)
        self.window = GameWindow(self.master)
        self.snake = Snake(self.master)
        self.apple = Apple(self.master)

    def advance(self):
        self.snake.advance(self.apple.getX(), self.apple.getY())

        # list tail coordinates
        tail = []

        for item in self.snake.getTail():
            tail.append([item.getX(), item.getY()])

        # check apple
        if self.snake.getHead() == [self.apple.getX(), self.apple.getY()]:
            self.apple.teleport(tail)

        # check endgames
        over = False

        head = self.snake.getHead()
        if head in tail:
            over = True
        elif head[0] > 448 or head[0] < 0:
            over = True
        elif head[1] > 288 or head[1] < 0:
            over = True

        if over:
            sleep(1.5)
            self.endGame()
            return

        # draw
        self.draw()
        self.apple.draw()
        self.master.after(400, self.advance)

    def draw(self):
        self.snake.draw()

    def keyInput(self, event):

        if event.char == 'a':
            direction = 1
        elif event.char == 'd':
            direction = 0
        elif event.char == 'w':
            direction = 2
        elif event.char == 's':
            direction = 3
        current_direction = self.snake.getDirection()
        if not ((current_direction -1 <= 0 and direction -1 <= 0) or (current_direction - 1 > 0 and direction - 1 > 0)):
            self.snake.turn(direction)

    def endGame(self):
        GameOverScreen(self.master)

    def begin(self):
        self.frame = self.window.getFrame()
        self.frame.bind("<Key>", self.keyInput)
        self.frame.focus_set()
        self.advance()
        self.master.mainloop()


class GameWindow():

    def __init__(self, master):
        self.master = master
        self.master.title('Snake!')
        self.frame = Frame(self.master, width = 480, height = 320, bg = 'black')
        self.frame.pack()

    def getFrame(self):
        return self.frame


class Snake():

    def __init__(self, master):
        self.master = master
        self.head = SnakeHead(self.master)
        self.facing = 0 # 0 = right, 1 = left, 2 = up, 3 = down
        self.tail = []

    def advance(self, apple_x, apple_y):

        old_x = self.head.getX()
        old_y = self.head.getY()

        # head
        if self.facing == 0:
            self.head.changeX(32)
        elif self.facing == 1:
            self.head.changeX(-32)
        elif self.facing == 2:
            self.head.changeY(-32)
        elif self.facing == 3:
            self.head.changeY(32)

        # lengthen tail if neccessary
        if self.head.getX() == apple_x and self.head.getY() == apple_y:
            if self.tail == []:
                self.addTail(old_x, old_y)
            else:
                self.addTail(self.tail[-1].getX(), self.tail[-1].getY())

        # tail
        if len(self.tail) != 0:
            tail_x = self.tail[0].getX()
            tail_y = self.tail[0].getY()

            self.tail[0].changeX(old_x)
            self.tail[0].changeY(old_y)

            for item in self.tail[1:-1]:
                temp = [item.getX(), item.getY()]
                item.changeX(tail_x)
                item.changeY(tail_y)
                tail_x = temp[0]
                tail_y = temp[1]

            if len(self.tail) > 1:
                self.tail[-1].changeX(tail_x)
                self.tail[-1].changeY(tail_y)


    def draw(self):
        self.head.draw()

        for item in self.tail:
            item.draw()

    def turn(self, direction):
        self.facing = direction

    def getDirection(self):
        return self.facing

    def addTail(self, x_coord, y_coord):
        self.tail += [SnakeTail(self.master, x_coord, y_coord)]

    def getTail(self):
        return self.tail

    def getHead(self):
        return [self.head.getX(), self.head.getY()]

class SnakeHead():

    def __init__(self, master):
        self.x = 0
        self.y = 0
        self.master = master
        self.image = Image.open('head.png')
        self.prepared_image = ImageTk.PhotoImage(self.image)
        self.widget = Label(self.master, image = self.prepared_image, bg = 'black')
        self.widget.image = self.prepared_image

    def changeX(self, change):
        self.x += change

    def changeY(self, change):
        self.y += change

    def draw(self):
        self.widget.place(x = self.x, y = self.y)

    def getX(self):
        return self.x

    def getY(self):
        return self.y

class SnakeTail():

    def __init__(self, master, x_coord, y_coord):
        self.master = master
        self.x = x_coord
        self.y = y_coord
        self.image = Image.open('tail.png')
        self.prepared_image = ImageTk.PhotoImage(self.image)
        self.widget = Label(self.master, bg = 'black', image = self.prepared_image)
        self.widget.image = self.prepared_image

    def draw(self):
        self.widget.place(x = self.x, y = self.y)

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def changeY(self, change):
        self.y = change

    def changeX(self, change):
        self.x = change


class Apple():

    def __init__(self, master):
        self.master = master
        self.image = Image.open('apple.png')
        self.prepared_image = ImageTk.PhotoImage(self.image)
        self.widget = Label(self.master, bg = 'black', image = self.prepared_image)
        self.widget.image = self.prepared_image
        self.x = 32 * randrange(0, 15)
        self.y = 32 * randrange(0, 10)

    def draw(self):
        self.widget.place(x = self.x, y = self.y)

    def teleport(self, tail):
        invalid_targets = [[self.x, self.y]] + tail
        self.x, self.y = self.generateNewLocation(invalid_targets)

    def generateNewLocation(self, invalid_targets):
        new_coords = [32 * randrange(0, 15), 32 * randrange(0, 10)]
        if new_coords in invalid_targets:
            new_coords = self.generateNewLocation(invalid_targets)
        return new_coords[0], new_coords[1]

    def getX(self):
        return self.x

    def getY(self):
        return self.y


class GameOverScreen():

    def __init__(self, master):
        self.master = master

        self.image = Image.open('gameover.png')
        self.prepared_image = ImageTk.PhotoImage(self.image)
        self.widget = Label(self.master, bd = 0, image = self.prepared_image)
        self.widget.image = self.prepared_image

        self.widget.place(x = 0, y = 0)


jimmy = Game()
jimmy.begin()