__author__ = 'steph'
from base_test import *

w = api.register_wallet(wallet='0045',
                        client_first_name='stephane',
                        client_last_name='planquart',
                        ctry='FRA',
                        phone_number='0123456789',
                        client_mail='s.planquart@payplug.com',
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
info = api.get_money_in_trans_details(wallet_ip='8.8.8.8', transaction_merchant_token='2012')

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

r = api.refund_money_in(transaction_id=13, wallet_ip=customer_ip)

iban = api.register_iban(wallet='splanquart+159@payplug.com', wallet_ip=customer_ip,
                         holder=u'Stéphane Planquart',
                         bic='CMCIFR2A',
                         iban='FR7615489047020008783080178',
                         dom1=u'Pierre Dev € avec un super long',
                         dom2='6 Impasse de la Jaurie')

bk = api.money_out(wallet='splanquart+159@payplug.com',
                   wallet_ip=customer_ip,
                   amount_tot='1.00',
                   iban_id=str(iban.id),
                   auto_commission='0')

f = open('files/Kbis.pdf', 'rb')
buffer = f.read(4*1024*1024)
from base64 import b64encode
buffer64 = b64encode(buffer)

r = api.upload_file(wallet='splanquart+159@payplug.com',
                    wallet_ip=customer_ip,
                    file_name='Kbis.pdf',
                    type='7',
                    buffer=buffer64)
from time import time
t = int(time()) - 24*3600
c = api.get_kyc_status(update_date=t, wallet_ip=customer_ip)


#money_in
m = api.money_in(wallet_ip=customer_ip,
                 wallet='splanquart+159@payplug.com',
                 amount_tot='10.00',
                 amount_com='0.30',
                 card_number='5017670000001800',
                 card_type='2',
                 card_crypto='400',
                 card_date='12/2016'
                 )

m = api.money_in_3d_init(wallet_ip=customer_ip,
                         wallet='splanquart+159@payplug.com',
                         amount_tot='10.00',
                         amount_com='0.30',
                         card_number='5017670000001800',
                         card_type='2',
                         card_code='400',
                         card_date='12/2016',
                         return_url='http://localhost/',
                         wk_token=token
                         )

gm = api.money_in_3d_confirm(wallet_ip=customer_ip,
                             transaction_id=149,
                             md='C456A5201DB0E4FA1E42389A9424EC39.C9324F789C3F437B8E2553778A2513298C'
                             )
