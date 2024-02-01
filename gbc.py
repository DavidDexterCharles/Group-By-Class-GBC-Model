#pylint: disable=R0903:too-few-public-methods
#pylint: disable=C0114:missing-module-docstring
#pylint: disable=C0304:missing-final-newline
#pylint: disable=C0115:missing-class-docstring


from typing import List
from document_service import DocumentService,Document

class GroupByClassTrain:
    '''
    Implementation of  the Group By Class Machine Learning Algorithms
    Features include model training,text classification,incremental learning, key word extraction
    '''
    def __init__(self,name):
        self.document_service:DocumentService=DocumentService()
        self.name = name
        self.labels = []
        self.number_of_documents=0

    def train(self,json_data):
        '''
        trains model, stores number of documents
        '''
        documents:List[Document]=self.document_service.json_to_documents(json_data)
        # print(d[0].content)
        self.number_of_documents=len(documents)
        print(self.number_of_documents)

    def print_model_name(self):
        '''
        prints the name of the current model instance
        '''
        print(self.name)