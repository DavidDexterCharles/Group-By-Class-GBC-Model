# pylint: disable=C0115:missing-class-docstring,C0114:missing-module-docstring
from fastapi import APIRouter

from app.api.pydanticmodels import Article
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
    print("apple")
    article=request_data
    return  request_data
