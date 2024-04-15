# Jeremy Zay

import http_util


class Cache():
    def __init__(self, url, cached_response) -> None:
        self.url = url #str
        self.cached_response = cached_response # http response in bytes
        self.last_modified = '-1' # str
        self.date = '-1' # str
        self.set_fields(self.get_header(self.cached_response))
    
    
    def get_response(self, response):
        '''
        get_response(response:bytes):bytes = response
        If response has not been modified since last caching, returns cached response,
        otherwise, updates cached response to new response and returns new response
        '''
        # bin_str -> bin_str
        #receives encoded response
        header = self.get_header(response)
        if self.is_not_modified(header):
            # print("not modified")
            return self.cached_response
        else: 
            self.cached_response = response
            # print("modified")
            return response
    
    
    def set_last_modified(self, header):
        '''
        set_last_modified(header:str):None
        sets cache last_modified field
        '''
        # header = self.get_header(self.cached_response)
        field_title = 'Last-Modified: '
        last_modified_line = self.find_in_header(header, field_title)
        if last_modified_line.startswith(field_title):
            
            self.last_modified = last_modified_line[len(field_title) : len(last_modified_line)-1] 

            # print(f"last_modified = {self.last_modified}")
        else: 
            # print("No last modified field")
            self.last_modified = '-1'


    def set_date(self, header):
        '''
        set_date(header:str):None
        sets cache date field
        '''
        date_line = self.find_in_header(header, 'Date')
        self.date = date_line
            
        field_title = 'Date: '
        date_line = self.find_in_header(header, field_title)
        if date_line.startswith(field_title):
            
            self.last_modified = date_line[len(field_title) : len(date_line)-1] 

            # print(f"date = {self.date}")
        else: 
            # print("No date field")
            self.date = '-1'
                        
        # print(f"date = {self.date}")


    def set_fields(self, header):
        '''
        set_fields(header:str):None
        sets cache date and last_modified fields (called upon init)
        '''
        self.set_last_modified(header)
        self.set_date(header)
        

    def is_not_modified(self, header): 
        '''
        is_not_modified(header:str):bool = True,
            if url has not been modified since last time got Response from it
        = False, otherwise
        '''
        not_modified = self.find_in_header(header, '304 Not Modified')
        if not_modified != '':
            # print('not modified')
            return True
        
        self.set_fields(header)

        return False
        
    
    def find_in_header(self, header, field):
        '''
        find_in_header(header:str, field:str):str = line
        returns the line in the header in which the field is, 
        if none found, returns '-1'
        '''
        header_list = header.split('\n')
        for i in range(len(header_list)):

            line = header_list[i]
            if field in line:
                # print(f'found field: {field}')
                return line
        
        return '-1'
    
    
    def get_header(self, response):
        '''
        get_header(response:bytes):str = header
        gets header (str) from response (bytes)
        '''
        response_list = response.split(b'\r\n\r\n')
        header = response_list[0].decode('utf-8')
        # print(f'header = \n{header}\n')
        return header
        

        
        
class CacheList(list):
    def __init__(self, cache_list):
        self.cache_list = cache_list             
    
    def is_url_in_cache(self, url):
        '''
        get_cache_by_url(url:str):bool = True, 
            if url in cache,
            False, otherwise
        '''
        for cache in self.cache_list:
            if url == cache.url:
                return True
        return False
    

    def get_cache_by_url(self, url):
        '''
        get_cache_by_url(url:str):Cache = cache
        Extracts cache object corresponding to url,
            if none exists, return None
        '''
        for cache in self.cache_list:
            if url == cache.url:
                return cache
        # print("url not in cache")
        return None
    
    
    def get_last_modified(self, url):
        '''
        get_last_modified(url:str):str = last_modified
        Extracts stored last_modified field from cached url
        '''
        last_modified = self.get_cache_by_url(url).last_modified
        if last_modified == '-1':
            print("no last modified field set")
        return last_modified
    
    
    def get_date(self, url):
        '''
        get_date(url:str):str = date
        Extracts stored date field from cached url
        '''
        date = self.get_cache_by_url(url).date
        if date == '-1':
            print("no date field set")
        return date
    
    
    def create_last_modified_req(self, http_req, url):
        '''
        create_last_modified_req(http_req:str, url:str):str = http_req
        
        Adds 'If-Modified-Since' field to GET req. 
        Sets the timestamp to the previous last_modified field, if found, 
            otherwise sets to previous date field, if foud,
            otherwise returns original request
        '''
        if self.get_last_modified(url) != '-1':
            return http_util.add_http_field(http_req, 'If-Modified-Since', self.get_last_modified(url), 2)
        elif self.get_date(url) != '-1': 
            return http_util.add_http_field(http_req, 'If-Modified-Since', self.get_date(url), 2)
        # print("orig http_req")
        return http_req

        
    def get_response_and_update_cache(self, url, response):
        '''
        get_response_and_update_cache(url:str, response:str):str = response
        
        If url in cache, returns cached response if unmodified, else returns new response
        If url not in cache, returns new response
        '''
        # print(f"url passed into get_response_and_update_cache: \n{url}\n")
        cache = self.get_cache_by_url(url)
        
        if cache:
            print("\nURL already in cache...")
            return cache.get_response(response)
        else:
            #update cache
            print("\nURL not yet in cache...")
            self.cache_list.append(Cache(url, response))
            return response
            
    def update_cache(self, url, response):
        # --not in use--
        #update cache
        # print("not yet in cache")
        self.cache_list.append(Cache(url, response))

        
    def print_urls_in_cache(self):
        '''
        prints len of cache and all URLs currently stored in cache
        '''
        print(f"\nprinting urls in cache (len = {len(self.cache_list)})")
        for cache in self.cache_list:
            print(f"url: {cache.url}")
        print("\n")