__author__ = "Jeremy Nelson, Mike Stabile"

import unittest
import logging
import sys
import functools
import types

from klinkutils import colors


class MakeWrappedFunction():
    def __init__(self, name, log, func):
        self.name = name
        self.log = log
        self.cache = {None: self}
        self.func = func
        self.display = ".".join([colors.cyan.ig.i(".".join(log.name.split(".")[:-1])),
                                 colors.red.ig.i(name)])

    def __get__(self, obj, cls=None):
        if obj is None:
            return self
        try:
            return self.cache[obj]
        except KeyError:
            pass

        cex = self.cache[obj] = functools.partial(self.__call__, obj)
        return cex

    def __call__(self, *args, **kwargs):
        self.log.debug(self.display)
        return self.func(*args, **kwargs)

class TestLoggerMeta(type):
    """
    Metaclass for wrapping a test case to enable clean logging for test cases
    """
    def __new__(cls, name, bases, dct):

        module = sys.modules[dct['__module__']]
        # get the logger for the class
        log = logging.getLogger(".".join([dct['__module__'], dct['__qualname__']]))
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter('%(lineno)s - %(message)10s')
        handler.setFormatter(formatter)
        log.addHandler(handler)


        if 'log_level' in dct:
            log_level = dct['log_level']
            if isinstance(dct['log_level'], str):
                log_level = getattr(logging, dct['log_level'].upper())
            log.setLevel(log_level)
            # print(log_level)
        for val in dct.values():
            if type(val) == types.FunctionType:
                val.__globals__["log"] = log
        # if the TestCase already provides setUp, wrap it
        if 'setUp' in dct:
            setUp = dct['setUp']
        else:
            setUp = lambda self: None
        # pdb.set_trace()

        for key, val in dct.items():
            if type(val) == types.FunctionType and key not in ['setUp', 'tearDown']:
                test_log = logging.getLogger(".".join([log.name, key]))
                dct[key] = MakeWrappedFunction(key, test_log, val)
        def wrappedSetUp(self):
            msg = "%s\n%s\n%s\n" % ("".rjust(75, "*"), colors.header(setUp.__globals__['log'].name), "".rjust(80,"_"))
            setUp.__globals__['log'].debug(msg)
            setUp(self)
        dct['setUp'] = wrappedSetUp
        return type.__new__(cls, name, bases, dct)

class LoggedTestCase(unittest.TestCase, metaclass=TestLoggerMeta):
    pass
