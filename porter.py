# Contains all functions related to the porter stemming algorithm.

from document import Document


def get_measure(term: str) -> int:
    """
    Returns the measure m of a given term [C](VC){m}[V].
    :param term: Given term/word
    :return: Measure value m
    """
    # TODO: Implement this function. (PR03)
    m = 0
    i = 0
    while i < len(term):
        if not condition_d(term):
            break
        i += 1
    while i < len(term):
        if condition_v(term):
            break
        i += 1
        m += 1
    while i < len(term):
        if cond_o(term):
            break
        i += 1
    return m
  


def condition_v(stem: str) -> bool:
    """
    Returns whether condition *v* is true for a given stem (= the stem contains a vowel).
    :param stem: Word stem to check
    :return: True if the condition *v* holds
    """
    # TODO: Implement this function. (PR03)

    condition = False

    vowels = 'aeiou'
    for i in range(0,len(stem)):

        if stem[i] in vowels:
            condition = True
            

    
    return condition




def condition_d(stem: str) -> bool:
    """
    Returns whether condition *d is true for a given stem (= the stem ends with a double consonant (e.g. -TT, -SS)).
    :param stem: Word stem to check
    :return: True if the condition *d holds
    """
    # TODO: Implement this function. (PR03)

    check = False

    double_consonants = ["bb","cc", "dd", "ff", "gg","hh","jj","kk","ll", "mm", "nn", "pp", "qq","rr","ss", "tt","vv","ww","xx","yy","zz"]

    if len(stem) >= 2 and stem[-2:] in double_consonants:
            check = True
            
    return check

def cond_o(stem: str) -> bool:
    """
    Returns whether condition *o is true for a given stem (= the stem ends cvc, where the second c is not W, X or Y
    (e.g. -WIL, -HOP)).
    :param stem: Word stem to check
    :return: True if the condition *o holds
    """
    check = False
    if len(stem) >= 3:
        if (stem[-1] not in 'aeiouwxy' and
            stem[-2] in 'aeiou' and
            stem[-3] not in 'aeiou'):
            check = True
    return check


def remove_stem(word,remove,replace,func=None):

    stemmed_term = word

    if word.endswith(remove):
        stemmed_term = word[:-len(remove)]
        if replace is not None and func is None or func:
            stemmed_term+=replace

    return stemmed_term



def stem_term(term: str) -> str:
    """
    Stems a given term of the English language using the Porter stemming algorithm.
    :param term:
    :return:
    """
    # TODO: Implement this function. (PR03)
    # Note: See the provided file "porter.txt" for information on how to implement it!
    
    term = term.lower()
    term = step1a(term)    
    term = step1b(term)   
    term = step1c(term)  

    term = step2(term)

    term = step3(term)

    term = step4(term)  

    term = step5a(term)
    term = step5b(term)
   
    return term

def step1a(word):

    word = remove_stem(word, 'sses','ss')
    word = remove_stem(word,'ies','i')
    word = remove_stem(word,'ss','s')
    word = remove_stem(word,'s',None)

    return word

def step1b(word):

    if word.endswith('eed'):
        if get_measure(word[:-3]) > 0:
            word = word[:-1]

    if word.endswith('ied'):
         
        if len(word) == 4:
            word = remove_stem(word, 'ied','ie')
        else:
            word = remove_stem(word,'ied','i')

    else:   
        if len(word)>1 and condition_v(word[:-2]) and word.endswith('ed'):
            word = word[:-2]

        elif len(word)>2 and condition_v(word[:-3]) and word.endswith('ing'):
            word = word[:-3]
  
    word = remove_stem(word, 'at', 'ate')
    word = remove_stem(word, 'bl', 'ble')
    word = remove_stem(word, 'iz', 'ize')

    return word

def step1c(word):

    if word.endswith('y') and condition_v(word[:-1]):
        word = word[:-1] + 'i'
    return word
         
def step2(word):

    check = False

    suffixes = {
        'ational': 'ate', 'tional': 'tion', 'enci': 'ence', 'anci': 'ance',
        'izer': 'ize', 'abli': 'able', 'alli': 'al', 'entli': 'ent',
        'eli': 'e', 'ousli': 'ous', 'ization': 'ize', 'ation': 'ate',
        'ator': 'ate', 'alism': 'al', 'iveness': 'ive', 'fulness': 'ful',
        'ousness': 'ous', 'aliti': 'al', 'iviti': 'ive', 'biliti': 'ble','XFLURTI':'XTI'
    }

    if get_measure(word) > 0:
        check = True


    for suffix, replacement in suffixes.items():
        word = remove_stem(word, suffix, replacement, check)
    return word


def step3(word):

    check = False

    suffixes = {
        'icate': 'ic', 'ative': '', 'alize': 'al', 'iciti': 'ic',
        'ical': 'ic', 'ful': '', 'ness': ''
    }

    if get_measure(word) > 0:
        check = True

    for suffix, replacement in suffixes.items():
        word = remove_stem(word, suffix, replacement, check)
    return word

def step4(word):

    check = False

    suffixes = [
        'al', 'ance', 'ence', 'er', 'ic', 'able', 'ible', 'ant', 'ement',
        'ment', 'ent', 'ou', 'ism', 'ate', 'iti', 'ous', 'ive', 'ize'
    ]

    if get_measure(word) > 1:
        check = True

    for suffix in suffixes:
        word = remove_stem(word, suffix, '',check)
    if word.endswith('ion') and get_measure(word[:-3]) > 1 and word[-4] in 'st':
        word = word[:-3]
    return word

def step5a(word):

    if word.endswith('e'):
        a = get_measure(word[:-1])
        if a > 1 or (a == 1 and not cond_o(word[:-1])):
            word = word[:-1]
    return word


def step5b(word):

    if get_measure(word) > 1 and condition_d(word) and word.endswith('l'):
        word = word[:-1]
    return word


def stem_all_documents(collection: list[Document]):
    """
    For each document in the given collection, this method uses the stem_term() function on all terms in its term list.
    Warning: The result is NOT saved in the document's term list, but in the extra field stemmed_terms!
    :param collection: Document collection to process
    """
    # TODO: Implement this function. (PR03)


    for document in collection:
        stemmed_terms = [stem_term(term) for term in document.terms]
        document.stemmed_terms = stemmed_terms

    return collection


def stem_query_terms(query: str) -> str:
    """
    Stems all terms in the provided query string.
    :param query: User query, may contain Boolean operators and spaces.
    :return: Query with stemmed terms
    """
    # TODO: Implement this function. (PR03)

    stemmed_term = stem_term(query)

    return stemmed_term 

  


