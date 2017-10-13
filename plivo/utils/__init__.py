# -*- coding: utf-8 -*-
import inspect
import re
from datetime import datetime


def is_valid_time_comparison(time):
    if isinstance(time, datetime):
        return True
    return False


def is_valid_subaccount(subaccount):
    subaccount_string = str(subaccount)
    if len(subaccount_string) == 20 and subaccount_string[:2] == 'SA':
        return True
    return False


def is_valid_mainaccount(mainaccount):
    mainaccount_string = str(mainaccount)
    if len(mainaccount_string) == 20 and mainaccount_string[:2] == 'MA':
        return True
    return False


def to_param_dict(func, vals, exclude_none=True):
    args, varargs, kwargs, _ = inspect.getargspec(func)
    arg_names = list(args)
    # The bit of regex magic below is for arguments that are keywords in
    # Python, like from. These can't be used directly, so our convention is to
    # add "_" suffixes to them. This strips them out.
    pd = {
        re.sub(r'^(.*)_+$', r'\1', key): value
        for key, value in vals.items()
        if key != 'self' and key in arg_names and
        (value is not None or exclude_none is False)
    }
    return pd
