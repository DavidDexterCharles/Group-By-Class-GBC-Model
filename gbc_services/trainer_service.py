#pylint: disable=R0903:too-few-public-methods
#pylint: disable=C0114:missing-module-docstring
#pylint: disable=C0304:missing-final-newline
#pylint: disable=C0115:missing-class-docstring
#pylint: disable=C0303:trailing-whitespace
#pylint: disable=C0301:line-too-long

from collections import Counter
from typing import List

from .document_service import Document

class TrainerService:

    def __init__(self,class_vectors,_unique_class_averages,documents:List[Document],allow_new_labels,categories=None):
        '''
        ..
        '''
        self.class_vectors=class_vectors
        self.unique_class_averages=_unique_class_averages
        self.documents=documents
        self.categories=categories
        self.allow_new_labels=allow_new_labels
       
       

    def _get_valid_categories(self,current_categories,allowed_categories):
        '''
        returns the categories that are in both
        current_categories and allowed_categories.
        By doing this only relevant class vectors
        are updated. Example if a model has 100 class
        vectors and the new document is only related
        to 2 out of the 100 (i.e. has category labels matching only 2 class vectors), then only the related class vectors get updated without having to traverse the other 98 class vectors
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
        if self.categories is not None:
            for category in self.categories:
                self.class_vectors[category]=Counter()
                self.unique_class_averages[category]=0
        
    
    def populate_class_vectors(self):
        '''
        populate_class_vectors
        '''
        all_categories = []
        for document in self.documents:
            all_categories.extend(document.categories)
            valid_categories=self._get_valid_categories(document.categories,self.categories)
            for category in valid_categories:
                if category in self.class_vectors:
                    self.class_vectors[category]+=document.term_vector
                else:
                    self.class_vectors[category]=document.term_vector
        unique_categories = self._get_valid_categories(all_categories,self.categories)
        
        if unique_categories is None:
            raise ValueError("The category list is empty. Cannot perform the operation.")
        
        self.categories=unique_categories

    def standardize_class_vectors(self,valid_categories=None):
        '''
        standardize_class_vectors
        '''
        if valid_categories is None:
            valid_categories=self.categories

        for category in valid_categories:
            class_vector=self.class_vectors[category]
            unique_weights = set(class_vector.values())
            unique_class_average = sum(unique_weights) / len(unique_weights)
            self.unique_class_averages[category]=unique_class_average
            for term in class_vector:
                class_vector[term] = round(class_vector[term] / unique_class_average,2)
    
    def get_valid_doc_labels(self,document_categories):
        '''
        Used For Incemental learning
        self.categories and returns valid list of 
        category labels based on whether allow_new_labels
        is true
        '''
        if self.allow_new_labels:
            self.categories+=document_categories
            self.categories=list(set(self.categories))
        valid_categories=self._get_valid_categories(document_categories,self.categories)
        return valid_categories

    def destandardize_class_vectors(self,valid_categories:List):
        '''
        Used For Incemental learning
        destandardize_class_vectors
        '''
        for category in valid_categories:
            if category not in self.class_vectors:
                #if category from valid_categories list does not 
                #have a corresponding class_vector in the set of 
                #class_vectors then create new class vector 
                self.class_vectors[category]=Counter()
                self.unique_class_averages[category]=0
            class_vector=self.class_vectors[category]
            unique_class_average=self.unique_class_averages[category]
            for term in class_vector:
                class_vector[term] = round(class_vector[term] * unique_class_average,1)
    
    def merge_classvector_with_termvector(self,valid_categories:List,document_term_vector:Counter):
        '''
        Used For Incemental learning
        merge_classvector_with_termvector
        '''
        for category in valid_categories:
            self.class_vectors[category]+=document_term_vector
            self.unique_class_averages[category]=0
    
    def re_standardize_class_vectors(self,valid_categories:List):
        '''
        Used For Incemental learning
        re_standardize_class_vectors
        '''
        self.standardize_class_vectors(valid_categories)
   

    def categorylist(self):
        '''
        If categories were explicitly specified , then only the specified
        labels will be used in training the model, otherwise the categorylist
        would be dynamicaly generated based on the categories associated with
        each document in the training set
        '''
        all_categories = []
        for document in self.documents:
            all_categories.extend(document.categories)
            valid_categories=self._get_valid_categories(document.categories,self.categories)
            for category in valid_categories:
                if category in self.class_vectors:
                    self.class_vectors[category]+=document.term_vector
                else:
                    self.class_vectors[category]=document.term_vector
        unique_categories = self._get_valid_categories(all_categories,self.categories)
        
        if unique_categories is None:
            raise ValueError("The category list is empty. Cannot perform the operation.")
        
        return unique_categories