# pylint: disable=C0115:missing-class-docstring,C0114:missing-module-docstring
# pylint: disable=C0301:line-too-long
import json
import redis
from fastapi import APIRouter
from app.api.pydanticmodels import Article
from app.services.gbc import GroupByClassModel
router = APIRouter()


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
    redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

    result="test"
    # jsondata=request_data#json.dump(request_data)
    model=GroupByClassModel()
    model.train(request_data)
    # # model3.train(example_json_data2)
    # model.get_categories(True)
    result=model.classify("Congratulations! You've been selected as the winner of our exclusive contest. Claim your prize now!")
    return  result
