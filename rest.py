# -*- coding: utf-8 -*-

import sys
import os
import json
import web
import xml.etree.ElementTree as ET
sys.path.append('/xiaolan/skills/')
import music
import news
import smarthome
import joke
import tuling
import weather

urls=(
    '/xiaolan/skills/text=(.*)','skills',
    '/xiaolan/states/start/(.*)','log',
    '/xiaolan/state/shutdown/(.*)','log',
    '/xiaolan/data/smarthome/e_id=(.*)&text=(.*)','smarthome',
)
app = web.application(urls,globals())

class skills:
    
    def GET(self, text):
        
