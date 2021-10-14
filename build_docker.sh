#!/usr/bin/bash
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 429201177306.dkr.ecr.us-east-1.amazonaws.com/coletas_s3_ibram
docker image build -t hl_extractions --build-arg AWS_ACCESS_KEY_ID=$1 --build-arg AWS_SECRET_ACCESS_KEY=$2 .
docker tag hl_extractions:latest 429201177306.dkr.ecr.us-east-1.amazonaws.com/coletas_s3_ibram:latest
docker push 429201177306.dkr.ecr.us-east-1.amazonaws.com/coletas_s3_ibram:latest