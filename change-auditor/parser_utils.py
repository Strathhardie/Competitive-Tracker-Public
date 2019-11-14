import datetime

# This class contains all methods to handle string and datetime logic
class ParserUtils(object):

    # Parsers for string of format: <financial institution>-<account type>-<current date time>.html
    @staticmethod
    def parseBankName(file):
        return file.split('-')[0]

    @staticmethod
    def parseAccount(file):
        return file.split('-')[1]

    @staticmethod
    def parseDateTime(file):
        return file.split('-')[2].split('.')[0]

    # Parsers for a string datetime of format: %Y%m%d_%H%M%S
    @staticmethod
    def parseYear(dt):
        return int(dt[:4])

    @staticmethod
    def parseMonth(dt):
        return int(dt[4:6])

    @staticmethod
    def parseDay(dt):
        return int(dt[6:8])

    @staticmethod
    def parseHour(dt):
        return int(dt[9:11])

    @staticmethod
    def parseMin(dt):
        return int(dt[11:13])

    @staticmethod
    def parseSec(dt):
        return int(dt[13:15])

    # Given two date times in the form of strings, return true if the first datetime is strictly earlier than the second
    @staticmethod
    def dateTimeLessThan(first, second):
        first_dt = datetime.datetime(ParserUtils.parseYear(first), ParserUtils.parseMonth(first), ParserUtils.parseDay(first),
                                     ParserUtils.parseHour(first), ParserUtils.parseMin(first), ParserUtils.parseSec(first))
        second_dt = datetime.datetime(ParserUtils.parseYear(second), ParserUtils.parseMonth(second), ParserUtils.parseDay(second),
                                     ParserUtils.parseHour(second), ParserUtils.parseMin(second), ParserUtils.parseSec(second))
        return first_dt < second_dt
