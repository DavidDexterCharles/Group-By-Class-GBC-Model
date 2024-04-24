# pylint: disable=C0115:missing-class-docstring,C0114:missing-module-docstring
# pylint: disable=C0301:line-too-long
# pylint: disable=W0707:raise-missing-from
from pymongo import MongoClient
from fastapi import APIRouter, Depends, HTTPException
from app.api.pydanticmodels import Article
from app.services.gbc import GroupByClassModel

import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from keras import datasets,layers,models
router = APIRouter()

# Define your MongoDB connection URL
# mongodb+srv://gbcuser:<password>@gbc.vny6qh7.mongodb.net/?retryWrites=true&w=majority&appName=gbc
MONGO_URI = "mongodb+srv://gbcuser:gbcuser@gbc.vny6qh7.mongodb.net/?retryWrites=true&w=majority&appName=gbc"

# Dependency function to create MongoDB client
def get_mongo_client():
    '''
    get_mongo_client
    '''
    client = MongoClient(MONGO_URI)
    yield client
    client.close()

@router.get("/cnn")
def cnn():
    '''
    returns category
    '''

    (training_images,training_labels),(testing_images,testing_labels)=datasets.cifar10.load_data()
    training_images,testing_images=training_images/255,testing_images/255
    class_names=['Plane','Car','Bird','Cat','Deer','Dog','Frog','Horse','Ship','Truck']

    for i in range(16):
        plt.subplot(4,4,i+1)
        plt.xticks([])
        plt.yticks([])
        plt.imshow(training_images[i],cmap=plt.cm.binary)
        plt.xlabel(class_names[training_labels[i][0]])
    
    plt.show()

    return "CNN VIEW"