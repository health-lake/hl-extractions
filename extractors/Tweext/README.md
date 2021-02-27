# Tweext module - v. 0.0.1

Tweext is a tool to extract tweets by a keyword.

## How to use

You need to create a credentials.json file with your Twitter API tokens in the same path of the script:
```json
{
    "consumer_key":"your_consumer_key_here",
    "consumer_secret_key":"your_secret_consumer_key_here",
    "access_token":"your_access_token_here",
    "secret_access_token":"your_secret_access_token_here"
}
```

Because of the S3 Writer operator, you also need to configure your AWS credentials at `awscli`.

After configured, you only need to type few code lines to take your csv directly into S3:
```python
from Tweext import Tweext

# Initializing the class
tweext = Tweext()

# Authenticating...
tweext.authenticate()

# Downloading tweets related to the specific keyword
tweext.start_extraction(keyword = 'vacina')
```

That's all!