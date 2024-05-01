#pylint: disable=C0200:consider-using-enumerate
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import f1_score
from sklearn.metrics import confusion_matrix , classification_report


from app.api.pydanticmodels import Article
from app.services.gbc import GroupByClassModel
# https://chat.openai.com/c/f1010516-2c2c-41be-9f50-fa9e3c8d4da8

def format_data(documents, labels):
    formatted_data = []

    for i in range(len(documents)):
        # Concatenate each feature with its index/position
        # feature_strings = [f"{idx}:{val}" for idx, val in enumerate(documents[i])]
        feature_strings = [f"{idx}:{round(val,1)}" for idx, val in enumerate(documents[i])]
        instance = {
            # "content": " ".join(map(str, documents[i])),  # Convert feature array to space seperated string
            "content": " ".join(feature_strings),  # Convert feature array to space seperated string
            "categories": ["malignant" if labels[i] == 0 else "benign"]  # Convert target to corresponding category, asumes each doc has one label
        }
        formatted_data.append(instance)
        # if i==20:
        #     break
    
    return formatted_data

class ModelMetrics:

    def __init__(self):
        # https://archive.ics.uci.edu/dataset/17/breast+cancer+wisconsin+diagnostic
        self.data_breast_cancer=load_breast_cancer()
    
    def gbc_binary(self):
        '''
        returns gbc metrics
        '''
        # Load the breast cancer data
        data =  self.data_breast_cancer
        X = data.data  # Features
        y = data.target  # Target variable (0 for malignant, 1 for benign)

        # Split the data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        # Format training and testing data
        formatted_train_data = format_data(X_train, y_train)
        formatted_test_data = format_data(X_test, y_test)
        # Now, 'formatted_train_data' and 'formatted_test_data' contain the training and testing datasets in the required format
        # You can use these formatted datasets to train and evaluate your model
        model=GroupByClassModel()
        model.train(formatted_train_data,True)
        model.classify(formatted_test_data)
        # return model.get_categories()
        gbc_model_1=model.get_model()
        print(confusion_matrix(gbc_model_1["y_true"], gbc_model_1["y_pred"], labels=gbc_model_1["categories"]))
        print(classification_report(gbc_model_1["y_true"], gbc_model_1["y_pred"], labels=gbc_model_1["categories"]))

        return gbc_model_1

    def naive_bayes(self):
        '''
        returns bayes metrics
        '''
        # Load the breast cancer dataset
        data =  self.data_breast_cancer
        X = data.data  # Features
        y = data.target  # Target variable (0 for malignant, 1 for benign)

        # Split the data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Initialize the Naive Bayes classifier
        model = GaussianNB()

        # Train the model
        model.fit(X_train, y_train)

        # Make predictions on the test set
        y_pred = model.predict(X_test)
        
        # y_true_text=[]
        # y_pred_text=[]
        # for i in range (len(y_pred)):
        #     y_true_text.append(X_test.target_names[X_test.target[i]])
        #     y_pred_text.append(X_test.target_names[y_pred[i]])
        #     if y_pred[i]==X_test.target[i]:
        #         count=count+1

        # Calculate the F1 score
        f1 = f1_score(y_test, y_pred)

        message=f"Bayes F1 Score: {f1}"
        print(message)

        print(confusion_matrix(y_test, y_pred, labels=[0,1]))
        print(classification_report(y_test, y_pred, labels=[0,1]))

        return {"message":message}

    def gbc_model(self):
        return "f1 score"