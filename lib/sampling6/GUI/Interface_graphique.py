#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: wanying
"""

from tkinter import *
import os, time
import tkinter.filedialog as tkfd
import tkinter.messagebox as tkmb
from GUI import threads as th

class Interface(Frame):
	def __init__(self,window):
		Frame.__init__(self, window, width=200, height=100)
		window.title("docking-sampling")
		window.resizable(False,False)
		
		#case a crocher
		self.label0=Label(window,text="Please define the docking search space:")
		self.label0.grid(row=0,column=0,columnspan=3,sticky=W)
		self.var_case1 = BooleanVar()
		self.var_case2 = BooleanVar()
		self.case1 = Checkbutton(window, text="Entire receptor surface", variable=self.var_case1)
		self.case2 = Checkbutton(window, text="Interface", variable=self.var_case2)
		self.case1.grid(row=1,column=0,columnspan=3,sticky=W)
		self.case2.grid(row=2,column=0,columnspan=3,sticky=W)
		
		#option 'minimise' a choisir ou pas
		self.labelopt=Label(window,text="Option:")
		self.labelopt.grid(row=3,column=0,sticky=W)
		self.var_case3 = BooleanVar()
		self.case3 = Checkbutton(window, text="minimize", variable=self.var_case3)
		self.case3.select()
		self.case3.grid(row=4,column=0,sticky=W)
		
		#parcourir dossier
		self.label1=Label(window,text="Path to the sampling program directory:")
		self.label1.grid(row=5,column=0,columnspan=2,sticky=W)
		self.bouton_browse = Button(window, text="Browse", command=self.SelectDir)
		self.bouton_browse.grid(row=6,column=2,sticky=W)
		self.p_directory = StringVar()
		self.ligne_texte = Entry(window, textvariable=self.p_directory, width=50)
		self.ligne_texte.grid(row=6,column=0,columnspan=2,sticky=W)

		#parcourir fichier pdb du recepteur
		self.label2=Label(window,text="Path to receptor pdb::")
		self.label2.grid(row=7,column=0,columnspan=2,sticky=W)
		self.bouton_browse = Button(window, text="Browse", command=self.SelectRecFile)
		self.bouton_browse.grid(row=8,column=2,sticky=W)
		self.p_rec = StringVar()
		self.ligne_texte = Entry(window, textvariable=self.p_rec, width=50)
		self.ligne_texte.grid(row=8,column=0,columnspan=2,sticky=W)
		
		#parcourir fichier pdb du ligand
		self.label3=Label(window,text="Path to ligand pdb:")
		self.label3.grid(row=9,column=0,columnspan=2,sticky=W)
		self.bouton_browse = Button(window, text="Browse", command=self.SelectLigFile)
		self.bouton_browse.grid(row=10,column=2,sticky=W)
		self.p_lig = StringVar()
		self.ligne_texte = Entry(window, textvariable=self.p_lig, width=50)
		self.ligne_texte.grid(row=10,column=0,columnspan=2,sticky=W)
		
		#choisir le nombre de points de depart
		self.label4=Label(window,text="Number of starting positions for the ligand:")
		self.label4.grid(row=11,column=0,columnspan=2,sticky=W)      
		self.pt = StringVar()
		self.pt.set(600)
		self.ligne_texte = Entry(window, textvariable=self.pt, width=5)
		self.ligne_texte.grid(row=11,column=1)  
		
		#choisir le nombre de rotations du ligand
		self.label5=Label(window,text="Number of orientations at one starting position: ")
		self.label5.grid(row=12,column=0,columnspan=3,sticky=W)
		
		self.label5=Label(window,text="Around x axis: ")
		self.label5.grid(row=13,column=0,sticky=W)
		self.rotaX = StringVar()
		self.rotaX.set(7)
		self.ligne_texte = Entry(window, textvariable=self.rotaX, width=3)
		self.ligne_texte.grid(row=13,column=0)
		
		self.label5=Label(window,text="Around y axis: ")
		self.label5.grid(row=14,column=0,sticky=W)
		self.rotaY = StringVar()
		self.rotaY.set(7)
		self.ligne_texte = Entry(window, textvariable=self.rotaY, width=3)
		self.ligne_texte.grid(row=14,column=0)
		
		self.label5=Label(window,text="Around z axis: ")
		self.label5.grid(row=15,column=0,sticky=W)
		self.rotaZ = StringVar()
		self.rotaZ.set(7)
		self.ligne_texte = Entry(window, textvariable=self.rotaZ, width=3)
		self.ligne_texte.grid(row=15,column=0)
		
		#bouton run
		self.bouton_run = Button(window, text="Run", command=self.click)
		self.bouton_run.grid(row=16,column=1,sticky=W)
		
	def click(self): #ce qu'on fait si on clique sur 'run' 
		if not self.p_directory.get() or not self.p_rec.get() or not self.p_lig.get():
			tkmb.showerror('Error', 'Empty box!')
		elif not os.path.isdir(self.p_directory.get()) or not os.path.isfile(self.p_rec.get()) or not os.path.isfile(self.p_lig.get()):
			tkmb.showerror("Error", "No such file or directory!")
		else:
			if os.path.isdir(self.p_directory.get()) and os.path.isfile(self.p_rec.get()) and os.path.isfile(self.p_lig.get()):
				if (self.var_case1.get()==True and self.var_case2.get()==True):
					tkmb.showerror("Error", "Please define only ONE type of docking search space!")
				elif self.var_case1.get()==True:
					w = th.Worker() #background worker
					w.set_args(self.p_directory.get(),self.p_rec.get(),self.p_lig.get(),self.pt.get(),self.rotaX.get(),self.rotaY.get(),self.rotaZ.get(),self.var_case3.get(),self.var_case2.get())
					w.start()
					tkmb.showinfo("Started", "Started")
					while not w.finished:
						time.sleep(0.5)
					tkmb.showinfo("Finished", "Finished")
				elif self.var_case2.get()==True:
					w = th.Worker() #background worker
					w.set_args(self.p_directory.get(),self.p_rec.get(),self.p_lig.get(),self.pt.get(),self.rotaX.get(),self.rotaY.get(),self.rotaZ.get(),self.var_case3.get(),self.var_case2.get())
					w.start()
					tkmb.showinfo("Started", "Started")
					while not w.finished:
						time.sleep(0.5)
					tkmb.showinfo("Finished", "Finished")
				
					
	def SelectRecFile(self):
		filename = tkfd.askopenfilename(title="Choose receptor file",filetypes=[("all files","*.pdb")])
		self.p_rec.set(filename)
		
	def SelectLigFile(self):
		filename = tkfd.askopenfilename(title="Choose ligand file",filetypes=[("all files","*.pdb")])
		self.p_lig.set(filename)
		
	def SelectDir(self):
		dirname = tkfd.askdirectory()
		self.p_directory.set(dirname)

