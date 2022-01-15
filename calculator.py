# needed for string split
import re
# test framework
import unittest

# DICT, covers german input
ONES = {'null': 0,
        'eins': 1,
        'zwei': 2,
        'drei': 3,
        'vier': 4,
        'fünf': 5,
        'sechs': 6,
        'sieben': 7,
        'acht': 8,
        'neun': 9,
        'zen': 10,
        'elf': 11,
        'zwoelf': 12,
        'zwanzig': 20,
        'dreißig': 30,
        'vierzig': 40,
        'fuenfzig': 50,
        'sechzig': 60,
        'siebzig': 70,
        'achzig': 80,
        'neunzig': 90,
        'hundert': 100,
        'tausend': 1000,
        'millionen': 1000000
        }


#  main transform function
#  the input string is store in a list
#  while the list contains string, split and transform this string
def transformString(componentenString):
    global numberList
    numberList = [componentenString]
    while hasString():
        transform()
        checkForUnd()

    return listToNumber()


#  check if the numberlist still has a string
#  check for every item in this list, if its trivial and can be convert into int, by ONES
#  if not, it can be transform into int
def hasString():
    found = False
    for listIndex in range(0, len(numberList)):
        # print("check item", numberList[listIndex])
        if not numberList[listIndex].isdecimal():
            # print("Item is String", numberList[listIndex])
            found = True
            for key in ONES.keys():
                # print("check key ", key)
                if numberList[listIndex] == key:
                    # print("")
                    numberList[listIndex] = str(ONES[key])

    if '' in numberList:
        numberList.remove('')

    print(numberList)
    return found


#  crete the list number
#  for every item in numberList, check if can split into smaller part
def transform():
    for index, item in enumerate(numberList):
        for value in reversed(ONES.keys()):
            tmpList = re.split("(" + value + ")", item)
            if 'zig' in tmpList:
                continue

            if len(tmpList) != 1:  # has found
                if '' in tmpList:
                    tmpList.remove('')

                numberList.pop(index)
                for j in range(0, len(tmpList)):
                    numberList.insert(index + j, tmpList[j])

                return
    return


def checkForUnd():
    if "und" in numberList:
        undIndex = numberList.index("und")
        #  ones, dec = numberList[undIndex - 1], numberList[undIndex + 1]
        numberList[undIndex - 1], numberList[undIndex + 1] = numberList[undIndex + 1], numberList[undIndex - 1]
        numberList.pop(undIndex)


#  convert the calculated list number in one int
def listToNumber():
    if '' in numberList:
        numberList.remove('')

    print("Diese liste wollen wir umwandeln:", numberList)
    if len(numberList) == 1:  # if list contains only one element return
        return int(numberList[0])

    count = 0
    listLen = len(numberList)
    index = 0

    while index < len(numberList):  # iterate over numberList

        if index == listLen - 1:  # last item in list, just add and return
            count += int(numberList[index])
            return count

        elif index == listLen - 2:  # second to last item
            if numberList[index + 1] in ['100', '1000', '1000000']:  # if item is factor, multiply by item[index + 1]
                count += int(numberList[index]) * int(numberList[index + 1])
                return count
            else:
                count += int(numberList[index]) + int(numberList[index + 1])  # else just add
                return count

        elif index < listLen - 2:
            if numberList[index + 1] == '100' and '1000' in numberList:  # factor is for 100k
                if index < numberList.index("1000"):
                    count += int(numberList[index]) * 100000
                    if numberList[index + 2] == "1000":
                        index += 2
                    else:
                        index += 1
            elif numberList[index + 2] in ['100', '1000', '1000000'] and numberList[index + 1] not in ['100', '1000',
                                                                                                       '1000000']:
                count += (int(numberList[index]) + int(numberList[index + 1])) * int(int(numberList[index + 2]))
                index += 2
            elif numberList[index + 1] in ['100', '1000', '1000000'] and numberList[index + 2] != '1000':
                count += int(numberList[index]) * int(numberList[index + 1])
                index += 1
        else:
            print("Error beim umwandeln", index, numberList)

        index += 1

    return count


#  Transform the input operator
def transformOperation(operationString):
    if operationString == "plus" or operationString == "+":
        return "+"
    elif operationString == "minus" or operationString == "-":
        return "-"
    elif operationString == "mal" or operationString == "*":
        return "*"
    elif operationString == "geteilt" or operationString == "/":
        return "/"
    else:
        return "Falscher input"


# ----------  TESTS ----------------------
#  Tests made with unittest

def forTest_calculation(inputString):
    componentListTest = inputString.split(" ")

    resultStringTest = ""
    for i in range(0, len(componentListTest)):
        if i % 2 == 1:  # must be an operator
            componentListTest[i] = transformOperation(componentListTest[i])

        elif not componentListTest[i].isdecimal():
            minusTest = False
            if componentListTest[i][0] == "-":
                minusTest = True
                componentListTest[i] = componentListTest[i][1:]
            componentListTest[i] = str(transformString(componentListTest[i]))  # transform userString into int

            if minusTest:
                componentListTest[i] = "-" + componentListTest[i]

        resultStringTest += componentListTest[i]

    return eval(resultStringTest)


class TestStringMethods(unittest.TestCase):

    def test_transform(self):
        self.assertEqual(transformString("dreimillionenvierhundertneuntausend"), 3409000)
        self.assertEqual(transformString("neunhundertviertausendzwoelf"), 904012)
        self.assertEqual(transformString("4hundert3tausend12"), 403012)
        self.assertEqual(transformString("12hundert"), 1200)
        self.assertEqual(transformString("zenhundertneun"), 1009)

    def test_transformOperation(self):
        self.assertEqual(transformOperation("plus"), "+")
        self.assertEqual(transformOperation("minus"), "-")
        self.assertEqual(transformOperation("mal"), "*")
        self.assertEqual(transformOperation("geteilt"), "/")

    def test_calculation(self):
        self.assertEqual(forTest_calculation("vierhundert mal sieben"), 2800)
        self.assertEqual(forTest_calculation("siebzig mal siebzig"), 4900)
        self.assertEqual(forTest_calculation("-einsmillioneneinshunderttausendvier - 1"), -1100005)
        self.assertEqual(forTest_calculation("4hundertvierzig geteilt 10"), 44)
        self.assertEqual(forTest_calculation("8hundert9 - 9"), 800)



# -------END  TESTS ----------------------

# Begin of "main"
print(" --- Willkommen im taschenrechner ---  \n")
print(" Wählen Sie einen Modus:  \n")
print(" 1: Automatische Tests ")
print(" 2: Berechnungen per Eingabe ")
print(" 3: Ausgeschriebene Zahl in einen Int umwandeln \n")
print(" Bitte beachten: Zahlen, wie 43 (Dreiundvierzig) sind als Vierzigdrei einzutragen ")
print(" Input wie 8hundert8 -> 808 sind auch möglich ")

calModus = input("Modus:")

if calModus == "1":
    unittest.main()

elif calModus == "2":
    while 1:
        calString = input("Geben Sie hier ihre berechnung ein:")
        componentList = calString.split(" ")

        resultString = ""
        for i in range(0, len(componentList)):
            if i % 2 == 1:  # must be an operator
                componentList[i] = transformOperation(componentList[i])

            elif not componentList[i].isdecimal():
                minus = False
                if componentList[i][0] == "-":
                    minus = True
                    componentList[i] = componentList[i][1:]
                    print(componentList[i])
                componentList[i] = str(transformString(componentList[i]))  # transform userString into int

                if minus:
                    componentList[i] = "(-" + componentList[i] + ")"

            resultString += componentList[i]

        print("Interpretierte Berechnung:", resultString)  # interpreted calculation
        code = compile(resultString, "<string>", "eval")
        print(eval(code))  # eval converts a cal. string into result ("2*2" = 4)

elif calModus == "3":
    while 1:
        testString = input("Geben Sie hier den Zahlenstring ein: ")
        print(transformString(testString))

else:
    print("Falsche Eingabe")
