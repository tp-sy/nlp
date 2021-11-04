from typing import List
from nltk.corpus import wordnet as wn
from nltk.corpus import brown
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures
from nltk import pos_tag
 
EXAMPLE_1 = "hot as sun"
EXAMPLE_2 = "hot as city"


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
    """
    Calculate collocation for the word
    """
    collocs = {}
    for w in tagged:
        if not w[1] in nouns:
            pass
        AB = bcf.score_ngram(BigramAssocMeasures.likelihood_ratio, word, w[0])
        if AB and AB > threshold:
            collocs[w] = AB
    return collocs

def parse_sentence(sentence: str, expected: bool, noun_pos: int):
    """
    Parses a single sentences and finds metaphors
    """
    tags = tag_sentence(sentence)
    adjs = []
    ns = []
    metaphors = {}
    for pos, tag in enumerate(tags):
        if tag[1] in adj or tag[1] in adv:
            adjs.append(tag[0])
        if tag[1] in nouns:
            if pos + 1 == noun_pos:
                ns.append(tag[0])
            else:
                print("Wrong noun position, skipping")

    if ns and adjs:
        for a in adjs:
            for n in ns:
                metaphors[f"{a}:{n}"] = {
                    "result": is_metaphor(n, a),
                    "expected": expected
                }
    return metaphors
def is_metaphor(noun, adjective):
    """
    Check if a noun-adjective pair is a metaphor
    """
    senses = {}
    concretes = {}
    # Get all the different meanings of the adjective
    lemmas = wn.lemmas(adjective)
    if not lemmas:
        senses[adjective] = "UNKNOWN"
    elif len(senses) == 1:
        senses[adjective] = "NO METAPHOR"
    else:
        senses[adjective] = lemmas

    # Get the category of the noun
    collocations = get_collocation(noun)
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
    if S1:
        metaphor = True # assume a metaphor unless compatibility found
        for adjective, lemmas in senses.items():
            if lemmas == "UNKNOWN" or lemmas == "NO METAPHOR":
                continue
            for lemma in lemmas:
                for synset in S1:
                    compatibility = synset.wup_similarity(lemma.synset())
                    if compatibility >= 0.3:
                        metaphor = False
                        break
        return metaphor
    return False

from multiprocessing import Pool
import json

def process_line(line):
    """
    Some preprocessing on the line before parsing the sentence
    """
    line = line.strip("\n")
    if line.endswith("y"):
        expected = True
    else:
        expected = False
    line, ann = line.rsplit(maxsplit=1) # Split off the annotations
    if ann.startswith("@"):
        try:
            noun_pos = int(ann[1]) # get the position of the noun in the metaphor
        except:
            print("Failed to get noun pos")
            return {}
        return parse_sentence(line, expected, noun_pos)
    return {}


with open("data/type1_metaphor_annotated.txt") as fd:
    lines = list(fd.readlines())
    #metaphors = []
    #with Pool(processes=8) as pool: # Do in 8 processes
    #    for line in lines:
    #        res = pool.apply_async(process_line, args=(line,))
    #        metaphors.append(res)

    #metaphors_dict = {}
    #for i, result in enumerate(metaphors):
        # Get the result after everything has been processed to not block the thread
    #    print(i)
    #    for key, value in result.get().items():
    #        if key in metaphors_dict:
    #            print("Found colliding metaphors")
    #        metaphors_dict[key] = value 
    metaphors_dict = {}
    for line in lines:
        result = process_line(line)
        if result:
            metaphors_dict.update(result)

    with open("type3_results.json", "w") as wfd:
        json.dump(metaphors_dict, wfd)
