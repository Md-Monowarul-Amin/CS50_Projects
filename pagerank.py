import copy
import math
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

    ret_dict = dict()

    for temp_page in corpus:
        ret_dict[temp_page] = (1 - damping_factor) / len(corpus)

    for temp_page in corpus[page]:
        ret_dict[temp_page] += damping_factor / len(corpus[page])
    
    return ret_dict


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    ret_dict = dict()
    
    for temp_page in corpus:
        ret_dict[temp_page] = 0

    page_list = []
    for temp_page in corpus:
        page_list.append(temp_page)

    current_page = random.choice(page_list)

    for i in range(n):
        option_list = []
        weight_list = []

        probability_list = transition_model(corpus, current_page, damping_factor)

        for temp_page in probability_list:
            option_list.append(temp_page)
            weight_list.append(probability_list[temp_page])
        
        current_page = random.choices(option_list, weights=weight_list)[0]
        ret_dict[current_page] += 1

    for temp_page in ret_dict:
        ret_dict[temp_page] /= n
    
    return ret_dict




def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    ret_dict = dict()
    new_rank_dict = dict()

    for temp_page in corpus:
        ret_dict[temp_page] = 1 / len(corpus)
    
    ok = 1
    while ok:
        new_rank_dict = copy.deepcopy(ret_dict)
        for temp_page in ret_dict:
            choice = 0
            for new_page in corpus:
                if temp_page in corpus[new_page]:
                    choice += ret_dict[new_page] / len(corpus[new_page])
                if not corpus[new_page]:
                    choice += ret_dict[new_page] / len(corpus)
            
            new_rank_dict[temp_page] = (1 - damping_factor) / len(corpus) + damping_factor * choice
        
        ok = 0
        for temp_page in ret_dict:

            if not new_rank_dict[temp_page] * 0.999 < ret_dict[temp_page] < new_rank_dict[temp_page] * 1.001:
                ok = 1

            ret_dict[temp_page] = new_rank_dict[temp_page]

    return ret_dict




if __name__ == "__main__":
    main()
