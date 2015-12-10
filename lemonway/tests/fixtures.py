from lemonway import Lemonway
import string
import random
import os

wl_login = os.getenv("wl_login")
wl_password = os.getenv("wl_password")
location = os.getenv("location")
customer_ip = os.getenv("customer_ip")
IBAN = "DE85111122223333444455"
BIC = "BELADEBEXXX"
default_wallet_id = "0001"

api = Lemonway(wl_login, wl_password, location)

def email_generator():
    email = ''.join(random.choice(string.ascii_lowercase) for _ in range(10))
    return '{}@gmail.com'.format(email)