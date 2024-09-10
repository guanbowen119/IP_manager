class MobileConverter(object):
    regex = '1[345789]\\d{9}'

    @staticmethod
    def to_python(value):
        return value

class UuidConverter(object):
    regex = '[\\w-]+'

    @staticmethod
    def to_python(value):
        return str(value)
