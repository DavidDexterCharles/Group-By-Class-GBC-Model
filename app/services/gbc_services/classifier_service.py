#pylint: disable=R0903:too-few-public-methods
#pylint: disable=C0114:missing-module-docstring
#pylint: disable=C0304:missing-final-newline
#pylint: disable=C0115:missing-class-docstring
#pylint: disable=C0303:trailing-whitespace
#pylint: disable=C0301:line-too-long

from typing import List
from .document_service import DocumentService


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
    def __init__(self,model_class_vectors,model_categories,combined_classterm_weights):
        self.model_class_vectors=model_class_vectors
        self.model_categories:List=model_categories
        self.ds:DocumentService=DocumentService()
        self.combined_classterm_weights=combined_classterm_weights
    
    def get_max_category(self,classification:dict):
        '''
        ## Return the category with the highest value:
        
        e.g.
        {'malignant': 1.0, 'benign': 4.0}
        When you call get_max_category(classification), 
        it will return the string ('malignant', 'benign', etc.)
        with the highest value in the classification dictionary
        '''
        max_category = max(classification, key=classification.get)
        return max_category

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
                for key in matching_terms:
                    if self.combined_classterm_weights[key] != 0:
                        related_vector[key] = mcv[key] / self.combined_classterm_weights[key]
                    else:
                        # Handle division by zero gracefully, for example, by setting a default value
                        related_vector[key] = 0  # or any other appropriate action
                    # related_vector[key]=mcv[key]/self.combined_classterm_weights[key] #Penalize the Related Class Vectors using combined_classterm_weights

                dot_product = sum(query_vector.get(key, 0) * related_vector.get(key, 0) for key in set(query_vector) & set(related_vector))
                related_terms[category]=related_vector
                related_vectors[category]=round(dot_product,3)

        print("\n\n")
        print(f"query_vector {query_vector}")
        print(f"related_terms {related_terms}")
        print(f"related_vectors {related_vectors}")
        return related_vectors
