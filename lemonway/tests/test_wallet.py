import unittest
import random
from .fixtures import api, customer_ip, email_generator

class WalletTestCase(unittest.TestCase):
    """
        Wallet TestCase
    """

    def TestGetWalletDetails(self):
        """
        Test we can get information about a wallet
        """
        wallet = api.get_wallet_details('0001', wallet_ip=customer_ip)
        self.assertIn("wallet", wallet)

    def TestCreateWallet(self):
        """
        Test we can create a new wallet
        """
        wallet_id = str(random.randint(0000,9999))
        new_wallet = api.register_wallet(wallet=wallet_id,
                            client_first_name='martin',
                            client_last_name='mekkaoui',
                            ctry='GER',
                            phone_number='+4911122233344',
                            client_mail=email_generator(),
                            client_title='M',
                            wallet_ip=customer_ip,
                            city="Berlin",
                            street="Elsenstr. 106",
                            post_code="12345")
        self.assertIn("wallet", new_wallet)
        self.assertEquals(wallet_id, new_wallet.get("wallet")['id'])