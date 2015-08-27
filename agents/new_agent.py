# Przykladowy agent do zadania 'zagubiony Wumpus'. Agent porusza sie wezykiem.

from random import randint
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
        self.np = (1 - p) / 4  # prawd niezgodnosci woli i dzialania
        self.pj = pj  # prawd dobrego odczytu jamy
        self.pn = pn  # prawd falszywego odczytu jamy
        self.height = height  # rozmiar mapy A
        self.width = width  # rozmiar mapy B
        self.map = areaMap  # mapa wlasciwa

        # w tym przykladzie histogram wypelniany rownymi wartosciami

        sum_norm = self.height * self.width
        print sum_norm
        self.hist = []

        for y in range(self.height):
            self.hist.append([])
            for x in range(self.width):
                self.hist[y].append(1.00/sum_norm)
        print self.hist
        sys.exit("czy histogram?")
        # dopisac reszte inicjalizacji agenta
        return

    # nie zmieniac naglowka metody, tutaj agent dokonuje obserwacji swiata
    # sensor przyjmuje wartosc True gdy agent ma uczucie stania w jamie
    def sense(self, sensor):
        if sensor:
            pass

    # nie zmieniac naglowka metody, tutaj agent decyduje w ktora strone sie ruszyc,
    # funkcja MUSI zwrocic jedna z wartosci [Action.UP, Action.DOWN, Action.LEFT, Action.RIGHT]
    def move(self):
        if self.times_moved < self.width - 1:
            self.times_moved += 1
            return self.direction
        else:
            self.times_moved = 0
            self.direction = Action.RIGHT if self.direction == Action.LEFT else Action.LEFT
            return Action.DOWN

    # nie zmieniac naglowka metody, tutaj agent udostepnia swoj histogram (ten z filtru
    # histogramowego), musi to byc tablica (lista list, krotka krotek...) o wymarach takich jak
    # plansza, pobranie wartosci agent.histogram()[y][x] zwraca prawdopodobienstwo stania na polu
    # w wierszu y i kolumnie x
    def histogram(self):
        return self.hist
