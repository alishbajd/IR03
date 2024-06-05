# Contains a unified class definition for a document.

class Document(object):
    def __init__(self):
        self.document_id = None  # Unique document ID
        self.title = ''  # Title of document
        self.raw_text = ''  # Holds complete text of document.
        self.terms = []  # Holds all terms.
        self.filtered_terms = []  # Holds terms without stopwords.
        self.stemmed_terms = []  # Holds terms that were stemmed with Porter algorithm. (Only relevant in PR03!)
        # Note: See PR02 task description for instructions regarding these properties.


    def __str__(self):
        shortened_content = self.raw_text[:10] + "..." if len(self.raw_text) > 10 else self.raw_text
        return 'D' + str(self.document_id).zfill(2) + ': ' + self.title + '("' + shortened_content + '")'
