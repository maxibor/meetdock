#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: wanying
"""
import threading, os
from tkinter import *
from tkinter.messagebox import *

class Worker():
	finished = False
	path = None
	r = None
	l = None
	nbPt = None
	XRota = None
	YRota = None
	ZRota = None
	minimize = True
	jet = False
			
	def set_args(self,p,r,l,nbPt,XRota,YRota,ZRota,minimize,jet):
		self.path=p
		self.r=r
		self.l=l
		self.nbPt=nbPt
		self.XRota=XRota
		self.YRota=YRota
		self.ZRota=ZRota
		self.jet=jet
		if minimize==False:
			self.minimize=False
		
	def do_work(self):
		try:
			os.makedirs("Results")
		except:
			pass
		os.system("python3 %s/Tools/confsGenerator.py -r %s -l %s -p %s -nbPt %s -XRota %s -YRota %s -ZRota %s -minimize %s -jet %s"%(self.path,self.r,self.l,self.path,self.nbPt,self.XRota,self.YRota,self.ZRota,self.minimize,self.jet))
		self.finished=True
		
	def start(self):
		self.th = threading.Thread(target=self.do_work)
		self.th.start()
	   
			
