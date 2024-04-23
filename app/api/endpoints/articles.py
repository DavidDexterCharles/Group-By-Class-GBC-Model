# pylint: disable=C0115:missing-class-docstring,C0114:missing-module-docstring
# pylint: disable=C0301:line-too-long
# pylint: disable=W0707:raise-missing-from
# import json
# import redis
from bson import ObjectId
from pymongo import MongoClient
from fastapi import APIRouter, Depends, HTTPException
from app.api.pydanticmodels import Article
from app.services.gbc import GroupByClassModel

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


@router.get("/articles")
def main():
    '''
    returns Articles
    '''
    return "Articles VIEW"


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
    model=GroupByClassModel(name=modelname,increment_learning=increment_learning)
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