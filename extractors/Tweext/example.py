from Tweext import Tweext
import time

# Initializing time counting
init = time.time()

# Initializing the class
tweext = Tweext()

# Authenticating...
tweext.authenticate()

# Downloading tweets related to the specific keyword
tweext.start_extraction(keyword = 'vacina')

# Time counting finished
end = time.time()
print('Executed in {}'.format(end-init))