from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score
from .IntentTraining import training_data


class IntentClassifier:
    def __init__(self):
        self.pipeline = Pipeline(
            [
                ("vectorizer", TfidfVectorizer()),
                ("model", LinearSVC(dual=False)),  # Using Linear SVM as the classifier
            ]
        )
        self.is_trained = False
        self.train(training_data)

    def train(self, training_data):
        training_texts, training_labels = zip(*training_data)
        self.pipeline.fit(training_texts, training_labels)
        self.is_trained = True

    def predict_intent(self, text):
        if not self.is_trained:
            raise ValueError("Classifier is not trained yet.")

        intent = self.pipeline.predict([text])[0]
        return intent
