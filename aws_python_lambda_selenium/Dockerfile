# Set up Python AWS Lambda docker image with Selenium

# Download the base image
FROM public.ecr.aws/lambda/python:3.8

# Define some global args
ARG MAIN_FILE='main.py'
ARG FUNCTION_ROOT='.'

# Define workdir path
WORKDIR ${FUNCTION_ROOT}

# Copy files into function root
COPY ${MAIN_FILE} ${FUNCTION_ROOT}

# Set root user
USER root

# Install selenium
RUN python3.8 -m pip install --upgrade pip
RUN python3.8 -m pip install selenium

# Install chromium browser
RUN yum -y upgrade
RUN yum install -y curl unzip
RUN curl https://intoli.com/install-google-chrome.sh | bash

# Download chromedriver
RUN wget https://chromedriver.storage.googleapis.com/87.0.4280.88/chromedriver_linux64.zip
RUN unzip ./chromedriver_linux64.zip
RUN rm ./chromedriver_linux64.zip
RUN mv -f ./chromedriver /usr/local/bin/chromedriver
RUN chmod 755 /usr/local/bin/chromedriver
RUN export PATH=$PATH:/usr/local/bin/chromedriver.exe

# Set CMD of handler
CMD [ "main.lambda_handler" ]