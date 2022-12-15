class BotException(Exception):
    """Base class for Telegram bot exceptions"""


class UnsupportedFileTypeException(BotException):
    pass
