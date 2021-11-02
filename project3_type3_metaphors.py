from typing import List
from nltk.corpus import wordnet as wn
from nltk.corpus import brown
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures
from nltk import pos_tag
import sys

EXAMPLE_1 = "Yellow potato is scary"
EXAMPLE_2 = "Whatever floats your fancy boat"

# nouns
# NN NN$ NNS NNS$ NP NP$ NPS NPS$ NR NRS
nouns = ["NN", "NN$", "NNS", "NNS$", "NP", 
    "NP$", "NPS", "NPS$", "NR", "NRS"]


# manually picked from here:
# https://provalisresearch.com/products/content-analysis-software/wordstat-dictionary/wordnet-based-categorization-dictionary/
concrete_noun_categories = [
    "animal",
    "artifact",
    "body",
    "food",
    "location",
    "object",
    "person",
    "plant"
]

# JJ = Adjective
adj = ["JJ"]
# RB = adverb, RBR, RBT, RN, RB?
adv = ["RB", "RBR", "RBT", "RN"]
words = brown.words()
tagged = brown.tagged_words()
bcf = BigramCollocationFinder.from_words(words)

def get_synsets(word: str, category=wn.NOUN) -> List:
    """
    returns a list of categories for given word
    word is assumed to be a noun
    """
    return wn.synsets(word, pos=category)

def tag_sentence(sentence: str):
    return pos_tag(sentence.split())

def is_concrete_noun(synset: List):
    """
    Return true if any of the hypernyms are in concrete category
    """
    for hypernym_paths in synset.hypernym_paths():
        for hypernym in hypernym_paths:
            if hypernym.name().split(".")[0] in concrete_noun_categories:
                return True
    return False

def get_collocation(word, threshold = 3):
    collocs = {}
    for w in tagged:
        if not w[1] in nouns:
            pass
        AB = bcf.score_ngram(BigramAssocMeasures.likelihood_ratio, word, w[0])
        if AB and AB > threshold:
            collocs[w] = AB
    return collocs

def is_metaphor(sentence: str):
    tags = tag_sentence(sentence)
    senses = {}
    noun_brown = {}
    concretes = {}
    for tag in tags:
        if tag[1] in adj:
            # Get all the different meanings of the adjective
            lemmas = wn.lemmas(tag[0])
            if not lemmas:
                senses[tag[0]] = "UNKNOWN"
            elif len(senses) == 1:
                senses[tag[0]] = "NO METAPHOR"
            else:
                senses[tag[0]] = lemmas
        if tag[1] in nouns:
            # Get the category of the noun
            collocations = get_collocation(tag[0])
            for k, v in collocations.items():
                # Need to filter category here
                for synset in get_synsets(k[0]):
                    if not synset:
                        # wn does not know this noun
                        continue
                    if is_concrete_noun(synset):
                        # Store all concrete nouns in a dict
                        concretes[synset] = v

    # sort dict by value and take the last 3
    sorted_concretes = [
        k for k, v in sorted(
            concretes.items(), key=lambda item: item[1]
            )
        ]
    S1 = sorted_concretes[3:]
    if not S1:
        print("No concrete nouns")
    else:
        for adjective, lemmas in senses.items():
            if lemmas == "UNKNOWN" or lemmas == "NO METAPHOR":
                continue
            for lemma in lemmas:
                metaphor = False
                for synset in S1:
                    compatibility = synset.wup_similarity(lemma.synset())
                    if compatibility >= 0.3:
                        print("Not a metaphor")
                        break
                else:
                    # No compatibility found, is a metaphor
                    metaphor = True
                    print(f"{sentence} has metaphor")
                # compatibility found, not a metaphor
