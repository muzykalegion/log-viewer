import time
from datetime import datetime
from multiprocessing import Pipe
from threading import Thread

import numpy as np


class Checker:
    def __init__(self):
        self.TAKEOFF_LIST = None

    def doStuff(self):
        self.TAKEOFF_LIST = np.zeros(10)  # Creating the take off curve
        for t in range(len(self.TAKEOFF_LIST)):
            self.TAKEOFF_LIST[t] = (1 - (1 / np.exp(t)))  # act like a cap-charge shape
        self.TAKEOFF_LIST = self.TAKEOFF_LIST.tolist()
        print(self.TAKEOFF_LIST)
        self.TAKEOFF_LIST.pop(0)
        print(self.TAKEOFF_LIST)

    def scaleRange(self, x, srcMin, srcMax, destMin, destMax):
        a = (destMax - destMin) * (x - srcMin)
        b = srcMax - srcMin
        print((a / b) + destMin)



class Thread1(Thread):
    def __init__(self, pipe):
        Thread.__init__(self)
        self.pipe_write, self.pipe_read = pipe

    def run(self):
        for i in range(2):
            self.pipe_write.send([i, i*i])
            self.pipe_write.send([3])
            print('1 sent')
            time.sleep(0.02)


class Thread2(Thread):
    def __init__(self, pipe):
        Thread.__init__(self)
        self.pipe_write, self.pipe_read = pipe

    def run(self):
        while True:
            # if self.pipe_read.poll():
            iar = self.pipe_read.recv()
            print(f'2 got {iar}')
            time.sleep(0.02)


if __name__ == '__main__':
    # pipe = Pipe()
    # thread1 = Thread1(pipe)
    # thread1.start()
    # thread2 = Thread2(pipe)
    # thread2.start()
    checker = Checker()
    checker.scaleRange(-510,0,490,0,500)


