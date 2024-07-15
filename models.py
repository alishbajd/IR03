# Contains all retrieval models.

from abc import ABC, abstractmethod

from document import Document
from cleanup import remove_stop_words_from_term_list
import re 
import os
import extraction
import porter
from collections.abc import Iterable



RAW_DATA_PATH = 'raw_data'
DATA_PATH = 'data'
COLLECTION_PATH = os.path.join(DATA_PATH, 'my_collection.json')

class RetrievalModel(ABC):
    @abstractmethod
    def document_to_representation(self, document: Document, stopword_filtering=False, stemming=False):
        """
        Converts a document into its model-specific representation.
        This is an abstract method and not meant to be edited. Implement it in the subclasses!
        :param document: Document object to be represented
        :param stopword_filtering: Controls, whether the document should first be freed of stopwords
        :param stemming: Controls, whether stemming is used on the document's terms
        :return: A representation of the document. Data type and content depend on the implemented model.
        """
        
        pass

    @abstractmethod
    def query_to_representation(self, query: str):
        """
        Determines the representation of a query according to the model's concept.
        :param query: Search query of the user
        :return: Query representation in whatever data type or format is required by the model.
        """
        pass

    @abstractmethod
    def match(self, document_representation, query_representation) -> float:
        """
        Matches the query and document presentation according to the model's concept.
        :param document_representation: Data that describes one document
        :param query_representation:  Data that describes a query
        :return: Numerical approximation of the similarity between the query and document representation. Higher is
        "more relevant", lower is "less relevant".
        """
        pass


class LinearBooleanModel(RetrievalModel):
    # TODO: Implement all abstract methods and __init__() in this class. (PR02)
    def __init__(self):
      pass
      

    def __str__(self):
        return 'Boolean Model (Linear)'
    
    def document_to_representation(self, document,  stop_word_filtering= False,stemming = False):
        term_list = document.terms
        represented_document = []
        if stop_word_filtering:
            represented_document = remove_stop_words_from_term_list(term_list)
        
        else:
            represented_document = term_list
        return represented_document

    def query_to_representation(self, query: str):

        query = query.lower()

        return query
    
    def match(self, document_representation, query_representation) -> float:
        score = 0

        for doc in document_representation:
       
            if query_representation == doc.lower():
                
                score = 100
        
        return score
                

class InvertedListBooleanModel(RetrievalModel):
    # TODO: Implement all abstract methods and __init__() in this class. (PR03)
    def __init__(self):
       pass



    def __str__(self):
        return 'Boolean Model (Inverted List)'

    def query_to_representation(self, query: str):
        
        seperate = []

        query_list = {}

        tokens = re.findall(r'\(|\)|\w+|[-&|]', query)

        c = 0

        for letter in tokens:
            if letter =='&' or letter =='|' or letter == '-' or letter == '(' or letter == ')':
                seperate.append(letter)

            else:
                stemmed_term = porter.stem_query_terms(letter)
                query_list[c] = {stemmed_term:[]}
                
                c+=1
              
        return (query_list,tokens)
    


    def document_to_representation(self, document: Document, stopword_filtering=False, stemming=False):

        if stopword_filtering:
            if isinstance(document, Iterable):
       
                for d in document:
                    d.terms = remove_stop_words_from_term_list(d.terms)       

      
        inverted_list = {}

        if stemming:
            document = porter.stem_all_documents(document)
     
            for d in document:
                for term in d.stemmed_terms:
                    if term not in inverted_list:
                        inverted_list[term] = []
                        inverted_list[term].append(d.document_id)
                    else:
                        if d.document_id not in inverted_list[term]:
                            inverted_list[term].append(d.document_id)

        
        else:
            if isinstance(document, Iterable):
                for d in document:
                    for term in d.terms:
                        term = term.lower()
                        if term not in inverted_list:                            
                            inverted_list[term] = []
                            inverted_list[term].append(d.document_id)
                        else:
                            if d.document_id not in inverted_list[term]:
                                inverted_list[term].append(d.document_id)               
        
        return inverted_list


    def match(self, document_representation, query_representation) -> float:
        """ Matches the query and document presentation according to the model's concept.
        :param document_representation: Data that describes one document
        :param query_representation:  Data that describes a query
        :return: Numerical approximation of the similarity between the query and document representation. Higher is
        "more relevant", lower is "less relevant".
        """

   
        query = query_representation[0]
        tokens = query_representation[1]

        query_term_dict = {}

        for i in tokens:
            if i in  document_representation.keys():
                query_term_dict[i]=document_representation[i]

                   
        resultant = []
        
        if '|' not in tokens and '&' not in tokens and '(' not in tokens and ')' not in tokens and '-' not in tokens:
            for i in tokens:
                resultant = document_representation[i]   
        else: 


            for i in range(0,len(tokens)):

                if tokens[i]=='&':
                    try:
                        l1 = query_term_dict[tokens[i-1]]     

                    except:
                        l1=[]
                    try:        
                        l2 = query_term_dict[tokens[i+1]]
                    except:
                        l2=[]

                    docs_list = self.and_operation(l1,l2)

                    resultant.extend(docs_list)

                if tokens[i] == '|':
                    try:
                        l1 = query_term_dict[tokens[i-1]]     

                    except:
                        l1=[]
                    try:        
                        l2 = query_term_dict[tokens[i+1]]
                    except:
                        l2=[]

                    docs_list = self.or_operation(l1,l2)

                    resultant.extend(docs_list)
                if tokens[i] == '-':
                    if tokens[i+1] != '(':
                        try:                        
                            l1 = query_term_dict[tokens[i+1]]
                        except:
                            l1=[]
                        docs_list = self.negative_operation(l1)
                        resultant.extend(docs_list)
                    else:
                            try:                        
                                l1 = query_term_dict[tokens[i+2]]
                            except:
                                l1=[]
                                docs_list = self.negative_operation(l1)
                                resultant.extend(docs_list)
                if tokens[i] == '(':
                    while tokens[i]!=')':
                        if tokens[i]=='&':

                            try:                        
                                l1 = query_term_dict[tokens[i+1]]
                            except:
                                l1=[] 
                            try:                        
                                l2 = query_term_dict[tokens[i-1]]
                            except:
                                l2=[]
                            docs_list = self.and_operation(l1,l2)
                            resultant.extend(docs_list)

                        if tokens[i] == '|':
                            try:                        
                                l1 = query_term_dict[tokens[i-1]]
                            except:
                                l1=[]    
                            try:                        
                                l2 = query_term_dict[tokens[i+1]]
                            except:
                                l2=[]
                            docs_list = self.or_operation(l1,l2)
                            resultant.extend(docs_list)
                        if tokens[i] == '-':
                            if tokens[i+1] != '(':
                                try:                        
                                    l1 = query_term_dict[tokens[i+1]]
                                except:
                                    l1=[]
                                docs_list = self.negative_operation(l1)
                                resultant.extend(docs_list)
                        else:
                            try:                        
                                l1 = query_term_dict[tokens[i+2]]
                            except:
                                l1=[]
                                docs_list = self.negative_operation(l1)
                                resultant.extend(docs_list)

                        i+=1

   
        result = (query_term_dict,set(resultant))

        return result

    def and_operation(self,l1,l2):
      
        intersection = list(set(l1) & set(l2))   


        return intersection

    def or_operation (self,l1,l2):
        union = list(set(l1) | set(l2))
        return union
    
    def negative_operation(self,l1):
        negative = []

        for i in range(1,82):
            if i not in l1:
                negative.append(i)
        
        return negative
        
               


class SignatureBasedBooleanModel(RetrievalModel):
    # TODO: Implement all abstract methods. (PR04)
    def __init__(self):
        raise NotImplementedError()  # TODO: Remove this line and implement the function.

    def __str__(self):
        return 'Boolean Model (Signatures)'


class VectorSpaceModel(RetrievalModel):
    # TODO: Implement all abstract methods. (PR04)
    def __init__(self):
        raise NotImplementedError()  # TODO: Remove this line and implement the function.

    def __str__(self):
        return 'Vector Space Model'


class FuzzySetModel(RetrievalModel):
    # TODO: Implement all abstract methods. (PR04)
    def __init__(self):
        raise NotImplementedError()  # TODO: Remove this line and implement the function.

    def __str__(self):
        return 'Fuzzy Set Model'


i = InvertedListBooleanModel()

d = Document()

i.document_to_representation(d)

# print(i.query_to_representation('fox&wolf'))
# print(i.query_to_representation('fox|wolf'))
# print(i.query_to_representation('-wolf'))
# print(i.query_to_representation('(fox&dog)|(quick&lazy)'))