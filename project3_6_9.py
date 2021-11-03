from typing import List
import nltk
from nltk.corpus import wordnet as wn
from nltk.corpus import reuters as rt

# nltk.download('reuters')
# nltk.download('wordnet')

stopwords = [".", ",", "a", "an", "the", "no"]

def get_synsets(word: str, category=wn.NOUN) -> List:
    """
    returns a list of categories for given word
    word is assumed to be a noun
    """
    return wn.synsets(word, pos=category)

def get_synsets_rt(word: str) -> List:
    """
    returns a list of categories for given word
    word is assumed to be a noun
    """
    return rt.categories(word)

def compareLists(l1: List, l2: List):
    l1.sort()
    l2.sort()
    for x in l1:
        if str(x) == "NOT A WORD":
            break
        else:
            x_lemmas = [str(lemma.name()) for lemma in x.lemmas()]
        for y in l2:
            if str(y) == "NOT A WORD":
                break
            else:
                y_lemmas = [str(lemma.name()) for lemma in y.lemmas()]
                for x_l in x_lemmas:
                    for y_l in y_lemmas:
                        if x_l == y_l:
                            return True
    return False

def task7():
    with open("metaphor_annotated_corpus.txt", "r") as f:
        file = f.readlines()
        r = []
        linecount = 0
        for line in file:
            splitted_line = line.split(" ")
            result = splitted_line.pop().split('@')[2].strip()
            list_of_synsets = []
            for l in splitted_line:
                if l in stopwords:
                    list_of_synsets.append(["NOT A WORD"])
                else:
                    s = get_synsets(l)
                    list_of_synsets.append(s)

            answers = []
            while len(list_of_synsets) > 0:
                inspected_list = list_of_synsets.pop()
                for l in list_of_synsets:
                    answer = compareLists(inspected_list, l)
                    if answer:
                        answers.append([True, result])
                        break

            if len(answers) > 0:
                r.append([True, result, linecount])
            else:
                r.append([False, result, linecount])

            linecount = linecount + 1
    corrects = 0
    uncorrects = 0
    for d in r:
        if d[0] == True and d[1] == 'y':
            corrects = corrects + 1 
        elif d[0] == False and d[1] == 'n':
            corrects = corrects + 1
        else:
            uncorrects = uncorrects + 1


    with open("task7_results.txt", "w") as f:
        f.write("Total" +"\t" + "Correct" + "\t" + "Uncorrect" + "\n")
        f.write(str(corrects + uncorrects) +"\t" + str(corrects) + "\t" + str(uncorrects) + "\n")
        f.write("Line" +"\t" + "Prediction" + "\t" + "Answer" + "\n")
        for d in r:
            f.write(str(d[2]) + "\t" + str(d[0]) + "\t" + str(d[1]) + "\n")

def task8():
    with open("metaphor_annotated_corpus.txt", "r") as f:
        file = f.readlines()
        r = []
        linecount = 0
        for line in file:
            splitted_line = line.split(" ")
            result = splitted_line.pop().split('@')[2].strip()
            list_of_synsets = []
            for l in splitted_line:
                if l in stopwords:
                    list_of_synsets.append(["NOT A WORD"])
                else:
                    s = get_synsets_rt(l)
                    list_of_synsets.append(s)

            answers = []
            while len(list_of_synsets) > 0:
                inspected_list = list_of_synsets.pop()
                for l in list_of_synsets:
                    answer = compareLists(inspected_list, l)
                    if answer:
                        answers.append([True, result])
                        break

            if len(answers) > 0:
                r.append([True, result, linecount])
            else:
                r.append([False, result, linecount])

            linecount = linecount + 1
    corrects = 0
    uncorrects = 0
    for d in r:
        if d[0] == True and d[1] == 'y':
            corrects = corrects + 1 
        elif d[0] == False and d[1] == 'n':
            corrects = corrects + 1
        else:
            uncorrects = uncorrects + 1


    with open("task8_results.txt", "w") as f:
        f.write("Total" +"\t" + "Correct" + "\t" + "Uncorrect" + "\n")
        f.write(str(corrects + uncorrects) +"\t" + str(corrects) + "\t" + str(uncorrects) + "\n")
        f.write("Line" +"\t" + "Prediction" + "\t" + "Answer" + "\n")
        for d in r:
            f.write(str(d[2]) + "\t" + str(d[0]) + "\t" + str(d[1]) + "\n")




task8()


