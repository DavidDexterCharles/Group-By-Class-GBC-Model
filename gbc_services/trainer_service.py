#pylint: disable=R0903:too-few-public-methods
#pylint: disable=C0114:missing-module-docstring
#pylint: disable=C0304:missing-final-newline
#pylint: disable=C0115:missing-class-docstring
#pylint: disable=C0303:trailing-whitespace

from collections import Counter
from typing import List

from .document_service import Document

class TrainerService:

    def __init__(self,class_vectors,documents:List[Document],categories=None):
        '''
        ..
        '''
        self._class_vectors=class_vectors
        self._documents=documents
        self._categories=categories
        if categories is None:
            self._categories_specified=False
        else:
            self._categories_specified=True

    def _intersect_list(self,current_categories,allowed_categories):
        '''
        returns the categories that are in both
        current_categories and allowed_categories
        '''
        if allowed_categories is None:
            return list(set(current_categories)) #remove any duplicates
        
        current_categories_set =set(current_categories)
        allowed_categories_set = set(allowed_categories)
        result_set = allowed_categories_set.intersection(current_categories_set)

        return list(result_set)
    
    def initialize_class_vectors(self):
        '''
        ..
        '''
        # print(self._categories)
        if self._categories is not None:
            for category in self._categories:
                self._class_vectors[category]=Counter()
        
    
    def populate_class_vectors(self):
        '''
        populate_class_vectors
        '''
        # print(self._class_vectors)
        all_categories = []
        for document in self._documents:
            all_categories.extend(document.categories)
            valid_labels=self._intersect_list(document.categories,self._categories)
            # print(valid_labels)
            for category in valid_labels:
                # print(category)
                if category in self._class_vectors:
                    self._class_vectors[category]+=document.term_vector
                else:
                    self._class_vectors[category]=document.term_vector
        unique_categories = self._intersect_list(all_categories,self._categories)
        
        if unique_categories is None:
            raise ValueError("The category list is empty. Cannot perform the operation.")

    def standardize_class_vectors(self):
        '''
        standardize_class_vectors
        '''
        

    def update_class_vectors(self):
        '''
        update_class_vectors
        '''
        

    # def _incremntal_learn_class_vectors(self):
    #     self._update_class_vectors()

   

    def categorylist(self):
        '''
        If categories were explicitly specified , then only the specified
        labels will be used in training the model, otherwise the categorylist
        would be dynamicaly generated based on the categories associated with
        each document in the training set
        '''
        all_categories = []
        for document in self._documents:
            all_categories.extend(document.categories)
            valid_labels=self._intersect_list(document.categories,self._categories)
            for category in valid_labels:
                if category in self._class_vectors:
                    self._class_vectors[category]+=document.term_vector
                else:
                    self._class_vectors[category]=document.term_vector
        unique_categories = self._intersect_list(all_categories,self._categories)
        
        if unique_categories is None:
            raise ValueError("The category list is empty. Cannot perform the operation.")
        
        return unique_categories