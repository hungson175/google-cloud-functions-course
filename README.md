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

## Setup static IP for the Cloud Functions

### Enable the necessary APIs:
```shell
# Enable Cloud Functions API
gcloud services enable cloudfunctions.googleapis.com

# Enable VPC Access API
gcloud services enable vpcaccess.googleapis.com

# Enable Compute Engine API (required for Cloud NAT)
gcloud services enable compute.googleapis.com
```

### Create a VPC and Subnet
```shell
# Create a new VPC network
gcloud compute networks create YOUR_VPC_NAME --subnet-mode=custom

# Create a new subnet in the VPC
gcloud compute networks subnets create YOUR_SUBNET_NAME \
    --network=YOUR_VPC_NAME \
    --region=YOUR_REGION \
    --range=YOUR_CIDR_RANGE
```
YOUR_CIDR_RANGE: The IP address range in CIDR format for the subnet, e.g., 10.0.0.0/24

### Set Up a Serverless VPC Access Connector
```shell
gcloud compute networks vpc-access connectors create [CONNECTOR_NAME] --region [REGION] --network [VPC_NAME] --range [IP_RANGE]
```

[IP_RANGE] with an IP range in CIDR notation that is reserved for the connector within the subnet’s range. 
E.g: 10.8.0.0/28

### Configure Cloud NAT
```shell
# Create a Cloud Router
gcloud compute routers create [ROUTER_NAME] --region [REGION] --network [VPC_NAME]

# Reserve a static IP address for Cloud NAT
gcloud compute addresses create bot-sample-external-ip --project=binance-bot-sample --description=bot-sample-external-ip --region=asia-southeast1

# Configure Cloud NAT to use the static IP:
gcloud compute routers nats create bot-sample-nat \
  --router bot-sample-router \
  --region asia-southeast1 \
  --nat-all-subnet-ip-ranges \
  --nat-external-ip-pool bot-sample-external-ip
```

### Deploy the Cloud Function
```shell
gcloud functions deploy [FUNCTION_NAME] \
--runtime python310 \
--trigger-http \
--vpc-connector bot-sample-connector 
```

