import nltk
import sys

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

NONTERMINALS = f"""
S -> NP VP | NP VP Conj NP VP | NP VP Conj VP
NP -> N | Det N | Det N PP | Det AP N | Det AP N PP | N PP | Det N Adv
AP -> Adj | Adj AP
VP -> V | V NP | V PP NP | V Adv | Adv V NP
PP -> P | P NP
"""

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
    # Convert sentence to lowercase
    sentence = sentence.lower()

    # Tokenize sentence
    tokens = nltk.word_tokenize(sentence)

    # Remove words that do not contain at least one alphabetic character
    tokens = [token for token in tokens if any(c.isalpha() for c in token)]

    return tokens


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    # Create list of noun phrase chunks
    chunks = []

    # Iterate over subtrees of tree
    for subtree in tree.subtrees():

        # If subtree is a noun phrase chunk, append to list
        if subtree.label() == "NP":
            if unique_np(subtree):
                chunks.append(subtree)
            
    # Return list of noun phrase chunks
    return chunks


# Helper function to determine if a subtree contains any other noun phrase subtrees:
def unique_np(subtree):
    """
    Return True if subtree does not contain any other noun phrase subtrees.
    """
    for sub in subtree.subtrees():
        if sub.label() == "NP" and sub != subtree:
            return False
    return True

if __name__ == "__main__":
    main()
