import os


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI", default="sqlite:///db.sqlite3")
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv("TRACK_MODIFICATIONS")
    SECRET_KEY = os.getenv("SECRET_KEY", default="SUP3R")


CHARACTERS = "123456789qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM"
MIN_LEN = 1
ORIGINAL_LINK_LEN = 128
PERMANENT_PART = "http://localhost/"
SHORT_LINK_LEN = 16
SPECIAL_CHARS = "$&!,|.><-; "
SHORT_AUTO_PART_LEN = 6
TIMEOUT_FOR_ORIGINAL = 5
