# # Contains all functions that deal with stop word removal.

# from document import Document
import string
import re
from document import Document
from collections import Counter


def remove_symbols(text_string: str) -> str:

    text_string = re.sub(r"'s\b", "", text_string)

    punctuations = str.maketrans("", "", string.punctuation)
    text_string = text_string.translate(punctuations)
    
    return text_string


def is_stop_word(term: str, stop_word_list: list[str]) -> bool:
    """
    Checks if a given term is a stop word.
    :param stop_word_list: List of all considered stop words.
    :param term: The term to be checked.
    :return: True if the term is a stop word.
    """
    term = remove_symbols(term)

    filtered_word = ''

    if term.lower() not in stop_word_list:
        filtered_word = term
    
    else:

        filtered_word = None

    return filtered_word


def remove_stop_words_from_term_list(term_list: list[str]) -> list[str]:

    
    """
    Takes a list of terms and removes all terms that are stop words.
    :param term_list: List that contains the terms
    :return: List of terms without stop words
    """
    filtered_list = []
    filtered_word = ''
    # Hint:  Implement the functions remove_symbols() and is_stop_word() first and use them here.
    # TODO: Implement this function. (PR02)
    stop_words_list = load_stop_word_list('raw_data//englishST.txt')

    for term in term_list:

        filtered_word = is_stop_word(term,stop_word_list=stop_words_list)
        
        if filtered_word is not None:

            filtered_list.append(filtered_word)

    return filtered_list




def filter_collection(collection: list[Document]):
    """
    For each document in the given collection, this method takes the term list and filters out the stop words.
    Warning: The result is NOT saved in the documents term list, but in an extra field called filtered_terms.
    :param collection: Document collection to process
    """
    # Hint:  Implement remove_stop_words_from_term_list first and use it here.
    # TODO: Implement this function. (PR02)

    for collect in collection:
        term_list = collect.terms
        collect.terms = []
        collect.terms = remove_stop_words_from_term_list(term_list=term_list)    
    return collection
    



def load_stop_word_list(raw_file_path: str) -> list[str]:
    """
    Loads a text file that contains stop words and saves it as a list. The text file is expected to be formatted so that
    each stop word is in a new line, e. g. like englishST.txt
    :param raw_file_path: Path to the text file that contains the stop words
    :return: List of stop words
    """
    stop_words = []
    with open(raw_file_path) as stop_words_file:
        stop_words = stop_words_file.read().splitlines()
    return stop_words


def create_stop_word_list_by_frequency(collection: list[Document]) -> list[str]:
    """
    Uses the method of J. C. Crouch (1990) to generate a stop word list by finding high and low frequency terms in the
    provided collection.
    :param collection: Collection to process
    :return: List of stop words
    """
    term_list = []
    term = ''
    term_frequencies = Counter()

    for document in collection:
        term_list = document.terms
        for term in term_list:
            term_frequencies.update(term)

    total_terms = sum(term_frequencies.values())
    high_freq_threshold = total_terms * 0.01  # Example: top 1% as high frequency
    low_freq_threshold = total_terms * 0.0001  # Example: bottom 0.01% as low frequency

    # Step 3: Generate stop word list
    stop_words = set()
    for term, freq in term_frequencies.items():
        if freq >= high_freq_threshold or freq <= low_freq_threshold:
            stop_words.add(term)

    return list(stop_words)
