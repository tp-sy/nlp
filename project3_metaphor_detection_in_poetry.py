import nltk
from nltk.corpus import brown
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures
import math
#nltk.download('brown')

words = brown.words()
#tagged = nltk.pos_tag(words)
tagged = brown.tagged_words()
size_of_corpus = len(brown.words())

# Collocation of two words (Score for how often they co-occur)
bcf = BigramCollocationFinder.from_words(words)
print(bcf.score_ngram(BigramAssocMeasures.likelihood_ratio, ".", "The"))

# JJ = Adjective
# RB = adverb, RBR, RBT, RN, RB?
# VB = verb (base form), VBD, VBG, VBN, VBP, VBZ
categories_of_interest = ['JJ', 'RB', 'RBR', 'RBT', 'RN', 'RB', 'VB', 'VBD' 'VBG', 'VBN', 'VBP', 'VBZ']

considered_words = ["man", "sky", "life", "love"]
results = []
with open("task1_results.txt", "w") as f:
    for w1 in considered_words:
        for w2 in tagged:
            # If the POS tag matches those of interest, and word hasn't been added yet
            if (w2[1] in categories_of_interest and w2 not in results):
                AB = bcf.score_ngram(BigramAssocMeasures.likelihood_ratio, w1, w2[0])
                # If no collocation
                if(AB == None):
                    continue
                MI = math.log10((AB* size_of_corpus)/ words.count(w1) * words.count(w2[0]) * 3) / math.log10(2)
                if(MI >= 3.0):
                    print(w1, w2, MI)
                    results.append(w2)
                    f.write(str(w1) + "\t" + str(w2) + "\t" +  str(MI) + "\n")


