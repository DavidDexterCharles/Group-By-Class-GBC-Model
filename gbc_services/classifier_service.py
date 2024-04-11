#pylint: disable=R0903:too-few-public-methods
#pylint: disable=C0114:missing-module-docstring
#pylint: disable=C0304:missing-final-newline
#pylint: disable=C0115:missing-class-docstring
#pylint: disable=C0303:trailing-whitespace
#pylint: disable=C0301:line-too-long

from typing import List
from gbc_services.document_service import DocumentService


class ClassifierService:
    '''
    The GBC Classification model calculates the similarity between two documents
    using the dot product (Inner Product) of their term vectors as per the vector space
    model. The result of a dot product calculation is a scalar value which represents how
    strongly related two documents are to each other.

    The steps for classifying a new document using the GBC Classification model are
    as follows:

    (1) Represent the new document as a query vector (the name given to the term vector of
        a document to be classified).

    (2) Find related class vectors, these are all class vectors that have a weight value
        for at least one of the terms present in the new document.

    (3) Penalize the related class vectors.

    (4) Predict the category of document by finding the dot product between the query
        vector and each of the penalized class vectors. The class vectors that gives the
        highest result is the category that best represents the query vector, and hence
        also the new document.
    '''
    def __init__(self,model_class_vectors,model_categories):
        self.model_class_vectors=model_class_vectors
        self.model_categories:List=model_categories
        self.ds:DocumentService=DocumentService()
    
    def classify(self,data):
        '''
        classify provided document by converting the data to a queryvector and finding dot product
        between it and its related class vectors
        '''
        query_vector=self.ds.term_vector(data)
        related_vectors={}
        related_terms={}
        for category in self.model_categories:
            mcv=self.model_class_vectors[category]
            matching_terms=set(mcv).intersection(set(query_vector))
            if matching_terms:
                related_vector = {key: mcv[key] for key in matching_terms}
                dot_product = sum(query_vector.get(key, 0) * related_vector.get(key, 0) for key in set(query_vector) & set(related_vector))
                related_terms[category]=related_vector
                related_vectors[category]=dot_product
        
        print(f"query_vector {query_vector}")
        print(f"related_terms {related_terms}")
        print(f"related_vectors {related_vectors}")
