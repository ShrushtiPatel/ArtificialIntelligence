import collections
from copy import deepcopy
from collections import Counter
import string
from random import *

class Literals():
    def __init__(self, a, b, flag):
        self.a = a
        self.b = b
        self.c = flag
    def generateLiterals(literal):
        temp = ""
        if (not(literal.c)):
            temp = "~"
        temp = temp + "X" + str(literal.a) + str(literal.b)
        return temp

def printResult(result):
    f = file("output.txt", "a")
    f.truncate()
    if(not(result)):
        f.write("no")
    else:
        f.write("yes")
        final = [0 for x in range(guests)]
        for value in values:
            if(True == values[value]):
                tmpLst = value.split("_")
                final[int(tmpLst[0])-1] = tmpLst[1]
        for t in range(len(final)):
            f.write("\n" + str(int(t)+1) + " " + str(final[t]))

def isModelSatisfied(clauses, values):
    temp = True
    atleastOneElement = False
    for clause in clauses:
        for cls in clause:
            if (str(cls.a)+"_"+str(cls.b) in values):
                if (values[str(cls.a) + "_" + str(cls.b)] != cls.c and 1 == len(clause)):
                    return False

    for clause in clauses:
        temp1 = False
        count = False
        for i in clause:
            atleastOneElement = True
            if(str(i.a)+"_"+str(i.b) in values):
                if(values[str(i.a)+"_"+str(i.b)] == i.c):
                    temp1 = temp1 or True
                count = True
        if(count):
            temp = temp and temp1
        elif(not(atleastOneElement)):
            return False
        else:
            return ""
    return temp

def findUnitClause(clauses):
    for clause in clauses:
        if (1 == len(clause)):
            return clause[0]
    return False

def findPureSymbol(clauses):
    testSymbol = set()
    for clause in clauses:
        for cls in clause:
            testSymbol.add(str(cls.a)+str(cls.b)+str(cls.c))
    for clause in clauses:
        for cls in clause:
            if (str(cls.a)+str(cls.b)+str(not(cls.c)) not in testSymbol):
                return cls
    return False

def simplify(clauses, literal):
    tempClauses = deepcopy(clauses)
    keys = []
    for i, clause in enumerate(clauses):
        count = False
        tmpList = []
        for cls in clause:
            if(str(cls.a) == str(literal.a) and str(cls.b) == str(literal.b) and cls.c == literal.c):
                keys.append(clause)
                count = True
                break
            elif(str(cls.a) == str(literal.a) and str(cls.b) == str(literal.b) and cls.c != literal.c):
                continue
            tmpList.append(cls)
        if(not(count) and 0 != len(tmpList)):
            clauses[i] = tmpList
    for key in keys:
        clauses.remove(key)
    return clauses

def DPLL(clauses, symbols, values):
    result = isModelSatisfied(clauses, values)
    if(True == result):
        return True
    elif(False == result):
        return False
    else:
        pureSymbol = findPureSymbol(clauses)
        if(False != pureSymbol):
            tmp = str(pureSymbol.a)+"_"+str(pureSymbol.b)
            values[tmp] = pureSymbol.c
            symbols.remove(tmp)
            clauses = simplify(clauses, pureSymbol)
            return DPLL(clauses, symbols, values)
        unitClause = findUnitClause(clauses)
        if(False != unitClause):
            tmp = str(unitClause.a) +"_"+str(unitClause.b)
            if(tmp in symbols):
                symbols.remove(tmp)
            values[tmp] = unitClause.c
            clauses = simplify(clauses, unitClause)
            return DPLL(clauses, symbols, values)
        tmpSymbols = deepcopy(symbols)
        tmp = tmpSymbols.pop()
        tmpLst = tmp.split("_")
        values[tmp] = True
        tmpClauses = simplify(deepcopy(clauses), Literals(tmpLst[0], tmpLst[1], True))
        if(DPLL(tmpClauses, tmpSymbols, values)):
            clauses = tmpClauses
            symbols = tmpSymbols
            return True
        else:
            symbols.remove(tmp)
            values[tmp] = False
            clauses = simplify(clauses, Literals(tmpLst[0], tmpLst[1], False))
            return DPLL(clauses, symbols, values)

def createFriendsClause():
    global clauses, clauseCounter
    friendClause = []
    friendClause1 = []
    if(tables >1):
        for i in friends:
            for j in range(tables):
                friendClause = []
                friendClause1 = []
                literal1 = Literals(i[0], j+1, True)
                literal2 = Literals(i[1], j+1, False)
                symbols.add(str(i[0])+"_"+str(j+1))
                symbols.add("~"+str(i[1])+"_"+str(j+1))
                friendClause.append(literal1)
                friendClause.append(literal2)
                literal1 = Literals(i[0], j+1, False)
                literal2 = Literals(i[1], j+1, True)
                symbols.add("~"+str(i[0])+"_"+str(j+1))
                symbols.add(str(i[1])+"_"+str(j+1))
                friendClause1.append(literal1)
                friendClause1.append(literal2)
                clauseCounter = clauseCounter+1
                clauses.append((deepcopy(friendClause)))
                clauseCounter = clauseCounter+1
                clauses.append((deepcopy(friendClause1)))
    return True

def createEnemiesClause():
    global clauses, clauseCounter
    for i in enemies:
        for j in range(tables):
            enemyClause = set()
            literal1 = Literals(i[0], j+1, False)
            literal2 = Literals(i[1], j+1, False)
            symbols.add("~"+str(i[0])+"_"+str(j+1))
            symbols.add("~"+str(i[1])+"_"+str(j+1))
            enemyClause.add(literal1)
            enemyClause.add(literal2)
            clauseCounter = clauseCounter+1
            clauses.append(deepcopy(enemyClause))
    return True

def createClausesForTables():
    global clauses, clauseCounter
    atLeastOneTable = []
    atMaxOneTable = []
    for i in range(guests):
        del atLeastOneTable [:]
        del atMaxOneTable [:]
        for j in range(tables):
            literal1 = Literals(i+1, j+1, True)
            atLeastOneTable.append(literal1)
            symbols.add(str(i+1)+"_"+str(j+1))
        clauseCounter = clauseCounter + 1
        clauses.append(deepcopy(atLeastOneTable))
        for j in range(tables):
            for k in range(j+1, tables):
                del atMaxOneTable [:]
                literal1 = Literals(i+1, j+1, False)
                literal2 = Literals(i+1, k+1, False)
                symbols.add("~"+str(i+1)+"_"+str(j+1))
                symbols.add("~"+str(i+1)+"_"+str(k+1))
                atMaxOneTable.append(literal1)
                atMaxOneTable.append(literal2)
                clauseCounter = clauseCounter+1
                clauses.append(deepcopy(atMaxOneTable))
    return True

def printCNF(clauses):
    finalClauses = []
    count = 0
    for clause in clauses:
        firstRecord = True
        temp = ""
        temp1= ""
        test = True
        counter =1
        for i in clause:
            if(firstRecord):
                temp = str(i)
                firstRecord = False
                temp1 = Literals.generateLiterals(i)
                count = count + 1
            else:
                temp = temp + " V " + str(i)
                temp1 = temp1 + "V" +Literals.generateLiterals(i)
                test = False
                counter = counter+1
                #print(count)
        print(count,temp1, counter)
            #finalClauses.append(temp)
    return finalClauses

def createKnowledgeBase (guestsRelation):
    for i in range (guests):
        for j in range(guests):
            if (str(guestsRelation[i][j]).upper() == "F"):
                friends.append((i+1, j+1))
            if (str(guestsRelation[i][j]).upper() == "E"):
                enemies.append((i+1, j+1))

guests = 0
tables = 0
guestsRelation = []
f = open('input.txt',"r")
firstLine = True
for line in f:
    if firstLine:
        a = line.split(" ")
        guests = int(a[0])
        tables = int(a[1])
        firstLine = False
        guestsRelation = [["0" for x in range(guests)] for y in range(guests)]

    else:
            a = line.split(" ")
            guestsRelation[int(a[0])-1][int(a[1])-1] = a[2].split("\n")[0]
            #guestsRelation[int(a[1]) - 1][int(a[0]) - 1] = a[2].split("\n")[0]

PersonAtTable = []
finalGuestList = []
clauses = []
friends = []
enemies = []
clauseCounter = 0
falseClauses =[]
symbols = set()
isTautology = False
values = {}
kb = createKnowledgeBase(guestsRelation)
if(0 == len(enemies)):
    f = file("output.txt", "a")
    f.truncate()
    if(tables >0):
        final = [1 for x in range(guests)]
        f.write("yes")
        for t in range(len(final)):
            f.write("\n" + str(int(t) + 1) + " " + str(final[t]))
    else:
        f.write("no")
else:
    createFriendsClause()
    createEnemiesClause()
    createClausesForTables()
    unitSymbols = set()
    finalSymbols = set()
    for symbol in symbols:
        tmpLst = list(symbol)
        if ("~" == tmpLst[0]):
            tmpLst.remove(tmpLst[0])
        temp = ""
        for t in tmpLst:
            temp = temp + t
        finalSymbols.add(temp)
    result = DPLL(clauses, finalSymbols, values)
    printResult(result)