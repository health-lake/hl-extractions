# AWS Lambda docker image with Python 3.8
FROM public.ecr.aws/lambda/python:3.8

# Copy files into lambda task root
COPY utils/ ./
COPY app.py Tweext.py credentials.json ./

# Execute the handler
CMD ["app.handler"]