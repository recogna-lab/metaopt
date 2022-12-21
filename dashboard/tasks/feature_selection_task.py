import os
from opfython.models.supervised import SupervisedOPF
import opfython.math.general as g
import opfython.stream.loader as l
import opfython.stream.parser as p
import opfython.stream.splitter as sp
import utils.transfer_functions as tf
import numpy as np
import os

from metaopt.celery import app


from .optimization_task import _OptimizationTask


class _FeatureSelectionTask(_OptimizationTask):
    abstract = True

    def supervised_opf_feature_selection(self, opytimizer):
        # Transform the continuous solution in boolean solution (feature array) by applying the transfer function
        features = tf.s1(opytimizer)

        # Remaking training and validation subgraphs with selected features
        X_train_selected = self.X_train[:, features]
        X_val_selected = self.X_val[:, features]

        # Create a SupervisedOPF instance
        opf = SupervisedOPF(
            distance='log_squared_euclidean',
            pre_computed_distance=None
        )

        # Fit training data into the classifier
        opf.fit(X_train_selected, self.Y_train)

        # Predict new data from validate set
        preds = opf.predict(X_val_selected)

        # Calculate accuracy
        acc = g.opf_accuracy(self.Y_val, preds)

        # Error
        error = 1 - acc

        # If the error is lower than the best agent's error
        if error <= self.space.best_agent._fit:
            # Save the best selected features
            self.best_selected_features = features

        return error

    def optimize(self, optimizer, agents, iterations):
        # Set optimizer    
        super().optimize(optimizer, self.supervised_opf_feature_selection, agents, iterations)

    def testing_task(self, opf):
        # Remaking training and tests subgraphs with selected features
        X_train_selected = self.X_train[:, self.best_selected_features]
        X_test_selected = self.X_test[:, self.best_selected_features]

        # Fit training data into the classifier
        opf.fit(X_train_selected, self.Y_train)

        # Predict new data from test set 
        preds = opf.predict(X_test_selected)

        confusion_matrix = g.confusion_matrix(self.Y_test, preds)
        accuracy = g.opf_accuracy(self.Y_test, preds)

        return (accuracy, confusion_matrix)

@app.task(name='feature_selection', base=_FeatureSelectionTask, bind=True)
def feature_selection(self, user_id, optimizer, dataset, agents, iterations):
    # Take the path of dataset
    dir = os.path.join('datasets', dataset)
    
    # Loading a .txt file to a numpy array
    txt = l.load_txt(dir)

    # Parsing a pre-loaded numpy array
    X, Y = p.parse_loader(txt)

    # Split data into training and test sets
    X_train, X_test, Y_train, Y_test = sp.split(
        X, Y, percentage=0.5, random_state=1
    )

    # Training set will be splited into training and validation sets
    self.X_train, self.X_val, self.Y_train, self.Y_val = sp.split(
        X_train, Y_train, percentage = 0.2, random_state=1
    )

    result = self.optimize(optimizer, agents, iterations)

    opf = SupervisedOPF(
        distance='log_squared_euclidean',
        pre_computed_distance=None
    )

    acc, confusion_matrix = self.testing_task(opf)

    # Return None (just to have a value)
    return None