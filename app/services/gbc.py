#pylint: disable=R0903:too-few-public-methods
#pylint: disable=C0114:missing-module-docstring
#pylint: disable=C0304:missing-final-newline
#pylint: disable=C0115:missing-class-docstring
#pylint: disable=C0303:trailing-whitespace
#pylint: disable=C0301:line-too-long,W0612:unused-variable

from collections import Counter
from typing import Dict, List
import uuid
from app.services.gbc_services.document_service import DocumentService,Document
from app.services.gbc_services.trainer_service import TrainerService
from app.services.gbc_services.classifier_service import ClassifierService

class GBCmodel:
    categories:list
    class_vectors:dict
    combined_classterm_weights:dict
    unique_class_averages:dict

class GroupByClassModel:
    '''
    Implementation of  the Group By Class Machine Learning Algorithms
    Features include model training,text classification,incremental learning, key word extraction
    '''
    def __init__(self,name="",categories:List[str]=None,increment_learning=True,verbose=True,number_of_features=0):
        '''
        Instantiate GBC Model:

        *By default incremental learning is set to True.
        '''
        self.verbose=verbose
        self.number_of_features=number_of_features
        self.model_class_vectors:Dict={}
        self.model_unique_class_averages:Dict={}
        self.model_combined_classterm_weights:Dict={}
        self.model_categories:List = categories
        self.related_terms={}
        # self.unique_class_average=0
        if self.model_categories is None:
            self.allow_new_labels=True
        else:
            self.model_categories:List = [category.lower() for category in categories]
            self.allow_new_labels=False
        
        self.increment_learning=increment_learning
        self.model_trained=False
        self.ds:DocumentService=DocumentService()
        self.name = f"{name}_{uuid.uuid4()}"
        
        self.number_of_documents=0
        self.f1_score=0
        self.precision=0
        self.true_positive=0
        self.true_ngative=0
        self.false_positive=0
        self.false_ngative=0
        self.y_true=[]
        self.y_pred=[]

    def _set_f1_socre(self,outcome):
        '''
        TP = the number of instances that are correctly predicted as positive by the model
          and are actually positive according to the ground truth or the actual labels
        FP= the number of instances that are incorrectly predicted as positive by the model but
            are actually negative according to the ground truth or the actual labels
        FN=  the number of instances that are incorrectly predicted as negative by the model but 
            are actually positive according to the ground truth or the actual labels
        '''
        # TP

    def set_model(self,retrieved_model):
        '''
        use a model retrieved from persistence store
        '''
        self.name:str=retrieved_model["name"]
        self.number_of_documents:int=retrieved_model["number_of_documents"]
        if self.increment_learning:
            self.model_trained:bool=retrieved_model["trained"]
        else:
            self.model_trained:bool=False
        self.model_class_vectors=retrieved_model["class_vectors"]
        self.model_unique_class_averages:Dict=retrieved_model["unique_class_averages"]
        self.model_combined_classterm_weights:Dict=retrieved_model["combined_classterm_weights"]
        self.model_categories:List = retrieved_model["categories"]

    def get_model(self):
        '''
        get_model
        '''
        trained_model ={
        "name":self.name,
        "number_of_documents":self.number_of_documents,
        "trained":self.model_trained,
        "categories":self.model_categories,
        "class_vectors":self.model_class_vectors,
        "combined_classterm_weights":self.model_combined_classterm_weights,
        "unique_class_averages":self.model_unique_class_averages
        }
        if self.y_true and self.y_pred:
            trained_model["y_true"] =self.y_true
            trained_model["y_pred"] =self.y_pred

        return trained_model

    def classify(self,data):
        '''
        classify
        '''
        cs = ClassifierService(self.model_class_vectors,self.model_categories,self.model_combined_classterm_weights,self.verbose,self.number_of_features)
        result={}
        
        if isinstance(data, list):
            labeled_documents=data
            for index,document in enumerate(labeled_documents):
                result= cs.classify(document["content"])
                if document["categories"]:
                    self.y_true.append(document["categories"][0])
                else:
                    # self.y_true.append("none")
                    continue
                if result:
                    document["prediction"]=result
                    document["prediction_max"]=cs.get_max_category(result)
                    self.y_pred.append(document["prediction_max"])
                    # self._set_f1_socre(document[""])
                    # y_pred.append(result)
                else:
                    document["prediction"]=''
                    document["prediction_max"]=''
                    self.y_pred.append('')
        else:
            result= cs.classify(data)
            self.related_terms=cs.related_terms            
        
        return result


    def train(self,json_data,string_to_json=False):
        '''
        Trains GBC Model:

        *By default incremental learning is enabeled.
        
        If model not already trained then create new model(generate new class vectors).

        If model already trained and increment_learning is True
        then do increment learning algorithm on existing model
        (update existing class vectors)
        '''
        
        documents:List[Document]=self.ds.json_to_doc(json_data,string_to_json)
        self.number_of_documents+=len(documents)
        ts=TrainerService(self.model_class_vectors,self.model_unique_class_averages,documents,self.allow_new_labels,self.model_categories)

        if self.model_trained:
            if self.increment_learning:
                self._update_existing_model(ts)
            else:
                print("model already trained")
        else:
            self._train_new_model(ts)
        
        self.model_combined_classterm_weights={}#always full update the combined calss termweights
        for category in self.model_class_vectors:
            class_vector=self.model_class_vectors[category]
            for term in class_vector:
                term_weight=class_vector[term]
                if term in self.model_combined_classterm_weights:
                    self.model_combined_classterm_weights[term]+=term_weight
                else:
                    self.model_combined_classterm_weights[term]=term_weight
        if self.verbose:
            print(f"model_class_vectors: {self.model_class_vectors}\n")
            print(f"model_combined_classterm_weights: {self.model_combined_classterm_weights}\n")
            print(f"model_categories: {self.model_categories}\n")
            print(f"unique_class_averages:{self.model_unique_class_averages}\n")
            print(f"number_of_documents: {self.number_of_documents}\n")

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
        # self.model_combined_classterm_weights=ts.combined_classterm_weights


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
        # self.model_combined_classterm_weights=ts.combined_classterm_weights


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