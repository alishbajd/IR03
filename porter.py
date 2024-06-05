# Contains all functions related to the porter stemming algorithm.

from document import Document


def get_measure(term: str) -> int:
    """
    Returns the measure m of a given term [C](VC){m}[V].
    :param term: Given term/word
    :return: Measure value m
    """
    # TODO: Implement this function. (PR03)
    raise NotImplementedError('This function was not implemented yet.')


def condition_v(stem: str) -> bool:
    """
    Returns whether condition *v* is true for a given stem (= the stem contains a vowel).
    :param stem: Word stem to check
    :return: True if the condition *v* holds
    """
    # TODO: Implement this function. (PR03)
    raise NotImplementedError('This function was not implemented yet.')


def condition_d(stem: str) -> bool:
    """
    Returns whether condition *d is true for a given stem (= the stem ends with a double consonant (e.g. -TT, -SS)).
    :param stem: Word stem to check
    :return: True if the condition *d holds
    """
    # TODO: Implement this function. (PR03)
    raise NotImplementedError('This function was not implemented yet.')


def cond_o(stem: str) -> bool:
    """
    Returns whether condition *o is true for a given stem (= the stem ends cvc, where the second c is not W, X or Y
    (e.g. -WIL, -HOP)).
    :param stem: Word stem to check
    :return: True if the condition *o holds
    """
    # TODO: Implement this function. (PR03)
    raise NotImplementedError('This function was not implemented yet.')


def stem_term(term: str) -> str:
    """
    Stems a given term of the English language using the Porter stemming algorithm.
    :param term:
    :return:
    """
    # TODO: Implement this function. (PR03)
    # Note: See the provided file "porter.txt" for information on how to implement it!
    raise NotImplementedError('This function was not implemented yet.')

def stem_all_documents(collection: list[Document]):
    """
    For each document in the given collection, this method uses the stem_term() function on all terms in its term list.
    Warning: The result is NOT saved in the document's term list, but in the extra field stemmed_terms!
    :param collection: Document collection to process
    """
    # TODO: Implement this function. (PR03)
    # raise NotImplementedError('This function was not implemented yet.')


def stem_query_terms(query: str) -> str:
    """
    Stems all terms in the provided query string.
    :param query: User query, may contain Boolean operators and spaces.
    :return: Query with stemmed terms
    """
    # TODO: Implement this function. (PR03)
   # raise NotImplementedError('This function was not implemented yet.')
