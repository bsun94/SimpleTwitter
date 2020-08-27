"""
Created on Wed Aug 26 23:37:57 2020

Contains enum class for login error handling
"""
from enum import Enum

class States(Enum):
    verified = 'verified'
    user_err = 'username error'
    pw_err = 'password error'
