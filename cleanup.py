# Contains all functions that deal with stop word removal.

from document import Document
import string


def remove_symbols(text: str) -> str:
    """
    Eliminates all punctuation and similar symbols from the provided string.
    Also removes any occurrences of "'s".
    :param text: Input string to be processed.
    :return: Processed string with symbols removed.
    """
    # Strip punctuation characters
    cleaned_text = text.translate(str.maketrans('', '', string.punctuation))
    # Remove "'s"
    cleaned_text = cleaned_text.replace("'s", "")
    return cleaned_text


def is_stop_word(term: str, stop_word_list: list[str]) -> bool:
    """
    Determines if a term is a stop word.
    :param term: Term to be checked.
    :param stop_word_list: List of stop words to check against.
    :return: True if the term is a stop word, False otherwise.
    """
    return term.lower() in stop_word_list


def remove_stop_words_from_term_list(term_list: list[str], stop_word_list=None) -> list[str]:
    """
    Filters out stop words from a list of terms.
    :param term_list: List of terms to be filtered.
    :param stop_word_list: List of stop words to remove.
    :return: List of terms with stop words removed.
    """
    # Filter out stop words from the term list
    filtered_terms = [term for term in term_list if not is_stop_word(term, stop_word_list)]
    return filtered_terms


def filter_collection(collection: list[Document]):
    """
    Filters stop words from the term list of each document in the collection.
    The filtered terms are stored in the document's filtered_terms attribute.
    :param collection: List of Document objects to be processed.
    """
    # Apply stop word removal to each document's term list
    for doc in collection:
        doc.filtered_terms = remove_stop_words_from_term_list(doc.terms, stop_word_list)


def load_stop_word_list(raw_file_path: str) -> list[str]:
    """
    Loads a list of stop words from a text file, where each line contains one stop word.
    :param raw_file_path: Path to the text file containing stop words.
    :return: List of stop words.
    """
    with open(raw_file_path, 'r') as file:
        stop_words = [line.strip().lower() for line in file.readlines()]
    return stop_words


def create_stop_word_list_by_frequency(collection: list[Document], low_freq: int = 5, high_freq: int = 100) -> list[str]:
    """
    Generates a list of stop words based on their frequency in the collection.
    Terms with very low or very high frequency are considered stop words.
    :param collection: List of Document objects to analyze.
    :param low_freq: Lower frequency threshold.
    :param high_freq: Upper frequency threshold.
    :return: List of stop words.
    """
    term_frequencies = {}
    for doc in collection:
        for term in doc.terms:
            normalized_term = term.lower()
            if normalized_term in term_frequencies:
                term_frequencies[normalized_term] += 1
            else:
                term_frequencies[normalized_term] = 1

    stop_words = [term for term, freq in term_frequencies.items() if freq <= low_freq or freq >= high_freq]
    return stop_words
