import mlflow
import mlflow.sklearn
import pickle
import os
from pathlib import Path
from typing import Tuple

from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LinearRegression


if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter

def dump_pickle(obj, filename: str):
    with open(filename, "wb") as f_out:
        return pickle.dump(obj, f_out)

@data_exporter
def export_data(#data, 
                data: Tuple[DictVectorizer, LinearRegression],
                *args, **kwargs):
    """
    Exports data to some source.

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Output (optional):
        Optionally return any object and it'll be logged and
        displayed when inspecting the block run.
    """
    # Specify your data exporting logic here
    # Specify your data exporting logic here
    dv, lr = data
    
    os.makedirs(kwargs.get('artifacts_path'),exist_ok=True)
    mlflow.set_tracking_uri(kwargs.get('mlflow_tracking_uri'))
    mlflow.set_experiment(kwargs.get('experiment_name'))
    print("Created experiment: ",kwargs.get('experiment_name'))
    
    with mlflow.start_run():
        # Log the model
        mlflow.sklearn.log_model(lr, "models")
        print("Model Logged")
        dump_pickle(dv, os.path.join(kwargs.get('artifacts_path'), "dv.pkl"))
        print("DV Saved")
        # Save the dv as an artifact
        mlflow.log_artifact(kwargs.get('artifacts_path'))
        print("DV Logged")
