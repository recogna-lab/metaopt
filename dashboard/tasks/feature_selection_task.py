import os
import numpy as np

import opfython.math.general as g
import opfython.stream.loader as l
import opfython.stream.splitter as sp
from opfython.models.supervised import SupervisedOPF

from utils.transfer_functions import get_transfer_function
from utils.optimizers import get_optimizer
import utils.parser as p

from metaopt.celery import app

from .optimization_task import _OptimizationTask
from opytimizer.core import Function

from metaopt.settings.environment import BASE_DIR

class _FeatureSelectionTask(_OptimizationTask):
    
    abstract = True

    def supervised_opf(self, opytimizer):
        # Transform the continuous solution in boolean solution (feature array) by applying the transfer function
        features = self.transfer_function(opytimizer)

        # Remake training and validation subgraphs with selected features
        X_train_selected = self.X_train[:, features]
        X_val_selected = self.X_val[:, features]

        # Create a SupervisedOPF instance
        opf = SupervisedOPF(
            distance='log_squared_euclidean',
            pre_computed_distance=None
        )

        # Fit training data into the classifier
        opf.fit(X_train_selected, self.Y_train)

        # Predict new data frnp.max(Y) + 1
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

    def optimize(self, optimizer, function, space, agents, iterations):
        # Set optimizer
        return super().optimize(
            optimizer,
            self.supervised_opf,
            space,
            agents,
            iterations
        )
    
    def setup(self, optimizer, function, space, agents):
        # Get and set the optimizer object    
        self.optimizer = get_optimizer(optimizer)
        
        # Set the cost function
        self.function = Function(function)

        # Configure the search space
        self.setup_space(agents, space)

    def select_features(self, optimizer, dataset, transfer_function, dimension, agents, iterations):

        self.dataset_split(dataset)

        self.transfer_function = get_transfer_function(transfer_function)

        lower_bound = [0] * dimension
        upper_bound = [1] * dimension

        space = {'dimension': dimension, 'lower_bound': lower_bound, 'upper_bound': upper_bound}

        result_opt = self.optimize(optimizer, None, space, agents, iterations)

        opf = SupervisedOPF(
            distance='log_squared_euclidean',
            pre_computed_distance=None
        )

        result_fs = self.testing_task(opf)

        metrics = self.metrics(result_fs['confusion_matrix']) 
        
        result = self.concatenate_results(result_opt, result_fs, metrics)

        return result

    def dataset_split(self, dataset):
        # Take the path of dataset
        dir = os.path.join(BASE_DIR, 'dashboard/static/dashboard/datasets', dataset)
        
        # Loading a .txt file to a numpy array
        txt = l.load_txt(dir)

        # Parsing a pre-loaded numpy array
        X, Y = p.parse_loader(txt)

        # Split data into training and test sets
        self.X_train, self.X_test, self.Y_train, self.Y_test = sp.split(
            X, Y, percentage=0.5, random_state=1
        )

        # Training set will be splited into training and validation sets
        self.X_train, self.X_val, self.Y_train, self.Y_val = sp.split(
            self.X_train, self.Y_train, percentage = 0.2, random_state=1
        )

    def testing_task(self, opf):
        # Remake training and tests subgraphs with selected features
        X_train_selected = self.X_train[:, self.best_selected_features]
        X_test_selected = self.X_test[:, self.best_selected_features]

        # Fit training data into the classifier
        opf.fit(X_train_selected, self.Y_train)

        # Predict new data from test set 
        preds = opf.predict(X_test_selected)

        confusion_matrix = g.confusion_matrix(self.Y_test, preds)
        confusion_matrix = confusion_matrix[1:, 1:]

        accuracy = g.opf_accuracy(self.Y_test, preds)

        return {
            'best_selected_features' : self.best_selected_features.tolist(), 
            'accuracy': accuracy, 
            'confusion_matrix': confusion_matrix.tolist()
        }

    def concatenate_results(self, *results):

        result = {}

        for r in results:
            result.update(r)

        return result
    
    def metrics(self, confusion_matrix):
        
        confusion_matrix = np.array(confusion_matrix)
        rows, _ = confusion_matrix.shape

        precision = []
        recall = []
        f1_score = []

        sum_cols = np.sum(confusion_matrix, axis=0)
        sum_rows = np.sum(confusion_matrix, axis=1)

        for clss in range(rows):
            p = confusion_matrix[clss, clss] / sum_cols[clss]
            r = confusion_matrix[clss, clss] / sum_rows[clss]
            f1 = 2 * (p * r) / (p + r)

            precision.append(p)
            recall.append(r)
            f1_score.append(f1)

        return {
            'precision': precision,
            'recall': recall,
            'f1-score': f1_score
        }

@app.task(name='feature_selection', base=_FeatureSelectionTask, bind=True)
def feature_selection(self, user_id, optimizer, dataset, transfer_function, dimension, agents, iterations):

    result = self.select_features(optimizer, dataset, transfer_function, dimension, agents, iterations)

    # Return None (just to have a value)
    return result