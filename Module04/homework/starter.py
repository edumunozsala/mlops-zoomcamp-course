#!/usr/bin/env python
# coding: utf-8


import pickle
import pandas as pd
import argparse

def read_data(filename, categorical, month, year):
    df = pd.read_parquet(filename)
    
    df['duration'] = df.tpep_dropoff_datetime - df.tpep_pickup_datetime
    df['duration'] = df.duration.dt.total_seconds() / 60

    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()
    
    df[categorical] = df[categorical].fillna(-1).astype('int').astype('str')
    
    df['ride_id'] = f'{year:04d}/{month:02d}_' + df.index.astype('str')
    
    return df

def load_model(model_filename):
    with open(model_filename, 'rb') as f_in:
        dv, model = pickle.load(f_in)
    
    return dv, model   

def score_model(df, features, dv, model):
    dicts = df[features].to_dict(orient='records')
    X_val = dv.transform(dicts)
    y_pred = model.predict(X_val)
    
    return y_pred


def get_prediction(df, categorical, model_filename):
    dv, model= load_model(model_filename)
    y_pred = score_model(df, categorical, dv, model)
    
    return y_pred

def save_predictions(df, y_pred, output_file):
    df_result=pd.DataFrame()
    df_result['ride_id']= df['ride_id']
    df_result['prediction']= y_pred

    df_result.to_parquet(
        output_file,
        engine='pyarrow',
        compression=None,
        index=False
    )
    
    return df

# Function to read the parameters year and month using argparse
def read_params():
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-y","--year", type=int, choices=range(2020,2024), help="Year of the data")
    parser.add_argument("-m", "--month", type=int, choices=range(1,13), help="Month of the data")
    parser.add_argument("--model", type=str, default="model.bin", help="Filename of the model")
    args = parser.parse_args()
    
    return args    

if __name__ == "__main__":
    categorical = ['PULocationID', 'DOLocationID']
    #year=2023
    #month=3
    #model_filename='model.bin'
    args= read_params()
    #Download the data
    input_file=f'https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{args.year:04d}-{args.month:02d}.parquet'
    output_file=f'output/results_{args.year:04d}-{args.month:02d}.parquet'
    print("File to download: ", input_file)
    df = read_data(input_file, categorical, args.month, args.year)
    print("Data downloaded")
    # Generate the predictions
    y_pred= get_prediction(df, categorical, args.model)
    print("Model predictions executed")
    # Calculare mean predicted duration
    print("Mean Predicted Duration: ", y_pred.mean())
    # Save the predictions
    df_result= save_predictions(df, y_pred,output_file)
    print("Model predictions saved")