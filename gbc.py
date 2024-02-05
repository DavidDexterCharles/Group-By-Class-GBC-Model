#pylint: disable=R0903:too-few-public-methods
#pylint: disable=C0114:missing-module-docstring
#pylint: disable=C0304:missing-final-newline
#pylint: disable=C0115:missing-class-docstring
#pylint: disable=C0303:trailing-whitespace

from typing import List
from gbc_services.document_service import DocumentService,Document
from gbc_services.trainer_service import TrainerService


class GBCModel:
    def __init__(self):
        self.class_vectors={}


class GroupByClassModel:
    '''
    Implementation of  the Group By Class Machine Learning Algorithms
    Features include model training,text classification,incremental learning, key word extraction
    '''
    def __init__(self,name,categories=None,increment_learning=True):
        '''
        Instantiate GBC Model:

        *By default incremental learning is set to True.
        '''
        self.class_vectors={}
        self.categories = categories
        self.unique_class_average=0
        
        self.increment_learning=increment_learning
        self.model_trained=False
        self.ds:DocumentService=DocumentService()
        self.name = name
        
        self.number_of_documents=0
        self.documents:List[Document]=[]

    def _categorylist(self,documents:List[Document]):
        # all_categories=[]
        # if self.categories is not None:
        #     all_categories = self.categories
        # for document in documents:
        #     all_categories.extend(document.categories)
        # unique_categories = list(set(all_categories))

        # if unique_categories is None:
        #     raise ValueError("The category list is empty. Cannot perform the operation.")
        
        # return unique_categories

        ts=TrainerService(self.class_vectors,self.documents,['Category C', 'Category F'])
        self.categories=ts.categorylist()
        print(ts._class_vectors)

        return self.categories

    def train3(self,json_data):
        '''
        Trains GBC Model:

        *By default incremental learning is done.
        
        If model not already trained then create new model(generate new class vectors).

        If model already trained and increment_learning is True
        then do increment learning algorithm on existing model
        (update existing class vectors)
        '''

        if self.model_trained:
            if self.increment_learning:
                self._update_existing_model(json_data)
            else:
                print("model already trained")
        else:
            self._train_new_model(json_data)
        
        # self.train2(json_data)
    
    def train(self,json_data):
        '''
        train model
        '''
        self.documents=self.ds.json_to_doc(json_data)

        # if self.categories is None:
        #     self.categories=self._categorylist(self.documents)

        ts=TrainerService(self.class_vectors,self.documents,self.categories)
        
        ts.initialize_class_vectors()
        ts.populate_class_vectors()
        print(self.class_vectors)


    def _update_existing_model(self,json_data):
        print("updating existing model")
        self.documents=self.ds.json_to_doc(json_data)
        self.number_of_documents=len(self.documents)
        self.categories=self._categorylist(self.documents)
        self.model_trained=True

    def _train_new_model(self,json_data):
        print("training new model")
        self.documents=self.ds.json_to_doc(json_data)
        print(self.documents[0].term_vector)
        print(self.documents[1].term_vector)
        print(self.documents[2].term_vector)
        print(self.documents[3].term_vector)
        print("\n")
        self.number_of_documents=len(self.documents)
        self.categories=self._categorylist(self.documents)
        self.model_trained=True


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