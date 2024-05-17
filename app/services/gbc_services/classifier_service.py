#pylint: disable=R0903:too-few-public-methods
#pylint: disable=C0114:missing-module-docstring
#pylint: disable=C0304:missing-final-newline
#pylint: disable=C0115:missing-class-docstring
#pylint: disable=C0303:trailing-whitespace
#pylint: disable=C0301:line-too-long
from heapq import nlargest
import random
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
    def __init__(self,model_class_vectors,model_categories,combined_classterm_weights,verbose):
        self.verbose=verbose
        self.model_class_vectors=model_class_vectors
        self.model_categories:List=model_categories
        self.ds:DocumentService=DocumentService()
        self.combined_classterm_weights=combined_classterm_weights
        self.related_terms={}
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
            # mcv=self.balanced_sample(mcv,500)
            # mcv=self.get_top_n_pairs(mcv,500)
            mcv=self.get_top_n_pairs(mcv,int(len(query_vector)))
            matching_terms=set(mcv).intersection(set(query_vector))
            if matching_terms:
                related_vector = {key: mcv[key] for key in matching_terms}
                for key in matching_terms:
                    if self.combined_classterm_weights[key] != 0:
                        related_vector[key] = round(mcv[key] / self.combined_classterm_weights[key],3)
                    else:
                        # Handle division by zero gracefully, for example, by setting a default value
                        related_vector[key] = 0  # or any other appropriate action
                    # related_vector[key]=mcv[key]/self.combined_classterm_weights[key] #Penalize the Related Class Vectors using combined_classterm_weights
                
                # related_vector = self.balanced_sample(related_vector,50)
                # related_vector = self.get_top_n_pairs(related_vector,30)
                dot_product = sum(query_vector.get(key, 0) * related_vector.get(key, 0) for key in set(query_vector) & set(related_vector))
                related_terms[category]=related_vector
                related_vectors[category]=round(dot_product,3)

        self.related_terms=related_terms
        if self.verbose:
            print("\n\n")
            print(f"query_vector {query_vector}")
            print(f"related_terms {related_terms}")
            print(f"related_vectors {related_vectors}")
        
        return related_vectors
    
    def get_top_n_pairs(self,related_vector, n):
        """
        Extracts the top N key-value pairs from the given dictionary based on values.

        Args:
        related_vector (dict): The input dictionary.
        n (int): Number of top key-value pairs to extract.

        Returns:
        dict: A new dictionary containing the top N key-value pairs.
        """
        return dict(nlargest(n, related_vector.items(), key=lambda item: item[1]))
    
    def balanced_sample(self,dictionary, size):
        # Step 1: Sort the dictionary by values
        sorted_items = sorted(dictionary.items(), key=lambda item: item[1])
        
        # Step 2: Split the sorted list into low, middle, and top categories
        total_items = len(sorted_items)
        split_point_1 = total_items // 3
        split_point_2 = (2 * total_items) // 3
        
        low_category = sorted_items[:split_point_1]
        middle_category = sorted_items[split_point_1:split_point_2]
        top_category = sorted_items[split_point_2:]
        
        # Step 3: Determine the proportions for each category
        low_size = size // 3
        middle_size = size // 3
        top_size = size - low_size - middle_size
        
        # Step 4: Randomly sample the required number of elements from each category
        sampled_low = random.sample(low_category, min(low_size, len(low_category)))
        sampled_middle = random.sample(middle_category, min(middle_size, len(middle_category)))
        sampled_top = random.sample(top_category, min(top_size, len(top_category)))
        
        # Step 5: Combine the sampled elements
        sampled_dict = dict(sampled_low + sampled_middle + sampled_top)
        
        return sampled_dict