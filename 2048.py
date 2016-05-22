# coding=utf-8
__author__ = 'haoxiang'
import os
import sys
import random
import getch


class GameMatrix(object):
    """
    2048
    """
    def __init__(self, lines=4, columns=4, base_number=2):
        """
        Initialize game
        """
        self.lines = lines
        self.columns = columns
        self.base_number = base_number
        self.score = 0
        self.highest_score = 0
        self.key_map = {'w': 1, 's': 2, 'a': 3, 'd': 4}
        self.matrix = [[0 for j in range(self.columns)] for i in range(self.lines)]

    def display(self):
        """
        Display the game matrix and tips
        """
        os.system('clear')
        print '\nCurrent score:', self.score
        print '\nHighest score in history:', self.highest_score
        print
        split_str = '+' + '-' * (8 * self.columns - 1) + '+'
        print split_str
        for line in self.matrix:
            print ('|%5s\t' * len(line) % tuple([str(x) if x else ' ' for x in line]) + '|')
            print split_str
        print '\n[Game Help]\n'
        print '<W>Up <S>Down <A>Left <D>Right <R>Restart <Q>Quit\n'
        print '[Program Help]\n'
        print 'Usage: python 2048.py <lines> <columns> <basenumber>\n'

    def computeLine(self, line, reverse):
        """
        :param line: [0, 2, 2, 4]
        :param reverse: True or False
        :return: [0, 0, 4, 4] or [4, 4, 0, 0]
        :function: Changing a line by the movement of player and compute the score   
        """
        lineWithoutZero = [x for x in line if x]
        if reverse:
            lineWithoutZero.reverse()
        l = len(lineWithoutZero)
        result = list()
        i = 0
        while i < l:
            if i == l - 1:
                result.append(lineWithoutZero[i])
                break
            if lineWithoutZero[i] != lineWithoutZero[i+1]:
                result.append(lineWithoutZero[i])
                i += 1
            else:
                result.append(lineWithoutZero[i] * 2)
                self.score += lineWithoutZero[i] * 2
                i += 2
        if len(result) < len(line):
            for k in range(len(line) - len(result)):
                result.append(0)
        if reverse:
            result.reverse()
        return result

    def play(self, move):
        """
        :param move: (1, 2, 3, 4) means (up, down, left, right)
        :return: True or False
        :function: Changing game matrix by the movement of player, return if the movement is legal
        """
        legal = False
        if move in (1, 2):
            for j in range(self.columns):
                column = [self.matrix[i][j] for i in range(self.lines)]
                r = self.computeLine(column, move == 2)
                if column != r:
                    legal = True
                    for i in range(self.lines):
                        self.matrix[i][j] = r[i]
        elif move in (3, 4):
            for i in range(self.lines):
                line = [self.matrix[i][j] for j in range(self.columns)]
                r = self.computeLine(line, move == 4)
                if line != r:
                    legal = True
                    for j in range(self.columns):
                        self.matrix[i][j] = r[j]
        return legal

    def produceRandomNum(self):
        """
        Produce a random in the game matrix after the movement of player, return if succed
        """
        index_list = list()
        for i in range(self.lines):
            for j in range(self.columns):
                if self.matrix[i][j] == 0:
                    index_list.append((i, j))
        if len(index_list) == 0:
            return False
        else:
            x, y = index_list[random.randint(0, len(index_list) - 1)]
            self.matrix[x][y] = self.base_number if random.randint(1, 100) < 90 else self.base_number * 2
            return True

    def isOver(self):
        """
        Return if the game is over
        """
        for i in range(self.lines):
            for j in range(self.columns):
                if self.matrix[i][j] == 0:
                    return False
                if i + 1 < self.lines and self.matrix[i][j] == self.matrix[i+1][j]:
                    return False
                if j + 1 < self.columns and self.matrix[i][j] == self.matrix[i][j+1]:
                    return False
        return True

    def start(self):
        """
        Play game, loops of producing random number, displaying game matrix, tips, waiting for and computing the player's movement
        """
        self.produceRandomNum()
        while True:
            self.produceRandomNum()
            self.display()
            if self.isOver():
                print 'Game over!'
                if self.highest_score < self.score:
                    self.highest_score = self.score
            while True:
                key = getch.getch()
                if key == 'r':
                    self.restart()
                    break
                if key == 'q':
                    exit(0)
                if key in self.key_map and self.play(self.key_map[key]):
                    break

    def restart(self):
        """
        Restart the game
        """
        if self.highest_score < self.score:
            self.highest_score = self.score
        self.score = 0
        for i in range(self.lines):
            for j in range(self.columns):
                self.matrix[i][j] = 0
        self.produceRandomNum()


if __name__ == '__main__':
    """
    Main function
    """
    if len(sys.argv) > 1:
        if len(sys.argv) != 4:
            print 'Usage: python 2048.py <lines> <columns> <basenumber>'
            exit(1)
        else:
            game = GameMatrix(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))
    else:
        game = GameMatrix()

    game.start()
