from flask import request, jsonify, make_response
from model import Model
from flask import Flask
app = Flask(__name__)
mvcmodel = Model() # Controller instatiates Model to Interact With 
                   # classification model and database


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

@app.route('/', methods=['GET'])
def test():
    return "Welcome to GBC API"
@app.route('/classifydata', methods=['POST']) # End point For Classifying Data
def get_classofdata():
    result =  mvcmodel.get_classofdata(request)
    return result    
@app.route('/classify', methods=['GET'])    
def getCategory():
    query = request.args.get('query')
    result =""
    if query:
      alltopicsandkeys=mvcmodel.traversePages("setTopicandTerms",'topicmodel')
      result = mvcmodel.getCategory(query,2,alltopicsandkeys)
    else:
      result = "none"
    return result
@app.route('/article', methods=['GET']) # Gets Articles and Associated Categories
def get_articlebypage():
    page = request.args.get('page')
    if page:
        result = mvcmodel.get_articlebypage(page)
    else:
        result = mvcmodel.get_articlebypage(1)
    return result
@app.route('/classificationmodel', methods=['GET']) # Returns the Classification Model
def getclassificationmodel():
    result = mvcmodel.getclassificationmodel()
    return result        







    
    

 
@app.route('/categorysearch', methods=['GET'])
def getcategorybyquery():
    query = request.args.get('query')
    result =""
    if query:
        result = mvcmodel.getcategorybyquery(query)
    else:
        result =  "All"  
    
    return result
    
@app.route('/topics', methods=['GET'])    
def getTopics():
    return mvcmodel.getTopics()
# @app.route('/keyword/<id>', methods=['GET'])
# def get_one_keyword(id):
#     return mvcmodel.getbyidkeyword(id)
# @app.route('/keyword', methods=['POST'])
# def create_keyword():
#     return mvcmodel.createkeyword(request)
# @app.route('/keyword/<id>', methods=['PATCH'])
# def update_keyword():
#     return mvcmodel.updatekeyword(request)
# @app.route('/keyword', methods=['DELETE'])
# def delete_keyword(id):
#     return mvcmodel.deletekeyword(request)
# @app.route('/keywords/', methods=['GET'])
# @app.route('/keywords', methods=['GET'])
# def getwordkey():
#     query = request.args.get('query')
#     page = request.args.get('page')
#     if page:
#         result = mvcmodel.getKeywordByPage(page)
#     else:
#         if query:
#             result = mvcmodel.getKeyword(query)
#         else:
#             result= mvcmodel.getallkeywords()
#     return result
    

    
    
    
    
    
# @app.route('/categorykeywords', methods=['GET'])
# def getalltopicmodels():
#     # page = request.args.get('page')
#     page=1;
#     result = mvcmodel.getcategorykeysbypage()
#     return result