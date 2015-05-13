#!/usr/bin/env python3
# 213 [Intermediate] The Lazy Typist
keyboard = ['qwertyuiop',
            'asdfghjkl ',
            '^zxcvbnm ^',
            '   #####  ', ]
hands = ['l', 'r']
handNames = {'l': 'left', 'r': 'right'}
handMask = ['llll  rrrr',
            'llll  rrrr',
            'llll  rrrr',
            'llll  rrrr', ]
moveLookup = {hand: {} for hand in hands}

for y, line in enumerate(keyboard):
    for x, char in enumerate(line):
        if char != ' ':
            for hand, lookup in moveLookup.items():
                if handMask[y][x] in (hand, ' '):
                    if char in lookup:
                        lookup[char].append((x, y))
                    else:
                        lookup[char] = [(x, y)]

def mapStringToActions(s):
    for char in s:
        if char == ' ':
            yield '#'
        elif char.isalpha():
            yield char
        else:
            raise ValueError()

def getMoves(hand, action):
    if action in moveLookup[hand]:
        for move in moveLookup[hand][action]:
            yield move

def changeHands(hand):
    return hands[(hands.index(hand)+1) % len(hands)]

def getAllMoves(actions):
    actions = list(actions)
    if actions:
        action = actions[0]
        for hand in hands:
            if action.isupper():
                for shiftMove in getMoves(hand, '^'):
                    for move in getMoves(changeHands(hand), action.lower()):
                        for restOfMoves in getAllMoves(actions[1:]):
                            yield [(hand, '^', shiftMove), (changeHands(hand), action.lower(), move)]+restOfMoves
            else:
                for move in getMoves(hand, action):
                    for restOfMoves in getAllMoves(actions[1:]):
                        yield [(hand, action, move)]+restOfMoves
    else:
        yield []

def getDisplayName(action):
    if action == '#':
        return 'Space'
    if action == '^':
        return 'Shift'
    return action.upper()


def calculateCostOfMoves(moves):
    handLocations = {hand: None for hand in hands}
    cost = 0
    for move in moves:
        if handLocations[move[0]]:
            thisCost = abs(move[2][0] - handLocations[move[0]][2][0])+abs(move[2][1] - handLocations[move[0]][2][1])
            cost += thisCost
        handLocations[move[0]] = move
    return cost

def printMoves(moves):
    handLocations = {hand: None for hand in hands}
    cost = 0
    for move in moves:
        if handLocations[move[0]] == move:
            print("{0}: Use {1} hand again".format(getDisplayName(move[1]), handNames[move[0]]))
        elif handLocations[move[0]]:
            thisCost = abs(move[2][0] - handLocations[move[0]][2][0])+abs(move[2][1] - handLocations[move[0]][2][1])
            print("{0}: Move {1} hand from {2} (effort: {3})".format(getDisplayName(move[1]), handNames[move[0]], getDisplayName(handLocations[move[0]][1]), thisCost))
            cost += thisCost
        else:
            print("{0}: Use {1} hand".format(getDisplayName(move[1]), handNames[move[0]]))
        handLocations[move[0]] = move
    print('-'*45)
    print("Total Effort: {}".format(cost))
    print()

def runLazyTypist(message):
    print('#'*45)
    print(message)
    print('-'*45)
    printMoves(min(getAllMoves(mapStringToActions(message)), key=calculateCostOfMoves))

def main():
    runLazyTypist('The quick brown Fox')
    runLazyTypist('hello world')
    runLazyTypist('qpalzm woskxn')
    runLazyTypist('Hello there DailyProgrammers')
    runLazyTypist('QPgizm QFpRKbi Qycn')

if __name__ == '__main__':
    main()