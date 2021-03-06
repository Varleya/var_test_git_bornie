'''
Created on May 6, 2011

@author: ppa
'''
import traceback

class Errors(object):
    """ class hosts error code constants """
    # general errors
    UNKNOWN_ERROR = 1

    NETWORK_ERROR = 100

    INDEX_RANGE_ERROR = 200


class ufException(Exception):
    """ Ultra-Finance exception """
    def __init__(self, error, errorMsg):
        """ constructor  """
        Exception.__init__(self)
        self.__error = error
        self.__errorMsg = errorMsg

    def __str__(self):
        """ string """
        return repr(self.__errorMsg)

    def getCode(self):
        """ accessor """
        return self.__error

    def getMsg(self):
        """ accessor """
        return "%s: %s" % (self.__errorMsg, traceback.format_exc(5))