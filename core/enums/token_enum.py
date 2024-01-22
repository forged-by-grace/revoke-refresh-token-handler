from enum import Enum

class Role(str, Enum):
    anonymouse='anonymouse'
    authenticated='authenticated'
    admin='admin'
