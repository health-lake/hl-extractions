# AWS Lambda docker image with Python 3.8
FROM public.ecr.aws/lambda/python:3.8

# Install the requirements
RUN pip install --upgrade pip
RUN pip install tweepy

# Copy files into lambda task root
COPY . .

# Execute the handler
CMD ["app.handler"]