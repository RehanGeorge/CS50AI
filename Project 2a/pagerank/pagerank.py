import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    #Dictionary to capture return value of probability distribution
    probability_distribution = dict()

    # Initialize dictionary with all probabilities initially set to 0
    for current_page in corpus:
        probability_distribution[current_page] = 0

    # If page has no links, choose randomly from all pages in the corpus
    if len(corpus[page]) == 0:
        for current_page in corpus:
            probability_distribution[current_page] = 1 / len(corpus)
        return probability_distribution
    
    # If page has links, choose randomly from links
    else:
        for link in corpus[page]:
            probability_distribution[link] = damping_factor / len(corpus[page])
        # print(probability_distribution)
        # Add probability of choosing a random page
        for current_page in corpus:
            probability_distribution[current_page] += (1 - damping_factor) / len(corpus)
        # print(probability_distribution)
        return probability_distribution


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Dictionary to capture return value of PageRank values
    page_rank_values = dict()

    # Initialize dictionary with all page ranks initially set to 0
    for page in corpus:
        page_rank_values[page] = 0

    # Choose a random page to start
    current_page = random.choice(list(corpus.keys()))

    # Run n times to populate page rank values
    for i in range(n):
        # Update page rank value for current page
        page_rank_values[current_page] += 1 / n
        # Update transition model
        probability_distribution = transition_model(corpus, current_page, damping_factor)
        # Update current page based on transition model
        current_page = random.choices(list(probability_distribution.keys()), weights=list(probability_distribution.values()))[0]
    return page_rank_values


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Dictionary to capture return value of PageRank values
    page_rank_values = dict()

    # Initialize dictionary with all page ranks initially set to 1 / N
    for page in corpus:
        page_rank_values[page] = 1 / len(corpus)

    # Initialize second dictionary to capture new page rank values
    new_page_rank_values = dict()

    # Initialize second dictionary with all page ranks initially set to 0
    for page in corpus:
        new_page_rank_values[page] = 0

    # Initialize variable to capture difference between old and new page rank values
    difference = 1

    # Run until difference between old and new page rank values is less than 0.001
    while difference > 0.001:
        # Update page rank values
        for page in corpus:
            # Update page rank value for current page based on random selection
            new_page_rank_values[page] = (1 - damping_factor) / len(corpus)
            # Update page rank value for all pages that link to current page
            for link in corpus:
                if page in corpus[link]:
                    new_page_rank_values[page] += damping_factor * page_rank_values[link] / len(corpus[link])
        # Update difference between old and new page rank values
        difference = 0
        for page in corpus:
            difference += abs(new_page_rank_values[page] - page_rank_values[page])
        # Update page rank values
        for page in corpus:
            page_rank_values[page] = new_page_rank_values[page]
    return page_rank_values


if __name__ == "__main__":
    main()
