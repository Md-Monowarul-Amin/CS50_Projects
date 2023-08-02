import nltk
import sys
# import nltk
# nltk.download('punkt')

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> N V | NP VP P NP NP VP | NP VP Conj NP VP | NP VP 
NP -> N | Det N | Det AP N | P NP | NP P NP | N PP 
VP -> V | V NP | V PP | VP Adv | Adv VP | VP Conj VP | V NP Adv
AP -> Adj | AP Adj 
PP -> P NP | P
"""
# | NP VP NP | NP Conj NP VP
grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    sentence = sentence.lower()
    sentence = nltk.word_tokenize(sentence)
    for word in sentence:
        ok = 0
        for char in word:
            if 65 <= ord(char) <= 90 or 97 <= ord(char) <= 122:
                ok = 1
                break
        if not ok:
            sentence.remove(word)
    #print(sentence)
    return sentence
    


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """

    noun_phrase_chunks = []
    #print(tree)
    parented_tree = nltk.tree.ParentedTree.convert(tree)

    for subtree in parented_tree.subtrees():
        if subtree.label() == "N":
            noun_phrase_chunks.append(subtree.parent())
    #print(noun_phrase_chunks)
    return noun_phrase_chunks


if __name__ == "__main__":
    main()
