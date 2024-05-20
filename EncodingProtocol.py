from random import randint

KEYWORD = "AMIT"

with open("LettersToNumbers.txt", "r") as file:
    readfile = file.read()
    NUMBEROFCODES = len(readfile.split("\n"))


def getRandomKey():
    finalList = []
    randomint = randint(100000000000000000000000, 10000000000000000000000000000000000)
    for i in str(randomint):
        finalList.append(__getLetterFromNumber(int(i)))
    return ''.join(finalList)


def setKeyword(keyword: str):
    global KEYWORD
    KEYWORD = keyword.upper()


def __getLTN():
    file = open("LettersToNumbers.txt", 'r')
    transform = file.read()
    list_LTN = transform.split("\n")
    list_LTN[0] = " "
    return list_LTN


def __getNumberFromLetter(letter):
    LTNlist = __getLTN()
    for i in range(len(LTNlist)):
        if LTNlist[i] == letter:
            return i
    return -1


def __getLetterFromNumber(number):
    LTNlist = __getLTN()
    for i in range(len(LTNlist)):
        if i == number:
            return LTNlist[i]
    return "--"


def encode(data: str, key = KEYWORD):
    data = data.upper()
    finalList = []
    count = 0
    for letter in data:
        if count >= len(key):
            count = 0
        addednumb = __getNumberFromLetter(key[count]) + __getNumberFromLetter(letter)
        if addednumb >= NUMBEROFCODES:
            addednumb = addednumb - NUMBEROFCODES
        finalList.append(__getLetterFromNumber(addednumb))
        count += 1
    return ''.join(finalList)


def decode(data: str, key = KEYWORD):
    finalList = []
    count = 0
    for letter in data:
        if count >= len(key):
            count = 0
        encodedNumb = __getNumberFromLetter(letter)
        KNumb = __getNumberFromLetter(key[count])
        trueNumb = encodedNumb - KNumb
        if trueNumb < 0:
            trueNumb = NUMBEROFCODES + trueNumb
        finalList.append(__getLetterFromNumber(trueNumb))
        count += 1
    return (''.join(finalList)).lower()



