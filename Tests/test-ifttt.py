#!/usr/bin/python3
#coding=utf-8

## Magic Mirror MMM-IFTTT Module layout.
#
#    url: 'http://10.0.0.20:8080/IFTTT'
#    method: POST
#    headers:
#      accept: 'application/json'
#    payload: '{"message": "{{ message }}","displaySeconds": "{{ displaySeconds }}","size": "{{ size }}"}'
#    content_type:  'application/json; charset=utf-8'
##

import json
import requests

response = requests.post('http://10.0.0.20:8080/IFTTT', json={'message': 'Hello world!', 'displaySeconds': '5', 'size': 'large'})

print(response.json())
