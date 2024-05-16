# pylint: disable=C0115:missing-class-docstring,C0114:missing-module-docstring
# pylint: disable=C0301:line-too-long
# pylint: disable=W0707:raise-missing-from,C0304:missing-final-newline
# import json
from datetime import datetime,timezone
import json
import time
from typing import List, Optional
from pymongo import MongoClient
from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, Query,Request
from fastapi.encoders import ENCODERS_BY_TYPE
from app.api.pydanticmodels import Article, Article2
from app.services.gbc import GroupByClassModel
from app.api.endpoints.ml_models.model_metrics import ModelMetrics

ENCODERS_BY_TYPE[ObjectId] = str

router = APIRouter()
MONGO_URI = "mongodb+srv://gbcuser:gbcuser@gbc.vny6qh7.mongodb.net/?retryWrites=true&w=majority&appName=gbc"
def get_mongo_client():
    '''
    get_mongo_client
    '''
    client = MongoClient(MONGO_URI)
    yield client
    client.close()

@router.get("/api/articles", response_model=List[Article2])
def api_articles(page_number: int = Query(1, ge=1), page_size: int = Query(100, ge=1), mongo_client: MongoClient = Depends(get_mongo_client)):
    '''
    Get all articles with pagination
    '''
    db = mongo_client["gbc_db"]
    article_collection = db["article"]
    skip = (page_number - 1) * page_size
    result = article_collection.find().sort("insert_date", -1).skip(skip).limit(page_size)
    return list(result)

@router.get("/api/evaluate", response_model=List[Article2])
def api_evaluate(mongo_client: MongoClient = Depends(get_mongo_client)):
    '''
    Get all articles with pagination
    '''
    db = mongo_client["gbc_db"]
    article_collection = db["article"]
    page_number=1 #page1
    page_size=500 #500 articles per page
    skip = (page_number - 1) * page_size
    result = article_collection.find().sort("insert_date", -1).skip(skip).limit(page_size)
    result_list=list(result)
    mm= ModelMetrics()
    mm.api_svm(result_list)
    mm.api_svm_tfidf(result_list)
    mm.api_naive_bayes(result_list)
    mm.api_gbc(result_list)

    return result_list