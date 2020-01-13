import pathlib
from pathlib import Path

cwd = Path(__file__).parents[0]
print(cwd)

maoriAlphabet = ['a','e','h','i','k','m','n','g','o','p','r','t','u','w']

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

def CheckMaoriAlphabet(array, maoriAlphabet):
    words = []
    counter = 0
    for item in array:
        counter += 1
        nullChars = 0
        totalChar = 0
        for i in range(len(item)):
            totalChar += 1
            if item[i] not in maoriAlphabet:
                nullChars += 1
        if nullChars == 0:
            item = 0,item #Format {0(maori)/1(english)}, {word}}
            words.append(item)
        else:
            item = 1,item
            words.append(item)
        #print(f"Word Length: {totalChar}. Characters in word not in the maori alphabet: {nullChars}")
    #print(words)
    return words


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

#Placeholders for testing
testMaori = SplitString(maoriLines[0])
testEnglish = SplitString(englishLines[0])

print("Note: Words shorter than 5 characters long have a high level of uncertainty. Any punctuation also will throw as an english word\n")
for line in englishLines:
    print(f"The line is: {line}")
    line = SplitString(line)
    words = CheckMaoriAlphabet(line, maoriAlphabet)
    maoriWords = None
    maoriWordsCount = 0
    englishWords = None
    englishWordsCount = 0
    for i in range(len(words)): #Check and increment a counter based on the return from the previous function
        if words[i][0] == 0: #if the word has is associated with a 0 its classed as maori by the program
            maoriWordsCount += 1
            if not maoriWords:
                maoriWords = words[i][1] + "\n"
            else:
                maoriWords = maoriWords + words[i][1] + "\n"
        else: #if it has 1 it is classed as english
            englishWordsCount +=1
            if not englishWords:
                englishWords = words[i][1] + "\n"
            else:
                englishWords = englishWords + words[i][1] + "\n"
    print(f"I believe there are {maoriWordsCount} maori word's in this line and {englishWordsCount} english word's in this line\n")
    print(f"I believe these are all maori words:\n{maoriWords}\nI think these are the english words:\n{englishWords}")
