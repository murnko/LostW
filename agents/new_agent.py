# Przykladowy agent do zadania 'zagubiony Wumpus'. Agent porusza sie wezykiem.

from numpy import array, roll
from action import Action
import sys
# nie zmieniac nazwy klasy


class Agent:
    # nie zmieniac naglowka konstruktora, tutaj agent dostaje wszystkie informacje o srodowisku
    def __init__(self, p, pj, pn, height, width, areaMap):

        self.times_moved = 0
        self.direction = Action.LEFT

        # w ten sposob mozna zapamietac zmienne obiektu
        self.p = p  # prawdodpodobienstwo zgodnosci woli i dzialania
        self.np = (1 - self.p) / 4  # prawd niezgodnosci woli i dzialania
        self.pj = pj  # prawd dobrego odczytu jamy
        self.pn = pn  # prawd falszywego odczytu jamy
        self.height = height  # rozmiar mapy A
        self.width = width  # rozmiar mapy B
        self.map = areaMap  # mapa wlasciwa
        self.belief = []
        self.horizontal_move = 0
        self.horizontal_done = 0
        # w tym przykladzie histogram wypelniany rownymi wartosciami
        sum_norm = self.height * self.width
        self.hist = []
        self.map_num = []
        self.hist_z = []
        self.exit = []
        for y in range(self.height):
            self.hist.append([])
            self.hist_z.append([])
            for x in range(self.width):
                self.hist[y].append(1.00/sum_norm)
                self.hist_z[y].append(1)

        # zamiana mapy na numeryczna z literalow
        for y in range(self.height):
            self.map_num.append([])
            for x in range(self.width):
                if self.map[y][x] == '.':
                    pole = 0
                elif self.map[y][x] == 'J':
                    pole = 1
                else:  # wyjscie
                    pole = 7
                    self.exit.append(y)
                    self.exit.append(x)
                self.map_num[y].append(pole)
        return

    # nie zmieniac naglowka metody, tutaj agent dokonuje obserwacji swiata
    # sensor przyjmuje wartosc True gdy agent ma uczucie stania w jamie
    def sense(self, sensor):
        if sensor:
            for y in range(self.height):
                for x in range(self.width):

                    if self.map_num[y][x] == 1:
                        self.hist_z[y][x] += 1
        else:
            for y in range(self.height):
                for x in range(self.width):
                    if self.map_num[y][x] == 0:
                        self.hist_z[y][x] += 1

        #  print self.hist_z
        #  print self.map_num

        pass

    # nie zmieniac naglowka metody, tutaj agent decyduje w ktora strone sie ruszyc,
    # funkcja MUSI zwrocic jedna z wartosci [Action.UP, Action.DOWN, Action.LEFT, Action.RIGHT]
    def move(self):
        # ustalenie polozenia od najwyzszego prawdopodobienstwa, pierwszego znalezionego
        max_prob = 0
        # self.hist_z[4][3] = 3
        for y in range(self.height):
            for x in range(self.width):
                if self.hist_z[y][x] > max_prob:
                    max_prob = self.hist_z[y][x]
                    self.belief = [y, x]
            #  awaryjny uniform tu bedzie


        #  print self.belief

        if self.horizontal_done:
            self.horizontal_move = 0
        else:
            self.horizontal_move = 1

        if self.belief[0] == self.exit[0]:
            self.horizontal_move = 1
        elif self.belief[1] == self.exit[1]:
            self.horizontal_move = 0

        if self.horizontal_move:
            self.horizontal_done = 1
            if abs(self.belief[1] - self.exit[1]) > self.width/2:
                if (self.belief[1] - self.exit[1]) > 0:
                    move = 'r'
                else:
                    move = 'l'
            else:
                if (self.belief[1] - self.exit[1]) > 0:
                    move = 'l'
                else:
                    move = 'r'
        else:
            self.horizontal_done = 0
            if abs(self.belief[0] - self.exit[0]) > self.height/2:
                if (self.belief[0] - self.exit[0]) > 0:
                    move = 'd'
                else:
                    move = 'u'
            else:
                if (self.belief[0] - self.exit[0]) > 0:
                    move = 'u'
                else:
                    move = 'd'
        #  print move
        #  musi nastapic przesuniecie histogramu
        #  print self.hist_z
        #  print self.hist_z
        if move == 'r':
            self.hist_z = roll(self.hist_z, 1, axis=1)
            return Action.RIGHT
        elif move == 'l':
            self.hist_z = roll(self.hist_z, -1, axis=1)
            return Action.LEFT
        elif move == 'u':
            self.hist_z = roll(self.hist_z, -1, axis=0)
            return Action.UP
        elif move == 'd':
            self.hist_z = roll(self.hist_z, 1, axis=0)
            return Action.DOWN

        sys.exit("czy histogram1?")

    # nie zmieniac naglowka metody, tutaj agent udostepnia swoj histogram (ten z filtru
    # histogramowego), musi to byc tablica (lista list, krotka krotek...) o wymarach takich jak
    # plansza, pobranie wartosci agent.histogram()[y][x] zwraca prawdopodobienstwo stania na polu
    # w wierszu y i kolumnie x

    def histogram(self):
        return self.hist
