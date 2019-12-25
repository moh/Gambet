from itertools import *
import random


class Numbers:
    # ## logic part
    def __init__(self):
        self.numbers = {str(x) for x in range(1, 10)}
        self.PCvalue, self.playerValue = [], []  # # these list contain a tuple (nb, boule ,strike)
        self.possibility_number = set()  # # set contain the possibility of number for pc
        self.pc_number = ""
        self.Player_name = "player"
        self.time = 0
        self.pc_number = self.generate_number()

    def generate_number(self):
        number = set()
        numbers = list(self.numbers)
        while len(number) != 4:
            nb = random.randrange(1, 10)
            number.add(str(nb))
        self.numbers = {str(x) for x in range(1, 10)}
        return str(''.join(number))

    # #part 1 : get the boule and strike of number entered bu user
    def get_boule_strike(self, number):  # # add number,boule,strike to playervalue
        counter_b = 0
        counter_s = 0
        for nb in number:
            if nb in self.pc_number:
                counter_b += 1
        for nb in range(4):
            if number[nb] == self.pc_number[nb]:
                counter_s += 1
        counter_b -= counter_s
        self.playerValue.append((number, counter_b, counter_s))
        return [counter_b, counter_s]

    # ## part 2 : guess number of player
    def get_poss(self, number, boule):
        boule = int(boule)
        number = set(str(number))
        final_poss, final_poss2 = set(), []
        pro_number = ''.join(self.numbers - number)
        poss1, poss2 = list(combinations(number, boule)), list(combinations(pro_number, 4 - boule))
        for x in poss1:
            for y in poss2:
                final_poss.add(''.join(list(x) + list(y)))
        for x in final_poss:
            final_poss2.extend([''.join(y) for y in (list(permutations(x, 4)))])
        if self.possibility_number == set():
            return set(final_poss2)
        else:
            return set(final_poss2) & self.possibility_number  # #return the entersection of the last present possibility

    def get_strike(self, number1, number2):
        counter_s = 0
        for x in range(4):
            if number1[x] == number2[x]:
                counter_s += 1
        return counter_s

    def get_advanced_poss(self, number, list1):
        new_poss = set()
        for y in list1:
            temporary_poss = set()
            for x in self.possibility_number:
                if self.get_strike(y[0], x) == int(y[2]):
                    temporary_poss.add(x)
            if new_poss == set():
                new_poss = temporary_poss
            else:
                new_poss = new_poss & temporary_poss
        return new_poss

    def get_random(self, list1):
        list1 = list(list1)
        length = len(list1)
        return list1[random.randrange(0, length)]
        # ##end of logic part

    def get_number(self, nb_guess=0, boule=0, strike=0):
        if self.time == 0:
            self.time += 1
            return self.generate_number()
        self.PCvalue.append((nb_guess, str(boule), str(strike)))
        self.possibility_number = (self.get_poss(nb_guess, boule + strike))
        self.possibility_number = self.get_advanced_poss(nb_guess, self.PCvalue)
        if len(self.possibility_number)==0:
            return False
        nb = self.get_random(self.possibility_number)
        return nb
