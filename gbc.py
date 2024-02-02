#pylint: disable=R0903:too-few-public-methods
#pylint: disable=C0114:missing-module-docstring
#pylint: disable=C0304:missing-final-newline
#pylint: disable=C0115:missing-class-docstring
#pylint: disable=C0303:trailing-whitespace


from typing import List
from document_service import DocumentService,Document



class GroupByClassModel:
    '''
    Implementation of  the Group By Class Machine Learning Algorithms
    Features include model training,text classification,incremental learning, key word extraction
    '''
    def __init__(self,name,increment_learning=True):
        '''
        Instantiate GBC Model:

        *By default incremental learning is set to True.
        '''
        self.increment_learning=increment_learning
        self.model_trained=False
        self.ds:DocumentService=DocumentService()
        self.name = name
        self.categories = []
        self.number_of_documents=0
        self.class_vectors={}

    def _categorylist(self,documents:List[Document]):
        all_categories = self.categories
        for document in documents:
            all_categories.extend(document.categories)
        unique_categories = list(set(all_categories))
        self.categories=unique_categories

    def train(self,json_data):
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

    def _update_existing_model(self,json_data):
        print("updating existing model")
        documents:List[Document]=self.ds.json_to_documents(json_data)
        self.number_of_documents=len(documents)
        self._categorylist(documents)
        self.model_trained=True

    def _train_new_model(self,json_data):
        print("training new model")
        documents:List[Document]=self.ds.json_to_term_vectors(json_data)
        print(documents[0].term_vector)
        print(documents[1].term_vector)
        self.number_of_documents=len(documents)
        self._categorylist(documents)
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

class GBCTrainModel:

    def __init__(self,model:GroupByClassModel):
        self.model=model

    def _initialize_class_vectors(self):
        for category in self.model.categories:
            self.model.class_vectors[category]={}
    
    def _populate_class_vectors(self):
        for category in self.model.categories:
            self.model.class_vectors[category]={}