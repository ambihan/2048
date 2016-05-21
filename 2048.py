# coding=utf-8
__author__ = 'haoxiang'
import os
import sys
import random
import getch

# global values
LINES = 4
COLUMNS = 4
SCORE = 0
RANDNUM = [2, 4]
KEYMAP = {'w': 1, 's': 2, 'a': 3, 'd': 4}


def displayMatrix(matrix):
    """
    :param matrix: Game Matrix
    :return: None
    :function: display the game matrix
    """
    os.system('clear')
    print '\nCurrent Score:', SCORE
    print
    sp = '+' + '-' * (8 * COLUMNS - 1) + '+'
    print sp
    for line in matrix:
        print ('|%5s\t' * len(line) % tuple([str(x) if x else ' ' for x in line]) + '|')
        print sp


def displayTips():
    """
    :param: None
    :return: None
    :function: display the game tips and score
    """
    print '\n[Game Help]\n'
    print '<W>Up <S>Down <A>Left <D>Right <R>Restart <Q>Quit\n'
    print '[Program Help]\n'
    print 'Usage: python 2048.py <lines> <columns> <basenumber>\n'


def computeLine(line, reverse):
    """
    :param line: [0, 2, 2, 4]
    :param reverse: True or False
    :return: [0, 0, 4, 4] or [4, 4, 0, 0]
    :function: Changing a line by the movement of player    
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
            global SCORE
            result.append(lineWithoutZero[i] * 2)
            SCORE += lineWithoutZero[i] * 2
            i += 2
    if len(result) < len(line):
        for k in range(len(line) - len(result)):
            result.append(0)
    if reverse:
        result.reverse()
    return result


def computeMatrix(matrix, move):
    """
    :param matrix: Game Matrix
    :param move: (1, 2, 3, 4) means (up, down, left, right)
    :return: True or False
    :function: Changing game matrix by the movement of player, return if the movement is legal
    """
    legal = False
    if move in (1, 2):
        for j in range(COLUMNS):
            column = [matrix[i][j] for i in range(LINES)]
            r = computeLine(column, move == 2)
            if column != r:
                legal = True
                for i in range(LINES):
                    matrix[i][j] = r[i]
    elif move in (3, 4):
        for i in range(LINES):
            line = [matrix[i][j] for j in range(COLUMNS)]
            r = computeLine(line, move == 4)
            if line != r:
                legal = True
                for j in range(COLUMNS):
                    matrix[i][j] = r[j]
    return legal


def produceRandomNum(matrix):
    """
    :param matrix: Game Matrix
    :return: True or False
    :function: Produce a random in the game matrix after the movement of player, return if game is not over
    """
    indexList = list()
    for i in range(LINES):
        for j in range(COLUMNS):
            if matrix[i][j] == 0:
                indexList.append((i, j))
    if len(indexList) == 0:
        return False
    else:
        x, y = indexList[random.randint(0, len(indexList) - 1)]
        matrix[x][y] = RANDNUM[random.randint(0, 1)]
        return True


def gameIsOver(matrix):
    """
    :param matrix: Game Matrix
    :return: True or False
    :function: return if the game is over
    """
    for i in range(LINES):
        for j in range(COLUMNS):
            if matrix[i][j] == 0:
                return False
            if i + 1 < LINES and matrix[i][j] == matrix[i+1][j]:
                return False
            if j + 1 < COLUMNS and matrix[i][j] == matrix[i][j+1]:
                return False
    return True


def run(matrix):
    """
    :param matrix: Game Matrix
    :return: None
    :function: Play game, loops of producing random number, displaying game matrix, tips, waiting for and computing the player's movement
    """
    while True:
        produceRandomNum(matrix)
        displayMatrix(matrix)
        displayTips()
        if gameIsOver(matrix):
            print '\nGame over!\n'
            break
        while True:
            key = getch.getch()
            if key == 'r':
                init(matrix)
                break
            if key == 'q':
                exit(0)
            if key in KEYMAP and computeMatrix(matrix, KEYMAP[key]):
                break

def init(matrix):
    """
    :param matrix: Game Matrix
    :return: None
    :function: Init game matrix
    """
    for i in range(LINES):
        for j in range(COLUMNS):
            matrix[i][j] = 0
    produceRandomNum(matrix)


if __name__ == '__main__':

    if len(sys.argv) > 1:
        if len(sys.argv) != 4:
            print 'Usage: python 2048.py <lines> <columns> <basenumber>'
        else:
            LINES = int(sys.argv[1])
            COLUMNS = int(sys.argv[2])
            RANDNUM = [int(sys.argv[3]), int(sys.argv[3]) * 2]

    matrix = list()
    for i in range(LINES):
        column = list()
        for j in range(COLUMNS):
            column.append(0)
        matrix.append(column)
    produceRandomNum(matrix)
    run(matrix)

    
