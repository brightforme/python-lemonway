__author__ = 'steph'
from lemonway.api import Lemonway
import logging
import sys
from lemonway.utils import generate_webkit_url

root = logging.getLogger()
root.setLevel(logging.INFO)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
root.addHandler(ch)

location = 'https://ws.lemonway.fr/mb/payplug/dev/directkit/service.asmx'
wl_login = 'society'
wl_password = '123456'
webkit_url = 'https://m.lemonway.fr/mb/payplug/dev/'
payplug_url = 'https://www.dev.payplug.com/p/lemonway_return_test'
token = '123467890'
customer_ip = '194.254.61.161'

api = Lemonway(wl_login, wl_password, location)