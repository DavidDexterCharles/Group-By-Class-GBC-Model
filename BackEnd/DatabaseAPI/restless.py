import models



class RestApi(object):

    def __init__(self):
        models.restless_manager.create_api(models.Article, methods=['GET', 'POST', 'DELETE','PUT','PATCH'])
        models.restless_manager.create_api(models.Articlecategorie, methods=['GET', 'POST', 'DELETE','PUT','PATCH'])
        models.restless_manager.create_api(models.Categorie, methods=['GET', 'POST', 'DELETE','PUT','PATCH'])
        models.restless_manager.create_api(models.Geotag, methods=['GET', 'POST', 'DELETE','PUT','PATCH'])
        models.restless_manager.create_api(models.Domain, methods=['GET', 'POST', 'DELETE','PUT','PATCH'])
        models.restless_manager.create_api(models.Topicmodel, methods=['GET', 'POST', 'DELETE','PUT','PATCH'])
        models.restless_manager.create_api(models.Keyword, methods=['GET', 'POST', 'DELETE','PUT','PATCH'])


