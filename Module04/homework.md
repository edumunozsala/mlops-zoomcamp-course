## Homework

In this homework, we'll deploy the ride duration model in batch mode. Like in homework 1, we'll use the Yellow Taxi Trip Records dataset. 

You'll find the starter code in the [homework](homework) directory.


## Q1. Notebook

We'll start with the same notebook we ended up with in homework 1.
We cleaned it a little bit and kept only the scoring part. You can find the initial notebook [here](homework/starter.ipynb).

Run this notebook for the March 2023 data.

What's the standard deviation of the predicted duration for this dataset?

* 1.24
* 6.24
* 12.28
* 18.28

**Answer**: 6.24

We just need to score or predict on the dataset and calculate the standard deviation using numpy:
```python
categorical = ['PULocationID', 'DOLocationID']
input_file='https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2023-03.parquet'
df = read_data(input_file, categorical)
model_filename='model.bin'
dv, model= load_model(model_filename)
y_pred = score_model(df, categorical, dv, model)
print("Standard Deviation: ",np.std(y_pred))
```
```text
Standard Deviation:  6.247488852238703
```

## Q2. Preparing the output

Like in the course videos, we want to prepare the dataframe with the output. 

First, let's create an artificial `ride_id` column:

```python
df['ride_id'] = f'{year:04d}/{month:02d}_' + df.index.astype('str')
```

Next, write the ride id and the predictions to a dataframe with results. 

Save it as parquet:

```python
df_result.to_parquet(
    output_file,
    engine='pyarrow',
    compression=None,
    index=False
)
```

What's the size of the output file?

* 36M
* 46M
* 56M
* 66M

__Note:__ Make sure you use the snippet above for saving the file. It should contain only these two columns. For this question, don't change the
dtypes of the columns and use `pyarrow`, not `fastparquet`. 

**Answer**: 66M
We write the code to create a result dataframe and save it as parquet:
```python
df_result=pd.DataFrame()
df_result['ride_id']= df['ride_id']
df_result['prediction']= y_pred

df_result.to_parquet(
    output_file,
    engine='pyarrow',
    compression=None,
    index=False
)
```
Then we check the filse size:
```bash
ls -l --block-size=M

total 66M
```

## Q3. Creating the scoring script

Now let's turn the notebook into a script. 

Which command you need to execute for that?

**Answer**: jupyter nbconvert --to script starter.ipynb


## Q4. Virtual environment

Now let's put everything into a virtual environment. We'll use pipenv for that.

Install all the required libraries. Pay attention to the Scikit-Learn version: it should be the same as in the starter
notebook.

After installing the libraries, pipenv creates two files: `Pipfile`
and `Pipfile.lock`. The `Pipfile.lock` file keeps the hashes of the
dependencies we use for the virtual env.

What's the first hash for the Scikit-Learn dependency?

**Answer**: sha256:057b991ac64b3e75c9c04b5f9395eaf19a6179244c089afdebaad98264bff37c

We need to install pipenv like other pip packages, you may have to update PATH variable. then, you can install packages in the enviroment in your project folder (`pipenv install <package>`) and we can review the Pipfile.lock and search for the scikit-learn package.

## Q5. Parametrize the script

Let's now make the script configurable via CLI. We'll create two 
parameters: year and month.

Run the script for April 2023. 

What's the mean predicted duration? 

* 7.29
* 14.29
* 21.29
* 28.29

Hint: just add a print statement to your script.

**Answer**: 14.29

Parameterized the code:
```py
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
```

And execute the script:
```bash
python -m starter -y 2023 -m 4
```
## Q6. Docker container 

Finally, we'll package the script in the docker container. 
For that, you'll need to use a base image that we prepared. 

This is what the content of this image is:
```
FROM python:3.10.13-slim

WORKDIR /app
COPY [ "model2.bin", "model.bin" ]
```

Note: you don't need to run it. We have already done it.

It is pushed it to [`agrigorev/zoomcamp-model:mlops-2024-3.10.13-slim`](https://hub.docker.com/layers/agrigorev/zoomcamp-model/mlops-2024-3.10.13-slim/images/sha256-f54535b73a8c3ef91967d5588de57d4e251b22addcbbfb6e71304a91c1c7027f?context=repo),
which you need to use as your base image.

That is, your Dockerfile should start with:

```docker
FROM agrigorev/zoomcamp-model:mlops-2024-3.10.13-slim

# do stuff here
```

This image already has a pickle file with a dictionary vectorizer
and a model. You will need to use them.

Important: don't copy the model to the docker image. You will need
to use the pickle file already in the image. 

Now run the script with docker. What's the mean predicted duration
for May 2023? 

* 0.19
* 7.24
* 14.24
* 21.19

**Answer**: 0.19

We create the Dockerfile:
```docker
FROM agrigorev/zoomcamp-model:mlops-2024-3.10.13-slim

ENV PROJECT_DIR /app

RUN python -m pip install --upgrade pip
RUN pip install pipenv

WORKDIR ${PROJECT_DIR}
RUN mkdir output
COPY Pipfile Pipfile.lock starter.py ${PROJECT_DIR}/
RUN pipenv install --system --deploy

ENV PATH="/.venv/bin:$PATH"

ENTRYPOINT ["python", "-m", "starter"]
CMD ["-y", "2023","-m", "5"]
```

Once the Dockerfile is created, we build the image:
```bash
docker build . -t homework41
```
Output:
```text
DEPRECATED: The legacy builder is deprecated and will be removed in a future release.
            Install the buildx component to build images with BuildKit:
            https://docs.docker.com/go/buildx/

Sending build context to Docker daemon  134.9MB
Step 1/9 : FROM agrigorev/zoomcamp-model:mlops-2024-3.10.13-slim
mlops-2024-3.10.13-slim: Pulling from agrigorev/zoomcamp-model
8a1e25ce7c4f: Pull complete 
1103112ebfc4: Pull complete 
fb784af4aeda: Pull complete 
043e7f3dd05a: Pull complete 
538a89c93346: Pull complete 
db87daa82210: Pull complete 
d8ee6bfe02f5: Pull complete 
Digest: sha256:f54535b73a8c3ef91967d5588de57d4e251b22addcbbfb6e71304a91c1c7027f
Status: Downloaded newer image for agrigorev/zoomcamp-model:mlops-2024-3.10.13-slim
 ---> 13e5353db264
Step 2/9 : ENV PROJECT_DIR /app
 ---> Running in 1f2af07b55a3
Removing intermediate container 1f2af07b55a3
 ---> e4fe60fb7aac
Step 3/9 : RUN python -m pip install --upgrade pip
 ---> Running in cbdf82cc1168
Requirement already satisfied: pip in /usr/local/lib/python3.10/site-packages (23.0.1)
...
Step 4/9 : RUN pip install pipenv
...
 ---> 5c6a03a9797d
Step 5/9 : WORKDIR ${PROJECT_DIR}
 ---> Running in f585440cfd2a
Removing intermediate container f585440cfd2a
 ---> 25f861845c81
Step 6/9 : RUN mkdir output
 ---> Running in dbe7302b8842
Removing intermediate container dbe7302b8842
 ---> 3b04d716f7cf
Step 7/9 : COPY Pipfile Pipfile.lock starter.py ${PROJECT_DIR}/
 ---> 36aef3b65942
Step 8/9 : RUN pipenv install --system --deploy
 ---> Running in ad474fd0f0d9
Installing dependencies from Pipfile.lock (939b42)...
Removing intermediate container ad474fd0f0d9
 ---> 2e453590c0be
Step 9/9 : CMD [     "python", "-m", "starter",    "-y", "2023",     "-m", "5", ]
 ---> Running in 9d047b23b469
Removing intermediate container 9d047b23b469
 ---> 71f6b0c6803f
Successfully built 71f6b0c6803f
Successfully tagged homework41:latest
```
Run the image to execute the inference:
```bash
docker run -it homework41
```
and the output was:
```text
(exp-tracking-env) ubuntu@ip-172-31-55-58:~/mlops-zoomcamp/04-deployment/homework$ docker run -it homework41

File to download:  https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2023-05.parquet
Data downloaded
Model predictions executed
Mean Predicted Duration:  0.19174419265916945
Model predictions saved
```

To test or debug your script you can login to a terminal in the container:
```bash
docker run -it homework41 bash
```

## Bonus: upload the result to the cloud (Not graded)

Just printing the mean duration inside the docker image 
doesn't seem very practical. Typically, after creating the output 
file, we upload it to the cloud storage.

Modify your code to upload the parquet file to S3/GCS/etc.


## Publishing the image to dockerhub

This is how we published the image to Docker hub:

```bash
docker build -t mlops-zoomcamp-model:2024-3.10.13-slim .
docker tag mlops-zoomcamp-model:2024-3.10.13-slim agrigorev/zoomcamp-model:mlops-2024-3.10.13-slim

docker login --username USERNAME
docker push agrigorev/zoomcamp-model:mlops-2024-3.10.13-slim
```
## Link to articles about deploying with pipenv in a Dockerfile

https://sourcery.ai/blog/python-docker/
https://dev.to/mrpbennett/setting-up-docker-with-pipenv-3h1o
https://pipenv.pypa.io/en/stable/docker.html
