#pylint: disable=R0903:too-few-public-methods
#pylint: disable=C0114:missing-module-docstring
#pylint: disable=C0304:missing-final-newline
#pylint: disable=C0115:missing-class-docstring
#pylint: disable=C0303:trailing-whitespace
#pylint: disable=C0301:line-too-long

from typing import Dict, List
import uuid
from .gbc_services.document_service import DocumentService,Document
from .gbc_services.trainer_service import TrainerService
from .gbc_services.classifier_service import ClassifierService

class GroupByClassModel:
    '''
    Implementation of  the Group By Class Machine Learning Algorithms
    Features include model training,text classification,incremental learning, key word extraction
    '''
    def __init__(self,name,categories:List=None,increment_learning=True):
        '''
        Instantiate GBC Model:

        *By default incremental learning is set to True.
        '''
        self.model_class_vectors:Dict={}
        self.model_unique_class_averages:Dict={}
        self.combined_classterm_weights:Dict={}
        self.model_categories:List = categories
        # self.unique_class_average=0
        if self.model_categories is None:
            self.allow_new_labels=True
        else:
            self.allow_new_labels=False
        
        self.increment_learning=increment_learning
        self.model_trained=False
        self.ds:DocumentService=DocumentService()
        self.name = f"{name}_{uuid.uuid4()}"
        
        self.number_of_documents=0

    def classify(self,data):
        '''
        classify
        '''
        cs = ClassifierService(self.model_class_vectors,self.model_categories,self.combined_classterm_weights)
        return cs.classify(data)
        
    def train(self,json_data):
        '''
        Trains GBC Model:

        *By default incremental learning is enabeled.
        
        If model not already trained then create new model(generate new class vectors).

        If model already trained and increment_learning is True
        then do increment learning algorithm on existing model
        (update existing class vectors)
        '''
        documents:List[Document]=self.ds.json_to_doc(json_data)
        self.number_of_documents+=len(documents)
        ts=TrainerService(self.model_class_vectors,self.model_unique_class_averages,documents,self.allow_new_labels,self.model_categories)

        if self.model_trained:
            if self.increment_learning:
                self._update_existing_model(ts)
            else:
                print("model already trained")
        else:
            self._train_new_model(ts)
        
        print(f"{self.model_class_vectors}\n")
        print(f"unique_class_averages:{self.model_unique_class_averages}\n")

    def _update_existing_model(self,ts:TrainerService):
        '''
        Incemental learning
        '''
        print("updating existing model")
        
        for document in ts.documents:
            valid_categories=ts.get_valid_doc_labels(document.categories)
            ts.destandardize_class_vectors(valid_categories)
            ts.merge_classvector_with_termvector(valid_categories,document.term_vector)
            # print(f"Destandardize:{ts.class_vectors}\n")
            ts.re_standardize_class_vectors(valid_categories)
            
            self.model_categories=ts.categories
            self.model_class_vectors=ts.class_vectors
            self.model_unique_class_averages=ts.unique_class_averages
            self.combined_classterm_weights=ts.combined_classterm_weights


    def _train_new_model(self,ts:TrainerService):
        '''
        Model Training
        '''
        print("training new model")
        ts.initialize_class_vectors()
        ts.populate_class_vectors()
        ts.standardize_class_vectors()
        self.model_categories=ts.categories
        self.model_class_vectors=ts.class_vectors
        self.model_unique_class_averages=ts.unique_class_averages
        self.model_trained=True
        self.combined_classterm_weights=ts.combined_classterm_weights


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
        c=self.model_categories
        if doprint:
            print(c)
        return c

    def print_model_name(self):
        '''
        prints the name of the current model instance
        '''
        print(self.name)