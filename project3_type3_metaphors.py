from typing import List
from nltk.corpus import wordnet as wn
from nltk.corpus import brown
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures
from nltk import pos_tag
import sys

EXAMPLE_1 = "Yellow potato is scary"
EXAMPLE_2 = "Whatever floats your fancy boat"

# JJ = Adjective
# RB = adverb, RBR, RBT, RN, RB?

# nouns
# NN NN$ NNS NNS$ NP NP$ NPS NPS$ NR NRS
nouns = ["NN", "NN$", "NNS", "NNS$", "NP", 
    "NP$", "NPS", "NPS$", "NR", "NRS"]

adj = ["JJ"]
adv = ["RB", "RBR", "RBT", "RN"]
words = brown.words()
tagged = brown.tagged_words()
bcf = BigramCollocationFinder.from_words(words)

def get_category(word: str, category=wn.NOUN) -> List:
    """
    returns a list of categories for given word
    word is assumed to be a noun
    """
    return wn.synsets(word, pos=category)

def tag_sentence(sentence: str):
    return pos_tag(sentence.split())

def is_metaphor(sentence: str):
    tags = tag_sentence(sentence)
    senses = {}
    noun_brown = {}
    concretes = {}
    for tag in tags:
        if tag[1] in adj:
            # Get all the different meanings of the adjective
            s = wn.lemmas(tag[0])
            if not s:
                senses[tag[0]] = "UNKNOWN"
            elif len(senses) == 1:
                senses[tag[0]] = "NO METAPHOR"
            else:
                senses[tag[0]] = s
        if tag[1] in nouns:
            # Get the category of the noun
            collocations = get_collocation(tag[0])
            for k, v in collocations.items():
                # Need to filter category here
                category = get_category(k[0])
                concretes[k[0]] = (v, category)

        # sort k-vs by value and get first 3
        sorted_concretes = [
            (k, v) for k, v in sorted(
                concretes.items(), key=lambda item: item[1][0]
                )
            ]
        S1 = sorted_concretes[:3]

        for adjective, sens in senses.items():
            if sens == "UNKNOWN" or sens == "NO METAPHOR":
                continue
            for word, (v, synset) in S1:
                for s in synset:
                    # TODO: Needs "word.type.num" format...
                    compatibility = s.wup_similarity(wn.synset(adjective))
                    if compatibility >= 0.3:
                        break
            else:
                # No compatibility found, is a metaphor
                metaphor = True
            # compatibility found, not a metaphor
            metaphor = False
            print(adjective, metaphor)

def get_collocation(word, threshold = 3):
    collocs = {}
    for w in tagged:
        if not w[1] in nouns:
            pass
        AB = bcf.score_ngram(BigramAssocMeasures.likelihood_ratio, word, w[0])
        if AB and AB > threshold:
            collocs[w] = AB
    return collocs


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("usage: script.py <word> <type>")
    elif sys.argv[2] == "noun":
        print(get_category(str(sys.argv[1])))
    elif sys.argv[2] == "adv":
        print(get_category(str(sys.argv[1]), wn.ADV))
    elif sys.argv[2] == "adj":
        print(get_category(str(sys.argv[1]), wn.ADJ))
    else:
        print("usage: script.py <word> <type>")