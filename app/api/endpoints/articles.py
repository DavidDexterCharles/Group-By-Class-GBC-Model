# pylint: disable=C0115:missing-class-docstring,C0114:missing-module-docstring
# pylint: disable=C0301:line-too-long
# pylint: disable=W0707:raise-missing-from
# import json
# import redis
import json
import time
from typing import List, Optional
from pymongo import MongoClient
from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, Query,Request
from fastapi.encoders import ENCODERS_BY_TYPE
from app.api.pydanticmodels import Article, Article2
from app.services.gbc import GroupByClassModel

ENCODERS_BY_TYPE[ObjectId] = str

router = APIRouter()

# https://youtu.be/VQnmcBnguPY?t=245
# accessing mongodb cluster

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


dummy_articles = [
    {
        "TITLE": "Article 1",
        "SOURCE": "http://example.com/article1",
        "CONTENT": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
        "articlecategories": {
            "category1": 20,
            "category2": 30,
            "category3": 50
        }
    },
    {
        "TITLE": "Article 2",
        "SOURCE": "http://example.com/article2",
        "CONTENT": "Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
        "articlecategories": {
            "category1": 10,
            "category2": 40,
            "category3": 50
        }
    },
    # Add more dummy articles as needed
]



@router.get("/article")
async def get_articles(page: Optional[int] = 1):
    page_size = 10  # Change this according to your pagination needs
    start_index = (page - 1) * page_size
    end_index = start_index + page_size
    paginated_articles = dummy_articles[start_index:end_index]
    total_pages = -(-len(dummy_articles) // page_size)  # Ceiling division to calculate total pages

    # Simulating delay of 0.5 seconds for demonstration
    time.sleep(0.5)

    return {
        "total_pages": total_pages,
        "data": paginated_articles
    }

@router.get("/getarticles", response_model=List[Article2])
def get_articles2(page_number: int = Query(1, ge=1), page_size: int = Query(10, ge=1), mongo_client: MongoClient = Depends(get_mongo_client)):
    '''
    Get all articles with pagination
    '''
    db = mongo_client["gbc_db"]
    article_collection = db["article"]
    skip = (page_number - 1) * page_size
    result = article_collection.find().skip(skip).limit(page_size)
    return list(result)

@router.post("/addarticle")
def add_article(content: str,mongo_client:MongoClient = Depends(get_mongo_client)):
    '''
    returns added article
    '''
    db = mongo_client["gbc_db"]
    article_collection = db["article"]
    # categories_collection = db["model_categories"]
    # class_vectors_collection = db["model_class_vectors"]
    # combined_classterm_weights_collection = db["model_combined_classterm_weights"]
    # unique_class_averages_collection = db["model_unique_class_averages"]
    # first_item = article_collection.find_one()
    new_article = Article2(
        title=f"{' '.join(content.split()[:8])}...",
        source="",
        content=content,
        categories=[]
    )
    result = article_collection.insert_one(dict(new_article))
    inserted_article = article_collection.find_one({"_id": result.inserted_id})
    return inserted_article


@router.get("/dummydata")
def get_dummy_data():
    pie_chart_data = {
        "labels": ["Category 1", "Category 2", "Category 3", "Category 4", "Category 5"],
        "datasets": [{
            "data": [30, 20, 15, 10, 25],
            "backgroundColor": ["#F7464A", "#46BFBD", "#FDB45C", "#949FB1", "#4D5360"],
            "hoverBackgroundColor": ["#FF5A5E", "#5AD3D1", "#FFC870", "#A8B3C5", "#616774"]
        }]
    }

    bar_chart_data = {
        "labels": ["Category 1", "Category 2", "Category 3", "Category 4", "Category 5"],
        "datasets": [{
            "label": "Weightings Of All Categories",
            "data": [25, 30, 15, 20, 10],
            "backgroundColor": ["rgba(245, 74, 85, 0.5)", "rgba(90, 173, 246, 0.5)",
                                "rgba(245, 192, 50, 0.5)", "rgba(255, 159, 64, 0.5)", "rgba(75, 192, 192, 0.5)"],
            "borderWidth": 1
        }]
    }
    return {"pieChartData": pie_chart_data, "barChartData": bar_chart_data}

@router.get("/getarticles")
def main():
    '''
    returns all Articles
    '''
    return "Articles VIEW"




# @router.get("/articles")
# def main2():
#     '''
#     returns Articles
#     '''
#     return "Articles VIEW"


@router.post("/classifydata")
async def post_classifydata(article_data:str,request: Request,mongo_client:MongoClient = Depends(get_mongo_client)):
    '''
    returns classifydata
    '''
    model=GroupByClassModel()
    db = mongo_client["gbc_db"]
    model_collection = db["model"]
    first_item = model_collection.find_one()

    if first_item:
        model.set_model(first_item)

    try:
        if first_item:
            model.set_model(first_item)
            result=model.classify(article_data)
            return result
        else:
            return {"message":"no trained model found"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"message: {str(e)}")

    # user_agent = request.headers.get("user-agent")
    # # Access request body
    # data = await request.json()
    # # Access request query parameters
    # query_params = dict(request.query_params)
    # # Process the request and return a response
    # response_data = {"user_agent": user_agent, "data": data, "query_params": query_params}
    # return response_data

@router.post("/healthtrain")
async def healthtrain(request_data: list[Article],modelname:str="model",increment_learning:bool=True,mongo_client: MongoClient = Depends(get_mongo_client)):
    '''
    train model
    '''
    # class_names=None#['Plane','Car','Bird','Cat','Deer','Dog','Frog','Horse','Ship','Truck']
    class_names=['Global Health Security Initiatives',
    'Infectious Disease Response and Prevention',
    'Public Health Emergency Preparedness',
    'Environmental Health and Protection',
    'Pandemic Management and Response']
    model=GroupByClassModel(name=modelname,categories=class_names,increment_learning=increment_learning)
    db = mongo_client["gbc_db"]
    model_collection = db["model"]

    first_item = model_collection.find_one()

    if first_item:
        model.set_model(first_item)

    model.train(request_data)
    # model.get_categories(True)
    trained_model ={
        "name":model.name,
        "number_of_documents":model.number_of_documents,
        "trained":model.model_trained,
        "categories":model.model_categories,
        "class_vectors":model.model_class_vectors,
        "combined_classterm_weights":model.model_combined_classterm_weights,
        "unique_class_averages":model.model_unique_class_averages
    }
    try:
        result = model_collection.replace_one({"name": model.name},trained_model, upsert=True)
        return trained_model
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"message: {str(e)}")


@router.post("/articles")
async def articles(request_data: list[Article]):#, db = Depends(get_db)):
    '''
    add articles
    '''
    # redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

    result="test"
    # jsondata=request_data#json.dump(request_data)
    model=GroupByClassModel()
    model.train(request_data)
    # # model3.train(example_json_data2)
    # model.get_categories(True)
    result=model.classify("Congratulations! You've been selected as the winner of our exclusive contest. Claim your prize now!")
    return  result

@router.post("/train")
async def train(request_data: list[Article],modelname:str="model",increment_learning:bool=True,mongo_client: MongoClient = Depends(get_mongo_client)):
    '''
    train model
    '''
    class_names=[]#['Plane','Car','Bird','Cat','Deer','Dog','Frog','Horse','Ship','Truck']
    model=GroupByClassModel(name=modelname,categories=class_names,increment_learning=increment_learning)
    db = mongo_client["gbc_db"]
    model_collection = db["model"]
    # categories_collection = db["model_categories"]
    # class_vectors_collection = db["model_class_vectors"]
    # combined_classterm_weights_collection = db["model_combined_classterm_weights"]
    # unique_class_averages_collection = db["model_unique_class_averages"]
    first_item = model_collection.find_one()

    if first_item:
        model.set_model(first_item)

    model.train(request_data)
    # # model3.train(example_json_data2)
    # model.get_categories(True)
    trained_model ={
        "name":model.name,
        "number_of_documents":model.number_of_documents,
        "trained":model.model_trained,
        "categories":model.model_categories,
        "class_vectors":model.model_class_vectors,
        "combined_classterm_weights":model.model_combined_classterm_weights,
        "unique_class_averages":model.model_unique_class_averages
    }
    try:
        # Insert the item into MongoDB
        # inserted_item = collection.insert_one(model.model_class_vectors)
        # result = class_vectors_collection.replace_one({"_id": model.name},model.model_class_vectors, upsert=True)
        # result = class_vectors_collection.insert_one(model.model_class_vectors)
        # result = model_collection.insert_one(trained_model)
        result = model_collection.replace_one({"name": model.name},trained_model, upsert=True)
        return trained_model
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"message: {str(e)}")
    
@router.post("/classify")
async def classify(article_data:str="Congratulations! You've been selected as the winner of our exclusive contest. Claim your prize now!",mongo_client: MongoClient = Depends(get_mongo_client)):
    '''
    train model
    '''
    model=GroupByClassModel()
    db = mongo_client["gbc_db"]
    model_collection = db["model"]
    first_item = model_collection.find_one()

   
    # categories_collection = db["model_categories"]
    # class_vectors_collection = db["model_class_vectors"]
    # combined_classterm_weights_collection = db["model_combined_classterm_weights"]
    # unique_class_averages_collection = db["model_unique_class_averages"]
   
    # model.model_categories=model_categories
    # model.model_class_vectors=model_class_vectors
    # model.model_combined_classterm_weights=model_combined_classterm_weights
    # model.model_unique_class_averages=model_unique_class_averages

    # model.train(request_data)
    # # model3.train(example_json_data2)
    # model.get_categories(True)
    try:
        # Insert the item into MongoDB
        # inserted_item = collection.insert_one(model.model_class_vectors)
        if first_item:
            model.set_model(first_item)
            result=model.classify(article_data)
            return result
        else:
            return {"message":"no trained model found"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"message: {str(e)}")

    return ""