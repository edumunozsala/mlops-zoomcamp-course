# MLOps Zoomcamp Course Cohort 2024

### 2024 Cohort

### Objective

Learn practical aspects of productionizing ML services — from training and experimenting to model deployment and monitoring.

### Target audience

Data scientists and ML engineers. Also software engineers and data engineers interested in learning about putting ML in production.

### Pre-requisites

* Python
* Docker
* Being comfortable with command line 
* Prior exposure to machine learning (at work or from other courses, e.g. from [ML Zoomcamp](https://github.com/alexeygrigorev/mlbookcamp-code/tree/master/course-zoomcamp))
* Prior programming experience (at least 1+ year)

## Syllabus

### [Module 1: Introduction](Module01)

* What is MLOps
* MLOps maturity model
* Running example: NY Taxi trips dataset
* Why do we need MLOps
* Course overview
* Environment preparation
* Homework

[More details](Module01)

### [Module 2: Experiment tracking and model management](Module02)

* Experiment tracking intro
* Getting started with MLflow
* Experiment tracking with MLflow
* Saving and loading models with MLflow
* Model registry
* MLflow in practice
* Homework

[More details](02-experiment-tracking)


### [Module 3: Orchestration and ML Pipelines]

* Workflow orchestration
* Mage

[More details](03-orchestration)


### [Module 4: Model Deployment]

* Three ways of model deployment: Online (web and streaming) and offline (batch)
* Web service: model deployment with Flask
* Streaming: consuming events with AWS Kinesis and Lambda
* Batch: scoring data offline
* Homework

[More details](04-deployment)


### [Module 5: Model Monitoring]

* Monitoring ML-based services
* Monitoring web services with Prometheus, Evidently, and Grafana
* Monitoring batch jobs with Prefect, MongoDB, and Evidently

[More details](05-monitoring)


### [Module 6: Best Practices]

* Testing: unit, integration
* Python: linting and formatting
* Pre-commit hooks and makefiles
* CI/CD (GitHub Actions)
* Infrastructure as code (Terraform)
* Homework

[More details](06-best-practices)

### [Project]

* End-to-end project with all the things above

[More details](07-project/)

## License

Copyright 2024 Eduardo Muñoz

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
