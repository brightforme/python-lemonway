__author__ = 'steph'
from lemonway.api import Lemonway
import logging
import sys

root = logging.getLogger()
root.setLevel(logging.DEBUG)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
root.addHandler(ch)

location = 'https://ws.lemonway.fr/mb/payplug/dev/directkit/service.asmx'
wl_login = 'society'
wl_password = '123456'

api = Lemonway(wl_login, wl_password, location)

w = api.register_wallet(wallet='0045',
                        client_first_name='stephane',
                        client_last_name='planquart',
                        ctry='FRA',
                        phone_number='0123456789',
                        client_mail='s.planquart@payplug.fr',
                        client_title='M',
                        wallet_ip='8.8.8.8'
                        )

wsc = api.get_wallet_details(wallet='SC',
                             wallet_ip='8.8.8.8'
                             )

pay = api.get_money_in_trans_details(wallet_ip='8.8.8.8', transaction_id=3)