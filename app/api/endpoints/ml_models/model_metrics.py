from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import f1_score


class ModelMetrics:

    def __init__(self):
        self.data=load_breast_cancer()

    def naive_bayes(self):
        '''
        returns bayes metrics
        '''
        # Load the breast cancer dataset
        data = load_breast_cancer()
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

        # Calculate the F1 score
        f1 = f1_score(y_test, y_pred)

        message=f"Bayes F1 Score: {f1}"
        print(message)
        return {"message":message}

    def gbc_model(self):
        return "f1 score"