# -*- coding: utf-8 -*-
import re
from lxml.objectify import ObjectifiedElement
from lemonway.mapping import lemonway_errors
import lxml.etree as etree

FILE_TYPE_ID_CARD_EU = 0
FILE_TYPE_RESIDENCE_PROOF = 1
FILE_TYPE_RIB = 2
FILE_TYPE_KBIS = 3
FILE_TYPE_OTHER_1 = 11
FILE_TYPE_OTHER_2 = 12
FILE_TYPE_OTHER_3 = 13


def convert_camel_case(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def pythonize(obj, is_list=False):
    for k, v in obj.__dict__.items():
        # obj.AttrTest = 3
        # => obj.attr_test = 3
        if k == 'xml':
            continue
        if isinstance(getattr(obj, k), ObjectifiedElement):
            if len(v) <= 1:
                v = pythonize(v)
            else:
                is_list = True
                l = []
                for e in v:
                    l.append(pythonize(e))
                    delattr(obj, k)
                v = l
        # If not a list of elements, set new attribute and delete old one
        setattr(obj, convert_camel_case(k), v)
        if not is_list:
            delattr(obj, k)
    return obj


def pretty_xml(xml):
    s = etree.fromstring(xml)
    return etree.tostring(s, pretty_print=True)


def generate_webkit_url(wk_url, money_in_token, css_url='', lang='fr'):
    return '%s?moneyInToken=%s&p=%s&lang=%s' % (
        wk_url, money_in_token, css_url, lang)


def format_details_errors(int_msg):
    """
    Get readable details informations by MoneyInTransDetails
    :type wallet_ip: str
    :type proposed_token: str
    """
    details_infos = {'msg': None, 'code': None, 'code_origin': None, 'msg_custom': None}

    details_infos['code_origin'] = unicode(int_msg)
    split = unicode(int_msg).split('-')
    details_infos['code'] = split[:-1]
    details_infos['msg'] = split[-1]

    # Message parties begin from
    message_list = [
        ('xx', "Code général"),
        ('yy', "Contrôle effectué par notre partenaire"),
        ('zz', "Code retourné par la banque du porteur"),
        ('dd', "Code lié au 3DS")]

    # Begin writing custom message
    details_infos['msg_custom'] = ""
    for i, j in enumerate(details_infos['code']):
        try:
            details_infos['msg_custom'] += "%s : %s. " % (
                message_list[i][1], lemonway_errors[message_list[i][0]][j])
        except:
            details_infos['msg_custom'] += "%s : Code not found in list. " % (
                message_list[i][1])
    return details_infos
