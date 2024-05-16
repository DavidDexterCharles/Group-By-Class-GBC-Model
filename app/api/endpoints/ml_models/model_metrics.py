#pylint: disable=C0200:consider-using-enumerate,C0301:line-too-long
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB, MultinomialNB
from sklearn.metrics import f1_score, hamming_loss,accuracy_score, precision_recall_fscore_support
from sklearn.metrics import confusion_matrix , classification_report


from sklearn.datasets import make_multilabel_classification
from sklearn.model_selection import train_test_split
from sklearn.multioutput import MultiOutputClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer

from sklearn.svm import SVC


from app.api.pydanticmodels import Article
from app.services.gbc import GroupByClassModel
# https://chat.openai.com/c/f1010516-2c2c-41be-9f50-fa9e3c8d4da8

def format_data(documents, labels):
    formatted_data = []

    for i in range(len(documents)):
        # Concatenate each feature with its index/position
        # feature_strings = [f"{idx}:{val}" for idx, val in enumerate(documents[i])]
        feature_strings = [f"{idx}:{round(val,2)}" for idx, val in enumerate(documents[i])]
        instance = {
            # "content": " ".join(map(str, documents[i])),  # Convert feature array to space seperated string
            "content": " ".join(feature_strings),  # Convert feature array to space seperated string
            "categories": ["malignant" if labels[i] == 0 else "benign"]  # Convert target to corresponding category, asumes each doc has one label
        }
        formatted_data.append(instance)
        # if i==20:
        #     break
    
    return formatted_data

def format_data_string(documents, labels):
    formatted_data = []

    for i in range(len(documents)):
        # Concatenate each feature with its index/position
        # feature_strings = [f"{idx}:{val}" for idx, val in enumerate(documents[i])]
        feature_strings = documents[i]#[f"{idx}:{round(val,2)}" for idx, val in enumerate(documents[i])]
        instance = {
            # "content": " ".join(map(str, documents[i])),  # Convert feature array to space seperated string
            "content": feature_strings,  # Convert feature array to space seperated string
            "categories": [labels[i].lower()]  # Convert target to corresponding category, asumes each doc has one label
        }
        formatted_data.append(instance)
        # if i==20:
        #     break
    
    return formatted_data
def format_data_multi(X, y):
    formatted_data = []
    for i in range(len(X)):
        # labels = [f"{j}" for j in range(len(y[i])) if y[i][j] == 1]
        labels = []
        for j in range(len(y[i])):
            if y[i][j] == 1:
                labels.append(f"{j}:{y[i][j]}")
        document = {
            "content": " ".join(map(str, X[i])),
            "categories": labels
        }
        formatted_data.append(document)
    return formatted_data

class ModelMetrics:

    def __init__(self):
        # https://archive.ics.uci.edu/dataset/17/breast+cancer+wisconsin+diagnostic
        self.data_breast_cancer=load_breast_cancer()
    
    def randomforest(self):
        # Generate random multi-label dataset
        X, y = make_multilabel_classification(n_samples=1000, n_features=20, n_classes=5, n_labels=3, random_state=42)

        # Split the dataset into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Initialize the base classifier (Random Forest)
        base_classifier = RandomForestClassifier(n_estimators=100, random_state=42)

        # Initialize the MultiOutputClassifier
        multi_label_classifier = MultiOutputClassifier(base_classifier, n_jobs=-1)

        # Fit the classifier to the training data
        multi_label_classifier.fit(X_train, y_train)

        # Predict the labels for the test set
        y_pred = multi_label_classifier.predict(X_test)

        # Evaluate the classifier
        accuracy = accuracy_score(y_test, y_pred)
        print("Accuracy:", accuracy)

        # Print classification report
        print("Classification Report:")
        print(classification_report(y_test, y_pred))

    def gbc_multi(self):
        # Generate random multi-label dataset
        X, y = make_multilabel_classification(n_samples=1000, n_features=20, n_classes=5, n_labels=3, random_state=42)

        # Split the dataset into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        formatted_train_data = format_data_multi(X_train, y_train)
        formatted_test_data = format_data_multi(X_test, y_test)
        model=GroupByClassModel()
        model.train(formatted_train_data,True)
        model.classify(formatted_test_data)
        gbc_model_1=model.get_model()
        
        # # Initialize the base classifier (Random Forest)
        # base_classifier = RandomForestClassifier(n_estimators=100, random_state=42)

        # # Initialize the MultiOutputClassifier
        # multi_label_classifier = MultiOutputClassifier(base_classifier, n_jobs=-1)

        # # Fit the classifier to the training data
        # multi_label_classifier.fit(X_train, y_train)

        # # Predict the labels for the test set
        # y_pred = multi_label_classifier.predict(X_test)

        print("y_test : ", y_test)

        # Evaluate the classifier
        # accuracy = accuracy_score(y_test, y_pred)
        accuracy = accuracy_score(y_test, gbc_model_1["y_pred"])
        print("Accuracy:", accuracy)

        # # Print classification report
        # print("Classification Report:")
        # print(classification_report(y_test, y_pred))

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
        # Calculate the F1 score
        y_pred_binary = [0 if val == "malignant" else 1 for idx, val in enumerate(gbc_model_1["y_pred"])]
        f1 = f1_score(y_test, y_pred_binary)
        message=f"GBC F1 Score: {f1}"
        print(message)
        # Calculate subset accuracy
        subset_accuracy = accuracy_score(y_test, y_pred_binary)
        # Calculate Hamming loss
        hamming_loss_value = hamming_loss(y_test, y_pred_binary)
        message=f"GBC subset_accuracy: {subset_accuracy}"
        print(message)
        message=f"GBC hamming_loss_value: {hamming_loss_value}"
        print(message)
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
        # Calculate subset accuracy
        subset_accuracy = accuracy_score(y_test, y_pred)
        # Calculate Hamming loss
        hamming_loss_value = hamming_loss(y_test, y_pred)
        message=f"Bayes subset_accuracy: {subset_accuracy}"
        print(message)
        message=f"Bayes hamming_loss_value: {hamming_loss_value}"
        print(message)
        print(confusion_matrix(y_test, y_pred, labels=[0,1]))
        print(classification_report(y_test, y_pred, labels=[0,1]))

        return {"message":message}

    def gbc_model(self):
        return "f1 score"
    

    def api_svm(self,data):
        # Extract features (content) and labels (categories)
        X = [doc["content"] for doc in data]
        y = [doc["categories"][0] for doc in data]

        # Split data into train and test sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Vectorize the text data using CountVectorizer (instead of TF-IDF)
        count_vectorizer = CountVectorizer(max_features=1000)  # You can adjust max_features as needed
        X_train_counts = count_vectorizer.fit_transform(X_train)
        X_test_counts = count_vectorizer.transform(X_test)

        # Train SVM classifier
        svm_clf = SVC()
        svm_clf.fit(X_train_counts, y_train)

        # Predict labels for the test set
        y_pred = svm_clf.predict(X_test_counts)

        # Calculate F1 score
        f1 = f1_score(y_test, y_pred, average='weighted')

        # Generate confusion matrix
        conf_matrix = confusion_matrix(y_test, y_pred)

        print("svm: F1 Score:", f1)
        print("svm: Confusion Matrix:\n", conf_matrix)
        
    def api_svm_tfidf(self,data):
        # Extract features (content) and labels (categories)
        X = [doc["content"] for doc in data]
        y = [doc["categories"][0] for doc in data]

        # Split data into train and test sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Vectorize the text data using TF-IDF
        tfidf_vectorizer = TfidfVectorizer(max_features=4)  # You can adjust max_features as needed
        X_train_tfidf = tfidf_vectorizer.fit_transform(X_train)
        X_test_tfidf = tfidf_vectorizer.transform(X_test)

        # Train SVM classifier
        svm_clf = SVC()
        svm_clf.fit(X_train_tfidf, y_train)

        # Predict labels for the test set
        y_pred = svm_clf.predict(X_test_tfidf)

        # Calculate F1 score
        f1 = f1_score(y_test, y_pred, average='weighted')

        # Generate confusion matrix
        conf_matrix = confusion_matrix(y_test, y_pred)

        print("svm_tfidf: F1 Score:", f1)
        print("svm_tfidf: Confusion Matrix:\n", conf_matrix)
    
    def api_naive_bayes(self, data):
        # Extract features (content) and labels (categories)
        X = [doc["content"] for doc in data]
        y = [doc["categories"][0] for doc in data]

        # Split data into train and test sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Vectorize the text data using CountVectorizer
        count_vectorizer = CountVectorizer(max_features=4)  # You can adjust max_features as needed
        X_train_counts = count_vectorizer.fit_transform(X_train)
        X_test_counts = count_vectorizer.transform(X_test)

        # Train Naive Bayes classifier
        nb_clf = MultinomialNB()
        nb_clf.fit(X_train_counts, y_train)

        # Predict labels for the test set
        y_pred = nb_clf.predict(X_test_counts)

        # Calculate F1 score
        f1 = f1_score(y_test, y_pred, average='weighted')

        # Generate confusion matrix
        conf_matrix = confusion_matrix(y_test, y_pred)

        print("naive_bayes: F1 Score:", f1)
        print("naive_bayes: Confusion Matrix:\n", conf_matrix)

    def api_gbc(self,data):
        '''
        returns gbc metrics
        '''
        X = [doc["content"] for doc in data]
        y = [doc["categories"][0] for doc in data]
        
        # Split the data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        # Format training and testing data
        formatted_train_data = format_data_string(X_train, y_train)
        formatted_test_data = format_data_string(X_test, y_test)
        # Now, 'formatted_train_data' and 'formatted_test_data' contain the training and testing datasets in the required format
        # You can use these formatted datasets to train and evaluate your model
        model=GroupByClassModel(verbose=False)
        model.train(formatted_train_data,True)
        model.classify(formatted_test_data)
        # return model.get_categories()
        gbc_model_1=model.get_model()
        # Calculate the F1 score
        # y_pred_binary = [0 if val == "malignant" else 1 for idx, val in enumerate(gbc_model_1["y_pred"])]
        y_pred=gbc_model_1["y_pred"]
        y_test_lower = [label.lower() for label in y_test]
        y_test=y_test_lower
        # f1 = f1_score(y_test, y_pred,average='weighted')
        precision, recall, f1, _ = precision_recall_fscore_support(y_test, y_pred, average='weighted', zero_division=1)
        message=f"GBC F1 Score: {f1}, Precision:{precision},Recall:{recall}"
        print(message)
        # Calculate subset accuracy
        subset_accuracy = accuracy_score(y_test, y_pred)
        # Calculate Hamming loss
        hamming_loss_value = hamming_loss(y_test, y_pred)
        message=f"GBC subset_accuracy: {subset_accuracy}"
        print(message)
        message=f"GBC hamming_loss_value: {hamming_loss_value}"
        print(message)
        y_true=gbc_model_1["y_true"]
        print(confusion_matrix(y_test, y_pred, labels=gbc_model_1["categories"]))
        print(classification_report(y_test, y_pred, labels=gbc_model_1["categories"],zero_division=1))

        return gbc_model_1