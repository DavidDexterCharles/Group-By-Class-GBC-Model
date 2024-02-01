#pylint: disable=R0903:too-few-public-methods
#pylint: disable=C0114:missing-module-docstring
#pylint: disable=C0304:missing-final-newline
#pylint: disable=C0115:missing-class-docstring


from typing import List
from document_service import DocumentService,Document

class GroupByClassModel:
    '''
    Implementation of  the Group By Class Machine Learning Algorithms
    Features include model training,text classification,incremental learning, key word extraction
    '''
    def __init__(self,name):
        self.model_trained=False
        self.ds:DocumentService=DocumentService()
        self.name = name
        self.categories = []
        self.number_of_documents=0

    def _categorylist(self,documents):
        all_categories = []
        for document in documents:
            all_categories.extend(document.categories)
        unique_categories = list(set(all_categories))
        self.categories=unique_categories

    def train(self,json_data):
        '''
        trains model, stores number of documents
        '''
        if self.model_trained:
            print("model already trained")
            return
        documents:List[Document]=self.ds.json_to_documents(json_data)
        self.number_of_documents=len(documents)
        self._categorylist(documents)

    def get_number_of_documents(self):
        '''
        returns number of docs used to train model
        '''
        return self.number_of_documents

    def get_categories(self,doprint=False):
        '''
        returns the list of categories/labels
        the model contains
        '''
        c=self.categories
        if doprint:
            print(c)
        return c

    def print_model_name(self):
        '''
        prints the name of the current model instance
        '''
        print(self.name)