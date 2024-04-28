# Google cloud functions course
## Introduction
This repository contains the code for the Google Cloud Functions course on Udemy. The course is designed to teach you how to build serverless applications using Google Cloud Functions. The course covers the following topics:
- Introduction to serverless computing
- Introduction to Google Cloud Functions
- Setting up Google Cloud Functions
- Deploying Google Cloud Functions
- Triggering Google Cloud Functions
- Monitoring Google Cloud Functions
- Testing Google Cloud Functions
- Securing Google Cloud Functions
- Building a serverless application

## Steps

### Setup environment
Create virtual enviroment
```python3 -m venv venv```

Activate virtual enviroment
```source venv/bin/activate```

Add requirements file requirements.txt

Install dependencies, only execute it in virtual environment (venv)
```pip install -r requirements.txt```

### Setup Google Cloud
- First install [Google Cloud SDK](https://cloud.google.com/sdk/docs/downloads-versioned-archives)

- Initialize Google Cloud SDK
```gcloud init```

- Select project
```gcloud config set project <project_id>```
e.g:
  ```gcloud config set project cloud-cloud-functions-course-421703```

- Deploy function
```gcloud functions deploy hello_world --runtime python310 --trigger-http```
