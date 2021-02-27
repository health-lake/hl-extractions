# -*- coding: utf-8 -*-

from Tweext import Tweext
import time

# Function to be called on AWS Lambda
def handler(event, context):
    # Start time counting
    init = time.time()

    # Initialize the class
    tweext = Tweext()

    # Authenticating...
    tweext.authenticate()

    # Download the least 100 tweets about 'vacina'
    tweext.start_extraction(
        keyword = 'vacina',
        limit = 100
    )

    # Stop time counting
    end = time.time()

    return "Process finished in {}".format(end-init)