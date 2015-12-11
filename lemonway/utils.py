# -*- coding: utf-8 -*-
import re
from lxml.objectify import ObjectifiedElement
from .mapping import lemonway_errors
import lxml.etree as etree
from collections import OrderedDict

FILE_TYPE_ID_CARD_EU = 0
FILE_TYPE_RESIDENCE_PROOF = 1
FILE_TYPE_RIB = 2
FILE_TYPE_KBIS = 3
FILE_TYPE_OTHER_1 = 11
FILE_TYPE_OTHER_2 = 12
FILE_TYPE_OTHER_3 = 13

def generate_webkit_url(wk_url, money_in_token, css_url='', lang='fr'):
    return '%s?moneyInToken=%s&p=%s&lang=%s' % (
        wk_url, money_in_token, css_url, lang)


def format_details_errors(int_msg):
    """
    Get readable details informations by MoneyInTransDetails

    >>> details = format_details_errors('01-ERR_PSP_REFUSED')
    {'msg': u'ERR_PSP_REFUSED', 'msg_custom': 'Code li\xc3\xa9 au 3DS : Porteur non enrol\xc3\xa9 3-D Secure. ',
    'code': [u'01'], 'code_origin': u'01-ERR_PSP_REFUSED'}

    >>> details = format_details_errors('14-00-14-ERR_PSP_REFUSED')
    {'msg': u'ERR_PSP_REFUSED', 'msg_custom': 'Code g\xc3\xa9n\xc3\xa9ral : Coordonn\xc3\xa9es bancaires ou
    cryptogramme visuel invalides. Code PSP : Code not found in list. Code banque porteur : Num\xc3\xa9ro de porteur
    invalide. ', 'code': [u'14', u'00', u'14'], 'code_origin': u'14-00-14-ERR_PSP_REFUSED'}

    """
    details_infos = {'msg': None, 'code': None, 'code_origin': None, 'msg_custom': None}

    details_infos['code_origin'] = unicode(int_msg)
    split = unicode(int_msg).split('-')
    details_infos['code'] = split[:-1]
    details_infos['msg'] = split[-1]

    # Message parties begin from
    message_list = [
        ('xx', "Code général"),
        ('yy', "Code PSP"),
        ('zz', "Code banque porteur"),
        ('dd', "Code lié au 3DS")]

    # Begin writing custom message
    details_infos['msg_custom'] = ""
    for i, j in enumerate(details_infos['code']):
        if j == "":
            continue
        # manage case with only one error code. That case of MoneyIn3DInit.
        # In this case we can use 'dd' code dict.
        # see in LW - Kit Marque Blanche - Guide Intégration - 6.4.pdf p.94
        if len(details_infos['code']) == 1:
            i = 3
        try:
            details_infos['msg_custom'] += "%s : %s. " % (
                message_list[i][1], lemonway_errors[message_list[i][0]][j])
        except KeyError:
            details_infos['msg_custom'] += "%s : Code not found in list. " % (
                message_list[i][1])
    if len(details_infos['msg_custom']) > 250:
        details_infos['msg_custom'] = "%s..." % details_infos['msg_custom'][:247]
    return details_infos

def walk_dict(d):
    new_d = {}
    for k,v in d.items():
        if isinstance(v, OrderedDict):
            new_d[k.lower()] = walk_dict(v)
        else:
            new_d[k.lower()] = v
    return new_d
