#!/usr/bin/python3
#
# Wesleyan University
# COMP 332
# Web server helper functions

# Jeremy Zay

# Project modules
import http_constants as const

def parse_url(url):

    url_components = url.split('http://')
    if len(url_components) > 1:
        url = '/'.join(url_components[1:])

    url_components = url.split('/')
    hostname = url_components[0]
    if len(url_components) == 1:
        pathname = '/'
    else:
        pathname = '/' + '/'.join(url_components[1:])

    return [hostname, pathname]

def create_http_req(hostname, pathname):

    # Create header lines
    get = 'GET ' + pathname + ' HTTP/1.0' + const.END_LINE
    host = 'Host: ' + hostname + const.END_LINE
    # modified_since =' If-Modified-Since: ' + const.END_LINE #Sun, 18 Jan 2018 20:43:27 GMT\r\n\r\n"
    conn_type = 'Connection: close' + const.END_LINE
    char_set = 'Accept-charset: utf-8' + const.END_LINE

    # Create HTTP request
    http_req = (get + host + char_set + conn_type + const.END_LINE)

    return http_req

def add_http_field(msg, name, value, priority):

    try:
        header_end = msg.index(const.END_HEADER) + len(const.END_LINE)
        # print(f'header_end = {header_end}')
        old_header = msg[ :  header_end]
        # print(f'old_header = {old_header}')
        # print(old_header.encode('utf-8'))
        old_header_list = old_header.split(const.END_LINE)
        
        field = name + ': ' + value #+ const.END_LINE
        
        old_header_list.insert(priority, field)
        new_msg = const.END_LINE.join(old_header_list) # [ : priority + 1]
        # print("new header = \n")
        # print(new_msg.encode('utf-8'))
        # new_msg = old_header + field + const.END_LINE
        # print(f'mew_msg = {new_msg}')

        
        return new_msg + const.END_HEADER

    except ValueError as e:
        print("Unable to add HTTP field:", e)
        return '-1'

def get_http_field(msg, name, end_str):

    try:
        name_start = msg.index(name)
        # print('line 1')
        name_end = name_start + len(name)
        # print('line 2')
        field_end = name_end + msg[name_end : ].index(end_str)
        # print('line 3')
        value = msg[name_end : field_end]
        # print('line 4')
        return value

    except ValueError as e:
        print("HTTP field not found: \n", f"msg = {msg},\n name = {name},\n end_str = {end_str},\n e = {e}\n")
        return -1

