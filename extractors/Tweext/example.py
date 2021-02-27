from Tweext import Tweext
import time

init = time.time()
tweext = Tweext()
tweext.authenticate()
tweext.start_extraction(keyword = 'vacina')
end = time.time()

print('Executed in {}'.format(end-init))