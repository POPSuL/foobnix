#-*- coding: utf-8 -*-
'''
Created on 1 дек. 2010

@author: ivan
'''
import urllib

""""
Server: nginx/0.8.53
Date: Wed, 01 Dec 2010 07:37:42 GMT
Content-Type: text/html
Content-Length: 169
Connection: close
"""

def get_url_length(path):
    open = urllib.urlopen(path)
    return open.info().getheaders("Content-Length")[0]

def get_url_type(path):
    open = urllib.urlopen(path)
    return open.info().getheaders("Content-Type")[0]
