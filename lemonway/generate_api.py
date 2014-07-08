# -*- coding: utf-8 -*-
import logging
from suds.client import Client
import types
import re
import os
from uuid import uuid1
from datetime import datetime
import textwrap

logging.getLogger('suds').setLevel(logging.INFO)
wsdl_url = 'file://' + os.path.dirname(os.path.realpath(__file__)) + '/lemonway.wsdl'

client = Client(wsdl_url)
logging.getLogger('suds').setLevel(logging.DEBUG)
WIDTH = 79
textwrapper = textwrap.TextWrapper(width=WIDTH, subsequent_indent='        ', replace_whitespace=False, break_long_words=False, break_on_hyphens=False)

default_values = {
    'register_wallet': {
        'version': '1.1',
        'ctry': None,
        'phone_number': None,
        'client_title': None,
        'wallet_ua': None
    },
    'get_wallet_details': {
        'version': '1.3',
        'wallet_ua': None
    },
    'update_wallet_details': {
        'version': '1.3',
        'new_email': None,
        'new_detail': None,
        'new_title': None,
        'new_first_name': None,
        'new_last_name': None,
        'new_ctry': None,
        'new_ip': None,
        'new_phone_number': None,
        'wallet_ua': None
    },
    'get_kyc_status': {
        'version': '1.3',
        'wallet_ua': None
    },
    'get_balances': {
        'version': '1.0',
        'wallet_ua': None
    },
    'get_money_in_trans_details': {
        'version': '1.3',
        'wallet_ua': None,
        'transaction_id': None,
        'transaction_comment': None,
        'transaction_merchant_token': None,
    },
    'money_in_web_init': {
        'version': '1.1',
        'wallet_ua': None,
        'amount_com': '0.00',
        'comment': None,
        'use_registered_card': 0,
        'auto_commission': 0
    },
    'refund_money_in': {
        'version': '1.2',
        'wallet_ua': None,
        'comment': None,
        'amount_to_refund': None
    },
    'get_balances': {
        'version': '1.0',
        'wallet_ua': None
    },
    'register_iban': {
        'version': '1.1',
        'wallet_ua': None
    },
    'money_out': {
        'version': '1.3',
        'wallet_ua': None,
        'amount_com': None,
        'message': None,
        'iban_id': None,
        'autoCommission': 0,  # 0 : ne pas déduire la commission automatiquement. 1 : déduire la commission automatiquement

    },
    'get_money_out_trans_details': {
        'version': '1.0',
        'wallet_ua': None,
        'transaction_id': None,
        'transaction_comment': None
    },

}


def convert_camel_case(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def upcase_first_letter(s):
    return s[0].upper() + s[1:]


def cmp_nillable(a, b):
    if a.nillable and not b.nillable:
        return 1
    elif a.nillable == b.nillable:
        return 0
    else:
        return -1


def wrap_text(text, indent=12):
    """Wrap text to WIDTH characters line length
    indent is 4, 8, 12 = number of spaces for indentation"""
    indent = text.index('(') + 1
    textwrapper.subsequent_indent = ' ' * indent
    return textwrapper.fill(text) + '\n'


def generate_classes():
    """Generate classes for a suds client
    :type client: suds.client.Client
    """
    print('Generating api.py...')
    content = """# -*- coding: utf-8 -*-
import logging
import os
from lemonway.exceptions import APIException
from lemonway.utils import pythonize, pretty_xml
from suds.client import Client
from time import strftime
from lxml import objectify


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


"""
    # Generate classes for complex types
    types = client.sd[0].types
    for t in types:
        # t is a tuple (Complex, Complex) with identical objects
        t = t[0]
        # Parameters to construct complex type + special cases
        children = []
        order_date = False
        for c in t.children():
            c = c[0]
            if c.name == 'date' and t.name.lower() == 'order':
                c.nillable = True
                order_date = True
            children.append(c)
        # Order parameters (nillable at the end)
        children = sorted(children, cmp=cmp_nillable)
        content += 'class %s(ComplexType):\n' % upcase_first_letter(t.name)
        init_met = '    def __init__(self, %s):\n' % ', '.join([convert_camel_case(c.name) + ('=None' if c.nillable else '') for c in children])
        content += wrap_text(init_met)
        # docstring = '        """\n'
        # for c in children:
        #     # c is a tuple (Element, Complex, Sequence)
        #     docstring += '        :type %s: %s\n' % (convert_camel_case(c.name), c.type[0] if c.type else 'UNKNOWN')
        # content += '%s        """\n' % docstring
        if order_date:
            content += "        if date is None:\n            date = strftime('%d/%m/%Y %H:%M')\n"
        content += '        super(%s, self).__init__(locals())\n' % (upcase_first_letter(t.name))
        translations = '        self._tr_params = {%s}' % ', '.join([("'%s': '%s'" % (convert_camel_case(c.name), c.name)) for c in children])
        content += wrap_text(translations)
        content += '\n\n'

    content += """class Lemonway(object):
    WSDL_URL = ('file://' + os.path.dirname(os.path.realpath(__file__))
                + '/lemonway.wsdl')

    def __init__(self, login, password, location):
        self.wl_login = login
        self.wl_pass = password
        self.language = 'en'
        self._location = location
        self._client = Client(self.WSDL_URL, cachingpolicy=1,
                              username=self.wl_login, password=self.wl_pass)
        self._client.options.cache.setduration(days=90)

    def ws_request(self, method, api_name, **params):
        self._client.set_options(location=self._location)
        info_msg = 'Calling %s method with params: %s' % (method, params)
        logger.info(info_msg)
        try:
            xml = getattr(self._client.service, method)(**params)
            answer = objectify.fromstring(xml)
            answer = pythonize(answer)
            answer.xml = pretty_xml(str(xml))
            logger.debug(xml)
        except Exception as e:
            msg = '%s %s - %s' % (e, e.message, info_msg)
            logger.error(msg)
            raise APIException(msg)
        # Detect errors and raise exception
        if 'error' in answer.__dict__:
            msg = '%s (code: %s) - %s' % (answer.msg, answer.code, info_msg)
            logger.error(msg)
            raise APIException(msg)
        return answer

    def soap_dict(self, complex_type):
        return complex_type.soap_dict if complex_type else None
"""

    # Generate methods (services from wsdl)
    for sd in client.sd:
        api_name = sd.service.name
        for port in sd.ports:
            # Pass ports[1] because it contains the same methods listed in ports[0]
            if port == sd.ports[1]:
                continue
            # port is a tupe (<type 'instance'>, <type 'list'>)
            # port[1] is a list of tuples (method_name, [arguments])
            # each argument is a tuple (<class 'suds.sax.text.Text'>, <class 'suds.xsd.sxbasic.Element'>)
            # first is text (name of paramter) and second is an element (.name .type[0] .nillable)
            for met, params in port[1]:
                # List of parameters: must be sorted (nillable at the end) and line length is
                params = sorted([p[1] for p in params], cmp=cmp_nillable)
                def_args = []
                ret_params = []
                complex_types = []
                met_default_values = default_values.get(convert_camel_case(met), {})
                api_level_params = ('wlLogin', 'wlPass', 'language')
                api_level_params_camel_case = [convert_camel_case(p) for p in api_level_params]
                for p in params:
                    if p.type and p.type[0] != 'string':
                        complex_types.append(p)
                    # sdef = 'param_with_underscore' with or not '=None'
                    sdef = convert_camel_case(p.name)
                    if sdef in met_default_values:
                        default_value = met_default_values.get(sdef)
                        if isinstance(default_value, str):
                            default_value = "'%s'" % default_value
                        sdef = '%s=%s' % (sdef, default_value)
                    elif p.nillable:
                        sdef += '=None'
                    if p.name not in api_level_params:
                        def_args.append(sdef)
                    # sret = 'paramCamelCase=param_with_underscore'
                    if p.name in api_level_params:
                        sret = '%s=self.%s' % (p.name, convert_camel_case(p.name))
                    else:
                        sret = p.name + '=' + (convert_camel_case(p.name))
                    ret_params.append(sret)
                # Re-order def_args to put params with default value at the end of list
                def_args = sorted(def_args, key=lambda k: '=' in k)
                # Print method definition
                method_definition = '    def %s(self, %s):\n' % (convert_camel_case(met), ', '.join(def_args))
                content += '\n' + wrap_text(method_definition)
                # Print docstring
                content += '        """\n'
                for p in params:
                    if p.name not in api_level_params:
                        content += '        :type %s: %s\n' % (convert_camel_case(p.name),
                                                               upcase_first_letter(p.type[0]) if p.type else 'UNKNOWN')
                content += '        """\n'
                # Print complex types conversion
                for p in complex_types:
                    content += '        %s = self.soap_dict(%s)\n' % (convert_camel_case(p.name), convert_camel_case(p.name))
                # Print return value
                method_ret = "        return self.ws_request('%s', '%s', %s)" % (met, api_name, ', '.join(ret_params))
                content += wrap_text(method_ret)

    filename = os.path.dirname(os.path.realpath(__file__)) + '/api.py'
    with open(filename, 'w+') as f:
        f.write(content)


if __name__ == "__main__":
    generate_classes()
