#!/usr/bin/env python

# MM1.py

# Example of SimPy for discrete-time situations.

# M/M/1 queue.  Usage:

#   MM1.py Lambda Mu

# Exponentially distributed arrivals and service with rates Lambda and
# Mu

# The server is modeled as by the Server process, and the arrivals are
# modeled by the Arrivals process.  We do not use a Resource here, just
# modeling the queue with a list Queue.  Alternatively, we could define
# a Job process, with one created with each arrival. 

from __future__ import generators  # delete if use Python >= 2.3 
from SimPy.Simulation import *
from random import Random,expovariate,uniform

import sys

class Server(Process):
   def __init__(self):
      Process.__init__(self)  
   def Run(self):
      self.Queue = []  # queue starts out empty
      self.NDone = 0  # number of jobs completed
      self.TotWait = 0.0
      while 1:
         self.Busy = 0  # 1 for busy, 0 for idle
         # if no jobs, sleep until one arrives
         if len(self.Queue) == 0:
            yield passivate,self
         # serve job at head of queue
         # record time this job arrived, for later bookkeeping
         self.ArrvTime = self.Queue[0]  
         del self.Queue[0]
         self.Busy = 1
         yield hold,self,Globs.Rnd.expovariate(Globs.Mu)
         # job done, do bookkeeping 
         self.NDone += 1
         self.TotWait += now() - self.ArrvTime  

class Arrivals(Process):
   def __init__(self):
      Process.__init__(self) 
   def Run(self):
      while 1:
         yield hold,self,Globs.Rnd.expovariate(Globs.Lambda)
         # add job to queue, in form of its arrival time
         Globs.Srvr.Queue.append(now())
         # wake server if it's idle
         if Globs.Srvr.Busy == 0:
            reactivate(Globs.Srvr)

class Globs:
   Rnd = Random(12345)
   Lambda = float(sys.argv[1])
   Mu = float(sys.argv[2])
   MaxSimtime = float(sys.argv[3])
   Srvr = Server()
   Arrs = Arrivals()

# "main" program starts here

def main():
   initialize()  
   activate(Globs.Srvr,Globs.Srvr.Run(),delay=0.0)
   activate(Globs.Arrs,Globs.Arrs.Run(),delay=0.0)
   simulate(until=Globs.MaxSimtime)
   print ("observed mean residence time", Globs.Srvr.TotWait/Globs.Srvr.NDone)

if __name__ == '__main__':
   main()