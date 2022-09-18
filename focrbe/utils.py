import Levenshtein
import os
import unidecode

import re


def remove_accent(text):
    return unidecode.unidecode(text)


def getStringDifferent(string1, string2):
    string1 = string1.lower()
    string1 = remove_accent(string1)
    string2 = string2.lower()
    string2 = remove_accent(string2)
    maxLeng = max(len(string1), len(string2))
    return Levenshtein.distance(string1, string2) / maxLeng


def digital_sequence(s, sort_literal=False, fullwidth_digits=False):
    """Get sorted list of numbers.

    Args:
        s (str): arbitrary string
        sort_literal (bool): literal sort
        fullwidth_digits (bool): accept full-width digits

    Returns:
        list
    """
    r = r"\d+" if fullwidth_digits else r"[0-9]+"
    k = None if sort_literal else lambda x: int(x)
    return sorted(re.findall(r, s), key=k)


# def date_detection(s, sort_literal=False, fullwidth_digits=False):
#     """Get sorted list of numbers.

#     Args:
#         s (str): arbitrary string
#         sort_literal (bool): literal sort
#         fullwidth_digits (bool): accept full-width digits

#     Returns:
#         list
#     """
#     x = re.findall(
#         "^[0-9]{1,2}\\/[0-9]{1,2}\\/[0-9]{4}$", s)
#     return x
