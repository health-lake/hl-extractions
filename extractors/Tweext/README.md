# Tweext module - v. 0.0.1

Tweext is a tool to extract tweets by a keyword.

## How to use

Create credentials.json into the project folder:
```json
{
    "consumer_key":"your_consumer_key_here",
    "consumer_secret_key":"your_secret_consumer_key_here",
    "access_token":"your_access_token_here",
    "secret_access_token":"your_secret_access_token_here"
}
```

Build your docker image:
```
docker build -t image_name .
```

Create a tag:
```
docker tag image_name:latest 123456789012.dkr.ecr.us-east-1.amazonaws.com/image_name:latest
```

Push to ECR:
```
docker push 123456789012.dkr.ecr.us-east-1.amazonaws.com/image_name:latest
```

After that you need to create your AWS Lambda function based on docker image, setting up the environment variables: KEYWORD and LIMIT.