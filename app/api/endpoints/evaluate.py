# pylint: disable=C0115:missing-class-docstring,C0114:missing-module-docstring,C0301:line-too-long,W0707:raise-missing-from
# from bson import ObjectId
from pymongo import MongoClient
from fastapi import APIRouter, Depends, HTTPException
from app.api.endpoints.ml_models.model_metrics import ModelMetrics
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


@router.get("/evaluate")
def main():
    '''
    returns Evaluation Hamming Loss, F1 Score, Precision, Recall, or Area Under the ROC Curve (AUC-ROC)
    '''
    return "Evaluate Hamming Loss, F1 Score, Precision, Recall, or Area Under the ROC Curve (AUC-ROC)"


@router.post("/f1score")
async def f1score(request_data: list[Article],mongo_client: MongoClient = Depends(get_mongo_client)):#, db = Depends(get_db)):
    '''
    return f1score
    '''

    '''
    model=GroupByClassModel()
    model.train(request_data)
    # # model3.train(example_json_data2)
    # model.get_categories(True)
    result=model.classify("Congratulations! You've been selected as the winner of our exclusive contest. Claim your prize now!")
    return  result
    '''

    db = mongo_client["gbc_db"]
    model_collection = db["model"]
    first_item = model_collection.find_one()
    

    
    mm= ModelMetrics()
    # bayes=mm.naive_bayes()
    gbc_model_1:dict=mm.gbc_binary()
    model_collection.replace_one({"name": gbc_model_1["name"]},gbc_model_1, upsert=True)

    return gbc_model_1["categories"]

@router.post("/train")
async def train(request_data: list[Article],modelname:str="model",increment_learning:bool=True,mongo_client: MongoClient = Depends(get_mongo_client)):
    '''
    train model
    '''
    class_names=['Plane','Car','Bird','Cat','Deer','Dog','Frog','Horse','Ship','Truck']
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