#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: wanying
"""

from tkinter import *
from GUI import Interface_graphique as Ig

#demarre la boucle tk
window=Tk()
interface=Ig.Interface(window)
window.mainloop()
