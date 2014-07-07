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
payplug_url = 'https://www.dev.payplug.fr/p/lemonway_return_test'
token = '123467890'
customer_ip = '194.254.61.161'

api = Lemonway(wl_login, wl_password, location)

w = api.register_wallet(wallet='0045',
                        client_first_name='stephane',
                        client_last_name='planquart',
                        ctry='FRA',
                        phone_number='0123456789',
                        client_mail='s.planquart@payplug.fr',
                        client_title='M',
                        wallet_ip=customer_ip
                        )

wsc = api.get_wallet_details(wallet='SC',
                             wallet_ip=customer_ip
                             )

payed = api.get_money_in_trans_details(wallet_ip=customer_ip, transaction_id=3)

to_pay = api.money_in_web_init(wk_token=token,
                               wallet='0014',
                               amount_tot='10.00',
                               amount_com='10.00',
                               return_url=payplug_url,
                               error_url=payplug_url,
                               cancel_url=payplug_url,
                               wallet_ip=customer_ip
                               )
url = generate_webkit_url(webkit_url, to_pay.token)
info = api.get_money_in_trans_details(wallet_ip=customer_ip, transaction_id=13)
info = api.get_money_in_trans_details(wallet_ip='8.8.8.8', transaction_merchant_token=token)

m = api.money_in_web_init(wk_token=token,
                          wallet='0014',
                          amount_tot='10.00',
                          amount_com='9.70',
                          return_url=payplug_url,
                          error_url=payplug_url,
                          cancel_url=payplug_url,
                          auto_commission=0,
                          version='1.1',
                          wallet_ip=customer_ip,
                          wallet_ua=None,
                          comment=None,
                          use_registered_card=0)

r = api.refund_money_in(transaction_id=13,wallet_ip=customer_ip)