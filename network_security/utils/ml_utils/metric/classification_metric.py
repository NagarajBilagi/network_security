from network_security.entity.artifact_entity import ClassificationMetricArtifact
from network_security.exception.exception import NetworkSecurityException

import os, sys

from sklearn.metrics import f1_score, precision_score, recall_score

def get_classification_score(y_pred, y_true)-> ClassificationMetricArtifact:

    try:
        model_f1_score= f1_score(y_true, y_pred)
        model_precision_score = precision_score(y_true, y_pred)
        model_recall_score = recall_score(y_true, y_pred)
        
        classification_score =ClassificationMetricArtifact(f1_score= model_f1_score, 
                                                           precsion_score= model_precision_score, 
                                                           recall_score=model_recall_score)
        return classification_score

    except Exception as e:
        raise NetworkSecurityException(e, sys)


