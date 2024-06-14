# MLOps Zoomcamp Course Cohort 2024

### 2024 Cohort

## Module 4: Model Deployment

* Three ways of model deployment: Online (web and streaming) and offline (batch)
* Web service: model deployment with Flask
* Streaming: consuming events with AWS Kinesis and Lambda
* Batch: scoring data offline
* Homework

## 🎯 ML Model Deployment as on-demand prediction service

Many business problems require to get a prediction from our ML model in real-time and on-demand with a low response time. In this scenario, the size of our model is a critical and limiting factor. Depending on it, we will have to design the architecture to deploy our predictor.

Suppose we have a small size model that predicts a lead time or classifies a product within a category, in this case we can consider the following simple steps for deploying it:

💾 Save and persist the model file in a secure but sharable storage (.pkl, .h5, .mod, etc.).
📲 Create REST API services to load and run the model using a framework like Flask, FastAPI, etc.
🔏 Create a Dockerfile, include only the strictly necessary dependencies to run our model.
🛠 Build a docker image and register it in a Container Registry on any cloud provider.
🛩 Deploy the API on a cloud service like Azure Web Services, AWS Fargate, or even any serverless service, AWS Lambda, Functions, Cloud Run, etc, using the container image.

This is just a simple example, in a production situation you have to take into account availability and scalability, a low latency service and some security settings. And try to build a CD/CI pipeline, to minimize the effort and time to get each new version of your model ready for your users.

## 💫 ML inference in batch prediction jobs

When we do not need the predictions on demand, in real-time, we can collect many of them, ingest them into a batch job, and send or store the responses to be reviewed or applied later on.

💱 We can reduce costs by running the jobs in a pay-as-you-go style but you need an appropriate scalability strategy to avoid long processing time or even errors.

A simple path to meet this goal:

✍ Create a score script that processes the input data on batches
🚌 Containerized the script and dependencies with docker and push it to a container registry
🕰 Schedules your job to run on a cloud service, like Google Cloud Run, Azure ML endpoint on AKS or ACI, AWS Fargate, etc.
📚 Return responses by giving access to a storage location or calling an API.

There are many requirements to analyze to define a good solution like model size, max time to respond, variations on the count of samples per batch,... It's your responsibility as an engineer to satisfy the requirements while reducing costs and time.

## Homework
You can follow the homework instructions and resolutions in this [link](./homework.md)

# Notes

Notes from previous students:

* [Notes on Model Deployment using Google Cloud Platform, by M. Ayoub C.](https://gist.github.com/Qfl3x/de2a9b98a370749a4b17a4c94ef46185)
* [Week 4: Deployment notes by Waleed](https://github.com/waleedayoub/mlops-zoomcamp/blob/main/cohorts/2023/04-deployment/module4notes.waleed.md)