from models import  app
from restless import RestApi

RestApi()

if __name__ == '__main__':

    app.run(debug=True, port=8081,host='0.0.0.0')



