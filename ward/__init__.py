from . import _ward
import atexit

ward = _ward.Ward()
atexit.register(ward.draw)
