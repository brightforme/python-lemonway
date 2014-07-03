# -*- coding: utf-8 -*-
import logging
import os
from lemonway.exceptions import APIException
from suds.client import Client
from time import strftime


logger = logging.getLogger('lemonway')


class ComplexType(object):
    def __init__(self, args):
        self.__dict__.update(args)
        del self.self

    def __str__(self):
        return str({k: v for k, v in self.__dict__.items()
                    if not k.startswith('_')})

    @property
    def soap_dict(self):
        return {v: getattr(self, k) for k, v in self._tr_params.items()}


class Lemonway(object):
    SANDBOX_LOCATION = ''
    PRODUCTION_LOCATION = ''
    WSDL_URL = ('file://' + os.path.dirname(os.path.realpath(__file__))
                + '/lemonway.wsdl')

    def __init__(self, merchant_id, access_key, production=False):
        self.merchant_id = merchant_id
        self.access_key = access_key
        if not production:
            self._location = self.SANDBOX_LOCATION
        else:
            self._location = self.PRODUCTION_LOCATION
        self._client = Client(self.WSDL_URL, cachingpolicy=1,
            username=self.merchant_id, password=self.access_key)
        self._client.options.cache.setduration(days=90)

    def ws_request(self, method, api_name, **params):
        self._client.set_options(location=self._location + api_name)
        logger.info('Calling %s method with params: %s' % (method, params))
        try:
            answer = getattr(self._client.service[api_name][api_name], method)(**params)
        except Exception as e:
            raise APIException(e.message)
        #if hasattr(answer, 'result') and answer.result.code != '00000':
        #    logger.error('Error while calling %s method with params: %s' % (method, params))
        #    raise APIException(answer)
        return answer

    def soap_dict(self, complex_type):
        return complex_type.soap_dict if complex_type else None

    def create_gift_code_amazon(self, debit_wallet, amount_agcod, wl_login,
            wl_pass, language, wallet_ip, wallet_ua):
        """
        :type debit_wallet: String
        :type amount_agcod: String
        :type wl_login: String
        :type wl_pass: String
        :type language: String
        :type wallet_ip: String
        :type wallet_ua: String
        """
        return self.ws_request('CreateGiftCodeAmazon', 'Service_mb',
            debitWallet=debit_wallet, amountAGCOD=amount_agcod,
            wlLogin=wl_login, wlPass=wl_pass, language=language,
            walletIp=wallet_ip, walletUa=wallet_ua, version=3)

    def fast_pay(self, client_mail, client_title, client_first_name,
            client_last_name, card_type, card_number, card_crypto, card_date,
            credit_wallet, amount, message, auto_commission, register_card,
            wl_login, wl_pass, language, wallet_ip, wallet_ua):
        """
        :type client_mail: String
        :type client_title: String
        :type client_first_name: String
        :type client_last_name: String
        :type card_type: String
        :type card_number: String
        :type card_crypto: String
        :type card_date: String
        :type credit_wallet: String
        :type amount: String
        :type message: String
        :type auto_commission: String
        :type register_card: String
        :type wl_login: String
        :type wl_pass: String
        :type language: String
        :type wallet_ip: String
        :type wallet_ua: String
        """
        return self.ws_request('FastPay', 'Service_mb', clientMail=client_mail,
            clientTitle=client_title, clientFirstName=client_first_name,
            clientLastName=client_last_name, cardType=card_type,
            cardNumber=card_number, cardCrypto=card_crypto, cardDate=card_date,
            creditWallet=credit_wallet, amount=amount, message=message,
            autoCommission=auto_commission, registerCard=register_card,
            wlLogin=wl_login, wlPass=wl_pass, language=language,
            walletIp=wallet_ip, walletUa=wallet_ua, version=3)

    def get_balances(self, update_date, wl_login, wl_pass, language, wallet_ip,
            wallet_ua):
        """
        :type update_date: String
        :type wl_login: String
        :type wl_pass: String
        :type language: String
        :type wallet_ip: String
        :type wallet_ua: String
        """
        return self.ws_request('GetBalances', 'Service_mb',
            updateDate=update_date, wlLogin=wl_login, wlPass=wl_pass,
            language=language, walletIp=wallet_ip, walletUa=wallet_ua,
            version=3)

    def get_kyc_status(self, update_date, wl_login, wl_pass, language,
            wallet_ip, wallet_ua):
        """
        :type update_date: String
        :type wl_login: String
        :type wl_pass: String
        :type language: String
        :type wallet_ip: String
        :type wallet_ua: String
        """
        return self.ws_request('GetKycStatus', 'Service_mb',
            updateDate=update_date, wlLogin=wl_login, wlPass=wl_pass,
            language=language, walletIp=wallet_ip, walletUa=wallet_ua,
            version=3)

    def get_money_in_iban_details(self, update_date, wl_login, wl_pass,
            language, wallet_ip, wallet_ua):
        """
        :type update_date: String
        :type wl_login: String
        :type wl_pass: String
        :type language: String
        :type wallet_ip: String
        :type wallet_ua: String
        """
        return self.ws_request('GetMoneyInIBANDetails', 'Service_mb',
            updateDate=update_date, wlLogin=wl_login, wlPass=wl_pass,
            language=language, walletIp=wallet_ip, walletUa=wallet_ua,
            version=3)

    def get_money_in_trans_details(self, transaction_id, transaction_comment,
            transaction_merchant_token, wl_login, wl_pass, language, wallet_ip,
            wallet_ua):
        """
        :type transaction_id: String
        :type transaction_comment: String
        :type transaction_merchant_token: String
        :type wl_login: String
        :type wl_pass: String
        :type language: String
        :type wallet_ip: String
        :type wallet_ua: String
        """
        return self.ws_request('GetMoneyInTransDetails', 'Service_mb',
            transactionId=transaction_id,
            transactionComment=transaction_comment,
            transactionMerchantToken=transaction_merchant_token,
            wlLogin=wl_login, wlPass=wl_pass, language=language,
            walletIp=wallet_ip, walletUa=wallet_ua, version=3)

    def get_money_out_trans_details(self, transaction_id, transaction_comment,
            wl_login, wl_pass, language, wallet_ip, wallet_ua):
        """
        :type transaction_id: String
        :type transaction_comment: String
        :type wl_login: String
        :type wl_pass: String
        :type language: String
        :type wallet_ip: String
        :type wallet_ua: String
        """
        return self.ws_request('GetMoneyOutTransDetails', 'Service_mb',
            transactionId=transaction_id,
            transactionComment=transaction_comment, wlLogin=wl_login,
            wlPass=wl_pass, language=language, walletIp=wallet_ip,
            walletUa=wallet_ua, version=3)

    def get_payment_details(self, transaction_id, transaction_comment,
            wl_login, wl_pass, language, wallet_ip, wallet_ua):
        """
        :type transaction_id: String
        :type transaction_comment: String
        :type wl_login: String
        :type wl_pass: String
        :type language: String
        :type wallet_ip: String
        :type wallet_ua: String
        """
        return self.ws_request('GetPaymentDetails', 'Service_mb',
            transactionId=transaction_id,
            transactionComment=transaction_comment, wlLogin=wl_login,
            wlPass=wl_pass, language=language, walletIp=wallet_ip,
            walletUa=wallet_ua, version=3)

    def get_wallet_details(self, wallet, wl_login, wl_pass, language,
            wallet_ip, wallet_ua):
        """
        :type wallet: String
        :type wl_login: String
        :type wl_pass: String
        :type language: String
        :type wallet_ip: String
        :type wallet_ua: String
        """
        return self.ws_request('GetWalletDetails', 'Service_mb', wallet=wallet,
            wlLogin=wl_login, wlPass=wl_pass, language=language,
            walletIp=wallet_ip, walletUa=wallet_ua, version=3)

    def money_in(self, wallet, amount_tot, amount_com, comment, card_type,
            card_number, card_crypto, card_date, auto_commission, wl_login,
            wl_pass, language, wallet_ip, wallet_ua):
        """
        :type wallet: String
        :type amount_tot: String
        :type amount_com: String
        :type comment: String
        :type card_type: String
        :type card_number: String
        :type card_crypto: String
        :type card_date: String
        :type auto_commission: String
        :type wl_login: String
        :type wl_pass: String
        :type language: String
        :type wallet_ip: String
        :type wallet_ua: String
        """
        return self.ws_request('MoneyIn', 'Service_mb', wallet=wallet,
            amountTot=amount_tot, amountCom=amount_com, comment=comment,
            cardType=card_type, cardNumber=card_number, cardCrypto=card_crypto,
            cardDate=card_date, autoCommission=auto_commission,
            wlLogin=wl_login, wlPass=wl_pass, language=language,
            walletIp=wallet_ip, walletUa=wallet_ua, version=3)

    def money_in3_d_authenticate(self, transaction_id, md, pa_res, card_type,
            card_number, card_code, card_date, wl_login, wl_pass, language,
            wallet_ip, wallet_ua):
        """
        :type transaction_id: String
        :type md: String
        :type pa_res: String
        :type card_type: String
        :type card_number: String
        :type card_code: String
        :type card_date: String
        :type wl_login: String
        :type wl_pass: String
        :type language: String
        :type wallet_ip: String
        :type wallet_ua: String
        """
        return self.ws_request('MoneyIn3DAuthenticate', 'Service_mb',
            transactionId=transaction_id, MD=md, PaRes=pa_res,
            cardType=card_type, cardNumber=card_number, cardCode=card_code,
            cardDate=card_date, wlLogin=wl_login, wlPass=wl_pass,
            language=language, walletIp=wallet_ip, walletUa=wallet_ua,
            version=3)

    def money_in3_d_confirm(self, transaction_id, md, pa_res, card_type,
            card_number, card_code, card_date, wl_login, wl_pass, language,
            wallet_ip, wallet_ua):
        """
        :type transaction_id: String
        :type md: String
        :type pa_res: String
        :type card_type: String
        :type card_number: String
        :type card_code: String
        :type card_date: String
        :type wl_login: String
        :type wl_pass: String
        :type language: String
        :type wallet_ip: String
        :type wallet_ua: String
        """
        return self.ws_request('MoneyIn3DConfirm', 'Service_mb',
            transactionId=transaction_id, MD=md, PaRes=pa_res,
            cardType=card_type, cardNumber=card_number, cardCode=card_code,
            cardDate=card_date, wlLogin=wl_login, wlPass=wl_pass,
            language=language, walletIp=wallet_ip, walletUa=wallet_ua,
            version=3)

    def money_in3_d_init(self, wk_token, wallet, amount_tot, amount_com,
            comment, card_type, card_number, card_code, card_date,
            auto_commission, return_url, wl_login, wl_pass, language,
            wallet_ip, wallet_ua):
        """
        :type wk_token: String
        :type wallet: String
        :type amount_tot: String
        :type amount_com: String
        :type comment: String
        :type card_type: String
        :type card_number: String
        :type card_code: String
        :type card_date: String
        :type auto_commission: String
        :type return_url: String
        :type wl_login: String
        :type wl_pass: String
        :type language: String
        :type wallet_ip: String
        :type wallet_ua: String
        """
        return self.ws_request('MoneyIn3DInit', 'Service_mb', wkToken=wk_token,
            wallet=wallet, amountTot=amount_tot, amountCom=amount_com,
            comment=comment, cardType=card_type, cardNumber=card_number,
            cardCode=card_code, cardDate=card_date,
            autoCommission=auto_commission, returnUrl=return_url,
            wlLogin=wl_login, wlPass=wl_pass, language=language,
            walletIp=wallet_ip, walletUa=wallet_ua, version=3)

    def money_in_validate(self, transaction_id, wl_login, wl_pass, language,
            wallet_ip, wallet_ua):
        """
        :type transaction_id: String
        :type wl_login: String
        :type wl_pass: String
        :type language: String
        :type wallet_ip: String
        :type wallet_ua: String
        """
        return self.ws_request('MoneyInValidate', 'Service_mb',
            transactionId=transaction_id, wlLogin=wl_login, wlPass=wl_pass,
            language=language, walletIp=wallet_ip, walletUa=wallet_ua,
            version=3)

    def money_in_web_init(self, wk_token, wallet, amount_tot, amount_com,
            comment, use_registered_card, return_url, cancel_url, error_url,
            auto_commission, wl_login, wl_pass, language, wallet_ip,
            wallet_ua):
        """
        :type wk_token: String
        :type wallet: String
        :type amount_tot: String
        :type amount_com: String
        :type comment: String
        :type use_registered_card: String
        :type return_url: String
        :type cancel_url: String
        :type error_url: String
        :type auto_commission: String
        :type wl_login: String
        :type wl_pass: String
        :type language: String
        :type wallet_ip: String
        :type wallet_ua: String
        """
        return self.ws_request('MoneyInWebInit', 'Service_mb',
            wkToken=wk_token, wallet=wallet, amountTot=amount_tot,
            amountCom=amount_com, comment=comment,
            useRegisteredCard=use_registered_card, returnUrl=return_url,
            cancelUrl=cancel_url, errorUrl=error_url,
            autoCommission=auto_commission, wlLogin=wl_login, wlPass=wl_pass,
            language=language, walletIp=wallet_ip, walletUa=wallet_ua,
            version=3)

    def money_in_with_card_id(self, wallet, amount_tot, amount_com, comment,
            card_id, auto_commission, wl_login, wl_pass, language, wallet_ip,
            wallet_ua):
        """
        :type wallet: String
        :type amount_tot: String
        :type amount_com: String
        :type comment: String
        :type card_id: String
        :type auto_commission: String
        :type wl_login: String
        :type wl_pass: String
        :type language: String
        :type wallet_ip: String
        :type wallet_ua: String
        """
        return self.ws_request('MoneyInWithCardId', 'Service_mb',
            wallet=wallet, amountTot=amount_tot, amountCom=amount_com,
            comment=comment, cardId=card_id, autoCommission=auto_commission,
            wlLogin=wl_login, wlPass=wl_pass, language=language,
            walletIp=wallet_ip, walletUa=wallet_ua, version=3)

    def money_out(self, wallet, iban_id, amount_tot, amount_com, message,
            auto_commission, wl_login, wl_pass, language, wallet_ip,
            wallet_ua):
        """
        :type wallet: String
        :type iban_id: String
        :type amount_tot: String
        :type amount_com: String
        :type message: String
        :type auto_commission: String
        :type wl_login: String
        :type wl_pass: String
        :type language: String
        :type wallet_ip: String
        :type wallet_ua: String
        """
        return self.ws_request('MoneyOut', 'Service_mb', wallet=wallet,
            ibanId=iban_id, amountTot=amount_tot, amountCom=amount_com,
            message=message, autoCommission=auto_commission, wlLogin=wl_login,
            wlPass=wl_pass, language=language, walletIp=wallet_ip,
            walletUa=wallet_ua, version=3)

    def refund_money_in(self, transaction_id, amount_to_refund, comment,
            wl_login, wl_pass, language, wallet_ip, wallet_ua):
        """
        :type transaction_id: String
        :type amount_to_refund: String
        :type comment: String
        :type wl_login: String
        :type wl_pass: String
        :type language: String
        :type wallet_ip: String
        :type wallet_ua: String
        """
        return self.ws_request('RefundMoneyIn', 'Service_mb',
            transactionId=transaction_id, amountToRefund=amount_to_refund,
            comment=comment, wlLogin=wl_login, wlPass=wl_pass,
            language=language, walletIp=wallet_ip, walletUa=wallet_ua,
            version=3)

    def register_card(self, wallet, card_type, card_number, card_code,
            card_date, wl_login, wl_pass, language, wallet_ip, wallet_ua):
        """
        :type wallet: String
        :type card_type: String
        :type card_number: String
        :type card_code: String
        :type card_date: String
        :type wl_login: String
        :type wl_pass: String
        :type language: String
        :type wallet_ip: String
        :type wallet_ua: String
        """
        return self.ws_request('RegisterCard', 'Service_mb', wallet=wallet,
            cardType=card_type, cardNumber=card_number, cardCode=card_code,
            cardDate=card_date, wlLogin=wl_login, wlPass=wl_pass,
            language=language, walletIp=wallet_ip, walletUa=wallet_ua,
            version=3)

    def register_iban(self, wallet, holder, bic, iban, dom1, dom2, wl_login,
            wl_pass, language, wallet_ip, wallet_ua):
        """
        :type wallet: String
        :type holder: String
        :type bic: String
        :type iban: String
        :type dom1: String
        :type dom2: String
        :type wl_login: String
        :type wl_pass: String
        :type language: String
        :type wallet_ip: String
        :type wallet_ua: String
        """
        return self.ws_request('RegisterIBAN', 'Service_mb', wallet=wallet,
            holder=holder, bic=bic, iban=iban, dom1=dom1, dom2=dom2,
            wlLogin=wl_login, wlPass=wl_pass, language=language,
            walletIp=wallet_ip, walletUa=wallet_ua, version=3)

    def register_wallet(self, wallet, client_mail, client_title,
            client_first_name, client_last_name, ctry, phone_number, wl_login,
            wl_pass, language, wallet_ip, wallet_ua):
        """
        :type wallet: String
        :type client_mail: String
        :type client_title: String
        :type client_first_name: String
        :type client_last_name: String
        :type ctry: String
        :type phone_number: String
        :type wl_login: String
        :type wl_pass: String
        :type language: String
        :type wallet_ip: String
        :type wallet_ua: String
        """
        return self.ws_request('RegisterWallet', 'Service_mb', wallet=wallet,
            clientMail=client_mail, clientTitle=client_title,
            clientFirstName=client_first_name, clientLastName=client_last_name,
            ctry=ctry, phoneNumber=phone_number, wlLogin=wl_login,
            wlPass=wl_pass, language=language, walletIp=wallet_ip,
            walletUa=wallet_ua, version=3)

    def send_payment(self, debit_wallet, credit_wallet, amount, message,
            wl_login, wl_pass, language, wallet_ip, wallet_ua):
        """
        :type debit_wallet: String
        :type credit_wallet: String
        :type amount: String
        :type message: String
        :type wl_login: String
        :type wl_pass: String
        :type language: String
        :type wallet_ip: String
        :type wallet_ua: String
        """
        return self.ws_request('SendPayment', 'Service_mb',
            debitWallet=debit_wallet, creditWallet=credit_wallet,
            amount=amount, message=message, wlLogin=wl_login, wlPass=wl_pass,
            language=language, walletIp=wallet_ip, walletUa=wallet_ua,
            version=3)

    def unregister_card(self, wallet, card_id, wl_login, wl_pass, language,
            wallet_ip, wallet_ua):
        """
        :type wallet: String
        :type card_id: String
        :type wl_login: String
        :type wl_pass: String
        :type language: String
        :type wallet_ip: String
        :type wallet_ua: String
        """
        return self.ws_request('UnregisterCard', 'Service_mb', wallet=wallet,
            cardId=card_id, wlLogin=wl_login, wlPass=wl_pass,
            language=language, walletIp=wallet_ip, walletUa=wallet_ua,
            version=3)

    def update_wallet_details(self, wallet, new_email, new_title,
            new_first_name, new_last_name, new_ctry, new_ip, new_phone_number,
            wl_login, wl_pass, language, wallet_ip, wallet_ua):
        """
        :type wallet: String
        :type new_email: String
        :type new_title: String
        :type new_first_name: String
        :type new_last_name: String
        :type new_ctry: String
        :type new_ip: String
        :type new_phone_number: String
        :type wl_login: String
        :type wl_pass: String
        :type language: String
        :type wallet_ip: String
        :type wallet_ua: String
        """
        return self.ws_request('UpdateWalletDetails', 'Service_mb',
            wallet=wallet, newEmail=new_email, newTitle=new_title,
            newFirstName=new_first_name, newLastName=new_last_name,
            newCtry=new_ctry, newIp=new_ip, newPhoneNumber=new_phone_number,
            wlLogin=wl_login, wlPass=wl_pass, language=language,
            walletIp=wallet_ip, walletUa=wallet_ua, version=3)

    def upload_file(self, wallet, file_name, type, buffer, wl_login, wl_pass,
            language, wallet_ip, wallet_ua):
        """
        :type wallet: String
        :type file_name: String
        :type type: String
        :type buffer: Base64Binary
        :type wl_login: String
        :type wl_pass: String
        :type language: String
        :type wallet_ip: String
        :type wallet_ua: String
        """
        buffer = self.soap_dict(buffer)
        return self.ws_request('UploadFile', 'Service_mb', wallet=wallet,
            fileName=file_name, type=type, buffer=buffer, wlLogin=wl_login,
            wlPass=wl_pass, language=language, walletIp=wallet_ip,
            walletUa=wallet_ua, version=3)

    def create_gift_code_amazon(self, debit_wallet, amount_agcod, wl_login,
            wl_pass, language, wallet_ip, wallet_ua):
        """
        :type debit_wallet: String
        :type amount_agcod: String
        :type wl_login: String
        :type wl_pass: String
        :type language: String
        :type wallet_ip: String
        :type wallet_ua: String
        """
        return self.ws_request('CreateGiftCodeAmazon', 'Service_mb',
            debitWallet=debit_wallet, amountAGCOD=amount_agcod,
            wlLogin=wl_login, wlPass=wl_pass, language=language,
            walletIp=wallet_ip, walletUa=wallet_ua, version=3)

    def fast_pay(self, client_mail, client_title, client_first_name,
            client_last_name, card_type, card_number, card_crypto, card_date,
            credit_wallet, amount, message, auto_commission, register_card,
            wl_login, wl_pass, language, wallet_ip, wallet_ua):
        """
        :type client_mail: String
        :type client_title: String
        :type client_first_name: String
        :type client_last_name: String
        :type card_type: String
        :type card_number: String
        :type card_crypto: String
        :type card_date: String
        :type credit_wallet: String
        :type amount: String
        :type message: String
        :type auto_commission: String
        :type register_card: String
        :type wl_login: String
        :type wl_pass: String
        :type language: String
        :type wallet_ip: String
        :type wallet_ua: String
        """
        return self.ws_request('FastPay', 'Service_mb', clientMail=client_mail,
            clientTitle=client_title, clientFirstName=client_first_name,
            clientLastName=client_last_name, cardType=card_type,
            cardNumber=card_number, cardCrypto=card_crypto, cardDate=card_date,
            creditWallet=credit_wallet, amount=amount, message=message,
            autoCommission=auto_commission, registerCard=register_card,
            wlLogin=wl_login, wlPass=wl_pass, language=language,
            walletIp=wallet_ip, walletUa=wallet_ua, version=3)

    def get_balances(self, update_date, wl_login, wl_pass, language, wallet_ip,
            wallet_ua):
        """
        :type update_date: String
        :type wl_login: String
        :type wl_pass: String
        :type language: String
        :type wallet_ip: String
        :type wallet_ua: String
        """
        return self.ws_request('GetBalances', 'Service_mb',
            updateDate=update_date, wlLogin=wl_login, wlPass=wl_pass,
            language=language, walletIp=wallet_ip, walletUa=wallet_ua,
            version=3)

    def get_kyc_status(self, update_date, wl_login, wl_pass, language,
            wallet_ip, wallet_ua):
        """
        :type update_date: String
        :type wl_login: String
        :type wl_pass: String
        :type language: String
        :type wallet_ip: String
        :type wallet_ua: String
        """
        return self.ws_request('GetKycStatus', 'Service_mb',
            updateDate=update_date, wlLogin=wl_login, wlPass=wl_pass,
            language=language, walletIp=wallet_ip, walletUa=wallet_ua,
            version=3)

    def get_money_in_iban_details(self, update_date, wl_login, wl_pass,
            language, wallet_ip, wallet_ua):
        """
        :type update_date: String
        :type wl_login: String
        :type wl_pass: String
        :type language: String
        :type wallet_ip: String
        :type wallet_ua: String
        """
        return self.ws_request('GetMoneyInIBANDetails', 'Service_mb',
            updateDate=update_date, wlLogin=wl_login, wlPass=wl_pass,
            language=language, walletIp=wallet_ip, walletUa=wallet_ua,
            version=3)

    def get_money_in_trans_details(self, transaction_id, transaction_comment,
            transaction_merchant_token, wl_login, wl_pass, language, wallet_ip,
            wallet_ua):
        """
        :type transaction_id: String
        :type transaction_comment: String
        :type transaction_merchant_token: String
        :type wl_login: String
        :type wl_pass: String
        :type language: String
        :type wallet_ip: String
        :type wallet_ua: String
        """
        return self.ws_request('GetMoneyInTransDetails', 'Service_mb',
            transactionId=transaction_id,
            transactionComment=transaction_comment,
            transactionMerchantToken=transaction_merchant_token,
            wlLogin=wl_login, wlPass=wl_pass, language=language,
            walletIp=wallet_ip, walletUa=wallet_ua, version=3)

    def get_money_out_trans_details(self, transaction_id, transaction_comment,
            wl_login, wl_pass, language, wallet_ip, wallet_ua):
        """
        :type transaction_id: String
        :type transaction_comment: String
        :type wl_login: String
        :type wl_pass: String
        :type language: String
        :type wallet_ip: String
        :type wallet_ua: String
        """
        return self.ws_request('GetMoneyOutTransDetails', 'Service_mb',
            transactionId=transaction_id,
            transactionComment=transaction_comment, wlLogin=wl_login,
            wlPass=wl_pass, language=language, walletIp=wallet_ip,
            walletUa=wallet_ua, version=3)

    def get_payment_details(self, transaction_id, transaction_comment,
            wl_login, wl_pass, language, wallet_ip, wallet_ua):
        """
        :type transaction_id: String
        :type transaction_comment: String
        :type wl_login: String
        :type wl_pass: String
        :type language: String
        :type wallet_ip: String
        :type wallet_ua: String
        """
        return self.ws_request('GetPaymentDetails', 'Service_mb',
            transactionId=transaction_id,
            transactionComment=transaction_comment, wlLogin=wl_login,
            wlPass=wl_pass, language=language, walletIp=wallet_ip,
            walletUa=wallet_ua, version=3)

    def get_wallet_details(self, wallet, wl_login, wl_pass, language,
            wallet_ip, wallet_ua):
        """
        :type wallet: String
        :type wl_login: String
        :type wl_pass: String
        :type language: String
        :type wallet_ip: String
        :type wallet_ua: String
        """
        return self.ws_request('GetWalletDetails', 'Service_mb', wallet=wallet,
            wlLogin=wl_login, wlPass=wl_pass, language=language,
            walletIp=wallet_ip, walletUa=wallet_ua, version=3)

    def money_in(self, wallet, amount_tot, amount_com, comment, card_type,
            card_number, card_crypto, card_date, auto_commission, wl_login,
            wl_pass, language, wallet_ip, wallet_ua):
        """
        :type wallet: String
        :type amount_tot: String
        :type amount_com: String
        :type comment: String
        :type card_type: String
        :type card_number: String
        :type card_crypto: String
        :type card_date: String
        :type auto_commission: String
        :type wl_login: String
        :type wl_pass: String
        :type language: String
        :type wallet_ip: String
        :type wallet_ua: String
        """
        return self.ws_request('MoneyIn', 'Service_mb', wallet=wallet,
            amountTot=amount_tot, amountCom=amount_com, comment=comment,
            cardType=card_type, cardNumber=card_number, cardCrypto=card_crypto,
            cardDate=card_date, autoCommission=auto_commission,
            wlLogin=wl_login, wlPass=wl_pass, language=language,
            walletIp=wallet_ip, walletUa=wallet_ua, version=3)

    def money_in3_d_authenticate(self, transaction_id, md, pa_res, card_type,
            card_number, card_code, card_date, wl_login, wl_pass, language,
            wallet_ip, wallet_ua):
        """
        :type transaction_id: String
        :type md: String
        :type pa_res: String
        :type card_type: String
        :type card_number: String
        :type card_code: String
        :type card_date: String
        :type wl_login: String
        :type wl_pass: String
        :type language: String
        :type wallet_ip: String
        :type wallet_ua: String
        """
        return self.ws_request('MoneyIn3DAuthenticate', 'Service_mb',
            transactionId=transaction_id, MD=md, PaRes=pa_res,
            cardType=card_type, cardNumber=card_number, cardCode=card_code,
            cardDate=card_date, wlLogin=wl_login, wlPass=wl_pass,
            language=language, walletIp=wallet_ip, walletUa=wallet_ua,
            version=3)

    def money_in3_d_confirm(self, transaction_id, md, pa_res, card_type,
            card_number, card_code, card_date, wl_login, wl_pass, language,
            wallet_ip, wallet_ua):
        """
        :type transaction_id: String
        :type md: String
        :type pa_res: String
        :type card_type: String
        :type card_number: String
        :type card_code: String
        :type card_date: String
        :type wl_login: String
        :type wl_pass: String
        :type language: String
        :type wallet_ip: String
        :type wallet_ua: String
        """
        return self.ws_request('MoneyIn3DConfirm', 'Service_mb',
            transactionId=transaction_id, MD=md, PaRes=pa_res,
            cardType=card_type, cardNumber=card_number, cardCode=card_code,
            cardDate=card_date, wlLogin=wl_login, wlPass=wl_pass,
            language=language, walletIp=wallet_ip, walletUa=wallet_ua,
            version=3)

    def money_in3_d_init(self, wk_token, wallet, amount_tot, amount_com,
            comment, card_type, card_number, card_code, card_date,
            auto_commission, return_url, wl_login, wl_pass, language,
            wallet_ip, wallet_ua):
        """
        :type wk_token: String
        :type wallet: String
        :type amount_tot: String
        :type amount_com: String
        :type comment: String
        :type card_type: String
        :type card_number: String
        :type card_code: String
        :type card_date: String
        :type auto_commission: String
        :type return_url: String
        :type wl_login: String
        :type wl_pass: String
        :type language: String
        :type wallet_ip: String
        :type wallet_ua: String
        """
        return self.ws_request('MoneyIn3DInit', 'Service_mb', wkToken=wk_token,
            wallet=wallet, amountTot=amount_tot, amountCom=amount_com,
            comment=comment, cardType=card_type, cardNumber=card_number,
            cardCode=card_code, cardDate=card_date,
            autoCommission=auto_commission, returnUrl=return_url,
            wlLogin=wl_login, wlPass=wl_pass, language=language,
            walletIp=wallet_ip, walletUa=wallet_ua, version=3)

    def money_in_validate(self, transaction_id, wl_login, wl_pass, language,
            wallet_ip, wallet_ua):
        """
        :type transaction_id: String
        :type wl_login: String
        :type wl_pass: String
        :type language: String
        :type wallet_ip: String
        :type wallet_ua: String
        """
        return self.ws_request('MoneyInValidate', 'Service_mb',
            transactionId=transaction_id, wlLogin=wl_login, wlPass=wl_pass,
            language=language, walletIp=wallet_ip, walletUa=wallet_ua,
            version=3)

    def money_in_web_init(self, wk_token, wallet, amount_tot, amount_com,
            comment, use_registered_card, return_url, cancel_url, error_url,
            auto_commission, wl_login, wl_pass, language, wallet_ip,
            wallet_ua):
        """
        :type wk_token: String
        :type wallet: String
        :type amount_tot: String
        :type amount_com: String
        :type comment: String
        :type use_registered_card: String
        :type return_url: String
        :type cancel_url: String
        :type error_url: String
        :type auto_commission: String
        :type wl_login: String
        :type wl_pass: String
        :type language: String
        :type wallet_ip: String
        :type wallet_ua: String
        """
        return self.ws_request('MoneyInWebInit', 'Service_mb',
            wkToken=wk_token, wallet=wallet, amountTot=amount_tot,
            amountCom=amount_com, comment=comment,
            useRegisteredCard=use_registered_card, returnUrl=return_url,
            cancelUrl=cancel_url, errorUrl=error_url,
            autoCommission=auto_commission, wlLogin=wl_login, wlPass=wl_pass,
            language=language, walletIp=wallet_ip, walletUa=wallet_ua,
            version=3)

    def money_in_with_card_id(self, wallet, amount_tot, amount_com, comment,
            card_id, auto_commission, wl_login, wl_pass, language, wallet_ip,
            wallet_ua):
        """
        :type wallet: String
        :type amount_tot: String
        :type amount_com: String
        :type comment: String
        :type card_id: String
        :type auto_commission: String
        :type wl_login: String
        :type wl_pass: String
        :type language: String
        :type wallet_ip: String
        :type wallet_ua: String
        """
        return self.ws_request('MoneyInWithCardId', 'Service_mb',
            wallet=wallet, amountTot=amount_tot, amountCom=amount_com,
            comment=comment, cardId=card_id, autoCommission=auto_commission,
            wlLogin=wl_login, wlPass=wl_pass, language=language,
            walletIp=wallet_ip, walletUa=wallet_ua, version=3)

    def money_out(self, wallet, iban_id, amount_tot, amount_com, message,
            auto_commission, wl_login, wl_pass, language, wallet_ip,
            wallet_ua):
        """
        :type wallet: String
        :type iban_id: String
        :type amount_tot: String
        :type amount_com: String
        :type message: String
        :type auto_commission: String
        :type wl_login: String
        :type wl_pass: String
        :type language: String
        :type wallet_ip: String
        :type wallet_ua: String
        """
        return self.ws_request('MoneyOut', 'Service_mb', wallet=wallet,
            ibanId=iban_id, amountTot=amount_tot, amountCom=amount_com,
            message=message, autoCommission=auto_commission, wlLogin=wl_login,
            wlPass=wl_pass, language=language, walletIp=wallet_ip,
            walletUa=wallet_ua, version=3)

    def refund_money_in(self, transaction_id, amount_to_refund, comment,
            wl_login, wl_pass, language, wallet_ip, wallet_ua):
        """
        :type transaction_id: String
        :type amount_to_refund: String
        :type comment: String
        :type wl_login: String
        :type wl_pass: String
        :type language: String
        :type wallet_ip: String
        :type wallet_ua: String
        """
        return self.ws_request('RefundMoneyIn', 'Service_mb',
            transactionId=transaction_id, amountToRefund=amount_to_refund,
            comment=comment, wlLogin=wl_login, wlPass=wl_pass,
            language=language, walletIp=wallet_ip, walletUa=wallet_ua,
            version=3)

    def register_card(self, wallet, card_type, card_number, card_code,
            card_date, wl_login, wl_pass, language, wallet_ip, wallet_ua):
        """
        :type wallet: String
        :type card_type: String
        :type card_number: String
        :type card_code: String
        :type card_date: String
        :type wl_login: String
        :type wl_pass: String
        :type language: String
        :type wallet_ip: String
        :type wallet_ua: String
        """
        return self.ws_request('RegisterCard', 'Service_mb', wallet=wallet,
            cardType=card_type, cardNumber=card_number, cardCode=card_code,
            cardDate=card_date, wlLogin=wl_login, wlPass=wl_pass,
            language=language, walletIp=wallet_ip, walletUa=wallet_ua,
            version=3)

    def register_iban(self, wallet, holder, bic, iban, dom1, dom2, wl_login,
            wl_pass, language, wallet_ip, wallet_ua):
        """
        :type wallet: String
        :type holder: String
        :type bic: String
        :type iban: String
        :type dom1: String
        :type dom2: String
        :type wl_login: String
        :type wl_pass: String
        :type language: String
        :type wallet_ip: String
        :type wallet_ua: String
        """
        return self.ws_request('RegisterIBAN', 'Service_mb', wallet=wallet,
            holder=holder, bic=bic, iban=iban, dom1=dom1, dom2=dom2,
            wlLogin=wl_login, wlPass=wl_pass, language=language,
            walletIp=wallet_ip, walletUa=wallet_ua, version=3)

    def register_wallet(self, wallet, client_mail, client_title,
            client_first_name, client_last_name, ctry, phone_number, wl_login,
            wl_pass, language, wallet_ip, wallet_ua):
        """
        :type wallet: String
        :type client_mail: String
        :type client_title: String
        :type client_first_name: String
        :type client_last_name: String
        :type ctry: String
        :type phone_number: String
        :type wl_login: String
        :type wl_pass: String
        :type language: String
        :type wallet_ip: String
        :type wallet_ua: String
        """
        return self.ws_request('RegisterWallet', 'Service_mb', wallet=wallet,
            clientMail=client_mail, clientTitle=client_title,
            clientFirstName=client_first_name, clientLastName=client_last_name,
            ctry=ctry, phoneNumber=phone_number, wlLogin=wl_login,
            wlPass=wl_pass, language=language, walletIp=wallet_ip,
            walletUa=wallet_ua, version=3)

    def send_payment(self, debit_wallet, credit_wallet, amount, message,
            wl_login, wl_pass, language, wallet_ip, wallet_ua):
        """
        :type debit_wallet: String
        :type credit_wallet: String
        :type amount: String
        :type message: String
        :type wl_login: String
        :type wl_pass: String
        :type language: String
        :type wallet_ip: String
        :type wallet_ua: String
        """
        return self.ws_request('SendPayment', 'Service_mb',
            debitWallet=debit_wallet, creditWallet=credit_wallet,
            amount=amount, message=message, wlLogin=wl_login, wlPass=wl_pass,
            language=language, walletIp=wallet_ip, walletUa=wallet_ua,
            version=3)

    def unregister_card(self, wallet, card_id, wl_login, wl_pass, language,
            wallet_ip, wallet_ua):
        """
        :type wallet: String
        :type card_id: String
        :type wl_login: String
        :type wl_pass: String
        :type language: String
        :type wallet_ip: String
        :type wallet_ua: String
        """
        return self.ws_request('UnregisterCard', 'Service_mb', wallet=wallet,
            cardId=card_id, wlLogin=wl_login, wlPass=wl_pass,
            language=language, walletIp=wallet_ip, walletUa=wallet_ua,
            version=3)

    def update_wallet_details(self, wallet, new_email, new_title,
            new_first_name, new_last_name, new_ctry, new_ip, new_phone_number,
            wl_login, wl_pass, language, wallet_ip, wallet_ua):
        """
        :type wallet: String
        :type new_email: String
        :type new_title: String
        :type new_first_name: String
        :type new_last_name: String
        :type new_ctry: String
        :type new_ip: String
        :type new_phone_number: String
        :type wl_login: String
        :type wl_pass: String
        :type language: String
        :type wallet_ip: String
        :type wallet_ua: String
        """
        return self.ws_request('UpdateWalletDetails', 'Service_mb',
            wallet=wallet, newEmail=new_email, newTitle=new_title,
            newFirstName=new_first_name, newLastName=new_last_name,
            newCtry=new_ctry, newIp=new_ip, newPhoneNumber=new_phone_number,
            wlLogin=wl_login, wlPass=wl_pass, language=language,
            walletIp=wallet_ip, walletUa=wallet_ua, version=3)

    def upload_file(self, wallet, file_name, type, buffer, wl_login, wl_pass,
            language, wallet_ip, wallet_ua):
        """
        :type wallet: String
        :type file_name: String
        :type type: String
        :type buffer: Base64Binary
        :type wl_login: String
        :type wl_pass: String
        :type language: String
        :type wallet_ip: String
        :type wallet_ua: String
        """
        buffer = self.soap_dict(buffer)
        return self.ws_request('UploadFile', 'Service_mb', wallet=wallet,
            fileName=file_name, type=type, buffer=buffer, wlLogin=wl_login,
            wlPass=wl_pass, language=language, walletIp=wallet_ip,
            walletUa=wallet_ua, version=3)
