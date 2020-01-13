import pathlib
from pathlib import Path

cwd = Path(__file__).parents[0]
print(f"{cwd}\n")

maoriAlphabet = ['a','e','h','i','k','m','n','g','o','p','r','t','u','w']
#kaore au i te mohio

def ReadTextFile(file):#Open the specified file and turn it into an array of lines
    f = open(str(cwd)+f'/FilesForQ3/{file}.txt', 'r', errors='ignore')
    if f.mode == 'r':
        string = f.read().splitlines()
    return string

def SplitString(string):#Split a string by spaces into array
    #This is forfilling Stage A, finding words in a line
    string = string.split(" ")
    return string

def ArrayToLower(array):#Convert entire arrays into lowercase
    for i in range(len(array)):
        array[i] = array[i].lower()
    return array

def CheckCommonMaori(string, commonMaori):
    """Take a string and check agaisnt common maori words
    after which, return a confidence factor"""
    successes = 0
    confidence = None
    items = len(string)
    for item in commonMaori:
        for word in string:
            if item == word:
                successes += 1

    #Could add more checks for the length of the array
    #If the array is longer then X, confidence should go up
    if successes >= (items/1.05):
        confidence = 95
    elif successes >= (items/1.15):
        confidence = 85
    elif successes >= (items/1.25):
        confidence = 75
    elif successes >= (items/2):
        confidence = 50
    elif successes >= (items/3):
        confidence = 35
    elif successes >= (items/4):
        confidence = 25
    else:
        confidence = 0
    return confidence, successes, items

def CheckCommonEnglish(string, commonEnglish):
    """Take a string and check agaisnt common english words
    after which, return a confidence factor"""
    successes = 0
    confidence = None
    items = len(string)
    for item in commonEnglish:
        for word in string:
            if item == word:
                successes += 1

    #Could add more checks for the length of the array
    #If the array is longer then X, confidence should go up
    if successes >= (items/1.05):
        confidence = 95
    elif successes >= (items/1.15):
        confidence = 85
    elif successes >= (items/1.25):
        confidence = 75
    elif successes >= (items/2):
        confidence = 50
    elif successes >= (items/3):
        confidence = 35
    elif successes >= (items/4):
        confidence = 25
    else:
        confidence = 0
    return confidence, successes, items

def ArrayToWordPrinter(array):
    """This function forfils Stage B
    Feed in an array directly from the text file
    and it will output indivudual words"""
    for item in array:
        print(f"Line of text: {item}")
        item = SplitString(item)
        for i in range(len(item)):
            print(f"Word {i}: {item[i]}")
        print("\n")

#Convert all text files into useable variables
commonEnglish = ReadTextFile('e')
commonMaori = ReadTextFile('m')
maoriLines = ReadTextFile('mlines')
englishLines = ReadTextFile('elines')

#For program simplicity convert everything to lowercase
maoriLines = ArrayToLower(maoriLines)
englishLines = ArrayToLower(englishLines)
commonEnglish = ArrayToLower(commonEnglish)
commonMaori = ArrayToLower(commonMaori)

for line in maoriLines:#chose between maoriLines or englishLines here
    print(line)
    line = SplitString(line)
    mConfidence, mSuccesses, mItems = CheckCommonMaori(line,commonMaori)
    eConfidence, eSuccesses, eItems = CheckCommonEnglish(line,commonEnglish)
    #print(eConfidence, eSuccesses, eItems)
    print(f"My confidence for this line being maori is: {mConfidence}\nMy confidence for this line being english is: {eConfidence}")
    if mConfidence > eConfidence:
        print("I believe this line is in english")
    elif eConfidence > mConfidence:
        print("I believe this line is in english")
    elif eConfidence == mConfidence and eConfidence != 0 and mConfidence != 0:
        print("Due to equal confidences I cannot decide what this is.")
    else:
        print("My algorthims have failed me. Please decide for yourself")


    print("\n")
