# -*- coding: utf-8 -*-

import time
import os
from Tweext import Tweext

# Function to be called on AWS Lambda
def handler(event, context):
    # Start time counting
    init = time.time()

    # Initialize the class
    tweext = Tweext()

    # Authenticating...
    tweext.authenticate()

    # Download the last LIMIT tweets about KEYWORD | Note that KEYWORD and LIMIT are environment variables declared at AWS Lambda
    keyword = os.environ['KEYWORD']
    limit = int(os.environ['LIMIT'])
    tweext.start_extraction(
        keyword = keyword,
        limit = limit
    )

    # Stop time counting
    end = time.time()

    return "Process finished in {}".format(end-init)