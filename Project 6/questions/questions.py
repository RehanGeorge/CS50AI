import nltk
import sys
import os
import string
import math

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():
    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {filename: tokenize(files[filename]) for filename in files}
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    # Create a dictionary to store the files
    files = {}

    # Loop through the files in the directory
    for file_name in os.listdir(directory):
        # Get the path of the file
        path = os.path.join(directory, file_name)

        # Open the file and read its contents
        with open(path, encoding="utf8") as f:
            files[file_name] = f.read()

    # Return the dictionary of files
    return files


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    # Tokenize the lowercased document
    tokens = nltk.word_tokenize(document.lower())

    # Remove the stop words and punctuation
    stop_words = nltk.corpus.stopwords.words("english")
    filtered_tokens = [
        token
        for token in tokens
        if token not in stop_words and token not in string.punctuation
    ]

    # Return the list of words
    return filtered_tokens


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    # Create a set to store the words
    words = set()

    # Create a dictionary to store the IDF Values
    idf_values = {}

    # Get the total number of documents
    total_documents = len(documents)

    # Loop through the documents
    for document in documents:
        # Add the words to the set
        words.update(documents[document])

    # Loop through the words and calculate the IDF value
    for word in words:
        # Get the number of documents that contain the word
        num_documents = sum([word in documents[document] for document in documents])

        # Calculate the IDF value
        idf = math.log(total_documents / num_documents)

        # Add the IDF value to the dictionary
        idf_values[word] = idf

    # Return the dictionary of IDF values
    return idf_values


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    # Calculate the tf-idf score for each file
    scores = {}

    for filename in files:
        # Calculate the tf-idf score for the file
        score = 0
        for word in query:
            if word in files[filename]:
                tf = files[filename].count(word)
                idf = idfs[word]
                score += tf * idf
        scores[filename] = score

    # Sort the files by their tf-idf scores
    sorted_files = [
        key for key, value in sorted(scores.items(), key=lambda x: x[1], reverse=True)
    ]

    # Return the top n files
    top_n_files = sorted_files[:n]
    return top_n_files


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    # Calculate the idf score for each sentence
    scores = {}

    for sentence in sentences:
        # Calculate the matching word measure score & query term density score for the sentence
        score = {"matching_word_measure": 0.0, "query_term_density": 0.0}
        matching_words = 0

        for word in query:
            if word in sentences[sentence]:
                score["matching_word_measure"] += idfs[word]
                matching_words += 1

        # Calculate the query term density score
        score["query_term_density"] = matching_words / len(sentences[sentence])

        # Calculate the final score
        scores[sentence] = score

    # Sort the sentences by their matching word measure scores and then query term density scores
    sorted_sentences = [
        key
        for key, value in sorted(
            scores.items(),
            key=lambda x: (x[1]["matching_word_measure"], x[1]["query_term_density"]),
            reverse=True,
        )
    ]

    # Return the top n sentences
    top_n_sentences = sorted_sentences[:n]
    return top_n_sentences


if __name__ == "__main__":
    main()
