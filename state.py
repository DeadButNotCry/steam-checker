from datetime import date, time, datetime

from selenium import webdriver

class State:
    def __init__(self):
        self.DUPL = 0
        self.INV = 0
        self.FRIENDS = 0
        self.TIME = datetime.now()
        self.SPAMMED = 0
        self.NOT_SPAMMED = 0
    def to_zero(self):
        self.DUPL = 0
        self.INV = 0
        self.FRIENDS = 0
