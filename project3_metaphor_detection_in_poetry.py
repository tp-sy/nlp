import nltk
from nltk.corpus import brown
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures
import math
#nltk.download('brown')

words = brown.words()
#tagged = nltk.pos_tag(words)
tagged = brown.tagged_words()
unique_tagged = list(set(brown.tagged_words()))
size_of_corpus = len(brown.words())
stopwords = [".", ",", "a", "an", "the", "no"]

# Collocation of two words (Score for how often they co-occur)
bcf = BigramCollocationFinder.from_words(words)

def task1():
    # JJ = Adjective
    # RB = adverb, RBR, RBT, RN, RB?
    # VB = verb (base form), VBD, VBG, VBN, VBP, VBZ
    categories_of_interest = ['JJ', 'RB', 'RBR', 'RBT', 'RN', 'RB', 'VB', 'VBD' 'VBG', 'VBN', 'VBP', 'VBZ']

    considered_words = ["man", "sky", "life", "love"]
    with open("task1_results2.txt", "w") as f:
        for w1 in considered_words:
            results = []
            for count, w2 in enumerate(unique_tagged):
                if(count%1000 == 0):
                    print("{} unique words processed.".format(count))
                # If the POS tag matches those of interest, and word hasn't been added yet
                if (w2[1] in categories_of_interest and w2 not in results):
                    AB = bcf.score_ngram(BigramAssocMeasures.raw_freq, w1, w2[0])
                    # If no collocation
                    if(AB == None):
                        continue
                    # Mutual information score
                    MI = math.log10(((AB*size_of_corpus)*size_of_corpus)/ (words.count(w1) * words.count(w2[0]) * 3)) / math.log10(2)
                    if(MI >= 3.0):
                        print(w1, w2, MI)
                        results.append(w2)
                        f.write(str(w1) + "\t" + str(w2) + "\t" +  str(MI) + "\n")
def task2():
    results2 = []
    with open("task2_unfiltered_results_remeas.txt", "a") as res_f:
        res_f.write("Metaphor" +"\t" + "Prediction" + "\t" + "Answer" + "\n")
        with open("metaphor_annotated_corpus.txt", "r") as f:
            file = f.readlines()
            #file = ["the sky is cloudy , yellowed by the smoke . @2@n"]
            for line in file:
                split = line.split(" ")
                head = int(''.join(x for x in split[-1] if x.isdigit()))-1
                head_word = split[head]
                yes_or_no = split[-1][-2]
                if(yes_or_no == '@'):
                    yes_or_no = split[-1][-1]
                if(yes_or_no == 's'):
                    continue
                # Remove stopwords
                split = [word.lower() for word in split if word not in stopwords]
                head = split.index(head_word)
                ans = {"y": True, "n": False}
                decision = {True: "Correct", False: "Incorrect"}
                #print(split[head])
                is_metaphor = []
                print(str(split[head]) + " " + str(split[head+1]) + " " + str(split[head+2]))
                for i in range(1,3):  
                    AB = bcf.score_ngram(BigramAssocMeasures.raw_freq, split[head], split[head+i])
                    print(i, AB)
                    # If no collocation
                    if(AB == None):
                        is_metaphor.append(True)
                        continue
                    # Mutual information score
                    MI = math.log10(((AB* size_of_corpus)*size_of_corpus)/ (words.count(split[head]) * words.count(split[head+i]) * 2)) / math.log10(2)
                    print("MI " + str(MI))
                    if(MI > 3.0):
                        is_metaphor.append(False)
                    else:
                        is_metaphor.append(True)
                # Sentence is a metaphor
                if(is_metaphor[0] == False and is_metaphor[1] == False):
                    print("Prediction: False" + "\tAnswer: " + str(ans[yes_or_no]) + "\tDecision: " + decision[ans[yes_or_no] == False])
                    res_f.write(str(split[head]) + " " + str(split[head+1]) + " " + str(split[head+2]) +"\t"+"False" + "\t" + str(ans[yes_or_no]) + "\n")
                    results2.append(False == ans[yes_or_no])
                # Only if both of the MI's are greater than 3 (True), the sentence is not a metaphor
                else:
                    print("Prediction: True" + "\tAnswer: " + str(ans[yes_or_no]) + "\tDecision: " + decision[ans[yes_or_no] == True])
                    res_f.write(str(split[head]) + " " + str(split[head+1]) + " " + str(split[head+2]) +"\t"+"True" + "\t" + str(ans[yes_or_no]) + "\n")
                    results2.append(True == ans[yes_or_no])
    # Remove duplicates
    with open("task2_unfiltered_results_remeas.txt", "r") as f:
        file = f.readlines()
    with open("task2_results_remeas.txt", "w") as res_f:
	for i in file:
            res_f.write(i)
