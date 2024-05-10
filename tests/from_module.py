from ward import ward
from time import sleep

@ward.watchit
def func_other_1():
    return sleep(0.21)
