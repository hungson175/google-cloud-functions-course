# Google Cloud Functions Course
## Starting a project
To start a new project in Google Cloud, we can go to the
[Firebase Console](https://console.firebase.google.com) or
create it from [Google Cloud Platform Console](https://console.cloud.google.com).
## Creating a virtual environment
First we have to install `python3-venv` with:
```
sudo apt install python3-venv
```
Then, we create the virtual environment:
```
python3 -m venv venv
```
To activate the virtual environment:
```
source venv/bin/activate
```
Then, we can add dependencies (packages) by putting them
in a `requirements.txt` file and we then install them with:
```
pip install -r requirements.txt
```
Testing the function locally, with example:
```
functions-framework --target [FUNCTION_NAME] --debug
functions-framework --target hello_world
```


## Deploying our functions
First, we have to set our project ID with the following 
command:
```
gcloud config set project [YOUR_PROJECT_ID]
```
Then we deploy our function with this command:
```
gcloud functions deploy [FUNCTION_NAME] --runtime python310 --trigger-http
```
Deloy and force region:
```shell
gcloud functions deploy [FUNCTION_NAME] --runtime python310 --trigger-http --region [REGION]
gcloud functions deploy hello_me --runtime python310 --trigger-http --region asia-southeast1
```
List all functions with:
```
gcloud functions list
```
Show information about the current project:
```
gcloud config list
```

## Deploying cloud functions with environment variables and other dependencies
We have to create a `.env.yaml` file and a `requirements.txt` file
in the same directory of our `main.py` and then run
the following command:
```
gcloud functions deploy [FUNCTION_NAME] --env-vars-file .env.yaml --runtime python37 --trigger-http
```
## Schedule Cloud Functions
We execute the following commands:
```
gcloud components install beta
gcloud components update
gcloud pubsub topics create [TOPIC_NAME]
gcloud pubsub subscriptions create cron-sub --topic [TOPIC_NAME]
```
## Deleting a Cloud Function
To delete a Cloud Function run the following command:
```
gcloud functions delete [FUNCTION_NAME]
```