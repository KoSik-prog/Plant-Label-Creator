#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:        Plant Label Creator.py
# Purpose:
#
# Author:      KoSik
#
# Created:     09.05.2025
# Copyright:   (c) kosik 2025
# -------------------------------------------------------------------------------
import label_cad
import eel
import os
import sys


@eel.expose 
def generate_label_small(labelText):
    print("generate label small")
    return label_cad.create_label_small(labelText)

@eel.expose 
def generate_label_big(labelText):
    print("generate label big")
    return label_cad.create_label_big(labelText)

def close_callback(window, args):
    eel.sleep(0.1)
    sys.exit(0)

class Gui:
    def __init__(self):
        print("GUI init")
        self.eel = eel
        self.eel.init(f'{os.path.dirname(os.path.realpath(__file__))}/web', allowed_extensions=['.js', '.html'])
        self.name = 'eel label'
        self.create_window()
        
    def create_window(self):
        eel.start(
            'index.html',
            mode='chrome',
            cmdline_args=[
                '--new-window',
                '--app=http://localhost:8000',
                '--window-size=430,400',
                '--disable-infobars',
                '--no-first-run'
            ],
            block=True,
            close_callback=close_callback
        )
        while True:
            eel.sleep(.1) 

if __name__ == "__main__":
    print("Planet Label Creator")
    gui = Gui()
    sys.exit(0)