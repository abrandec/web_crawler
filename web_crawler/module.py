""" Web Crawler Module v0.0.1 """
import os
import re
from urllib.parse import urlparse
import dataclasses
import requests

from bs4 import BeautifulSoup

# pylint: disable=trailing-whitespace
# pylint: disable=anomalous-backslash-in-string
# pylint: disable=too-many-instance-attributes
# pylint: disable=line-too-long
# pylint: disable=import-error
# pylint: disable=invalid-name
# pylint: disable=unused-variable
# pylint: disable=too-many-arguments

@dataclasses.dataclass
class web_crawler:
    """
    Web crawler class
    """
    def __init__(self, url_timeout, no_go_domains, max_depth, save_dest, debug_mode):
        """
        Initialize web crawler

        :param url_timeout: timeout for web requests in seconds
        :type url_timeout: int
        :param no_go_domains: list of domains to not crawl
        :type no_go_domains: list[str]
        :param max_depth: max page depth to crawl
        :type max_depth: int
        :param file_type_regex: regex to match file types
        :type file_type_regex: str
        :param save_dest: directory to save files to
        :type save_dest: str
        """
        self.url_timeout = url_timeout
        self.no_go_domains = no_go_domains
        self.max_depth = max_depth
        self.file_type_regex = ".(?:htm|pdf|org)"
        self.save_dest = save_dest
        self.debug_mode = debug_mode

        self.url_list = []
        self.tag_list = ['a', 'link']

        self.saved_urls = []
        self.saved_url_dest = []
    
    #                   #
    #   ERROR HANDLING  #
    #                   #   

    def __print_crawl_error(self, url, error, depth): 
        """ 
        for __web_request()
        
        :param url: url to print
        :type url: str
        :param error: error to print
        :type error: str
         """
        if self.debug_mode:
            match depth:
                case 0:
                    print(f"❌ {error} - {url}")
                case _:
                    print(f"{self.__wht_space(depth)}├ {depth}/{self.max_depth} ❌ {error} - {url}")

    def __no_go_domain(self, url, depth):
        """ 
        Avoid crawling certain domains
        
        :param url: url to check domain of
        :type url: str
        :param depth: depth of recursion
        :type depth: int

        :return: True if domain is forbidden, else False
        :rtype: bool
        """
        for no_go_domain in self.no_go_domains:
            if no_go_domain in urlparse(url).netloc:
                if self.debug_mode:
                    print(f"{self.__wht_space(depth)}├ {depth}/{self.max_depth} ❌ No go domain: {no_go_domain}")
                return True
        return False
    
    #                #      
    # MISC FUNCTIONS #
    #                #

    def __wht_space(self, depth):
        """ 
        generate white space for indentation
        
        :param depth: depth of recursion
        
        :return: whitespace for indentation
        :rtype: str
         """
        return " " * (depth + 1)
    
    def __url_status_stdout(self, url, depth): 
        """ 
        print return status of url to stdout
     
        :param url: url to print
        :type url: str
        :param depth: depth of recursion
        :type depth: int
        """
        if self.debug_mode:
            match depth:
                case 0:
                    underline = "─" * len(url)
                    print(f"{underline}\n{url}\n{underline}")
                case _:
                    # why doesn't the whitespace work anymore lol #
                    print(f"{self.__wht_space(depth)}├ {depth}/{self.max_depth}  {url}")
    
    def __file_saved_status(self, filename, depth, status_tf):
        """ 
        check if file has been saved and print status
     
        :param filename: file to check
        :type filename: str
        :param url: url to print
        :type url: str
        :param depth: depth of recursion
        :type depth: int
        :param status_tf: True if file has been saved, else False
        :type status_tf: bool
        """
        if self.debug_mode:
            match status_tf:
                case True:
                    print(f"{self.__wht_space(depth)}└ ✅ Saved file: {filename}")
                case _:
                    print(f"{self.__wht_space(depth)}└ ❌ File already exists: {filename}")
                
    #                         #      
    # MAIN INTERNAL FUNCTIONS #
    #                         #

    def __file_mode(self, resp):
        """ 
        return file mode for saving file
        html just needs resp.text, other file types need resp.content
        
        :param resp: response to get file mode from
        :type resp: requests.Response
        
        :return: file content, file mode
        :rtype: tuple(str, str)
        """
        if not re.match("\.(?:htm)", resp.url):
            return (resp.content, "wb")
        return (resp.text, "w")

    def __path_exists(self, path):
        """ 
        create directory if it doesn't exist
        
        :param path: path to check
        :type path: str
        """
        if not os.path.exists(path):
            os.makedirs(path)
    
    def __calc_root_dir(self, dest_path, deptherino):
        """ 
        calculate root directory of destination path 
        
        : param dest_path: destination path to calculate root directory of
        : type dest_path: str
        : param deptherino: depth of recursion
        : type deptherino: int
        
        : return: root directory of destination path
        : rtype: str
        """
        backtrace_amt = dest_path.count("/") - deptherino
        for i in range(backtrace_amt):
            dest_path = "../" + dest_path
        return dest_path

    def __url_to_local_path(self, url):
        """ 
        convert any url to local path
        
        :param url: url to convert to local path
        :type url: str
        
        :return: tuple of full_save_path and save_path
        :rtype: tuple(str, str)
        """
        full_save_path = self.save_dest + "/" + urlparse(url).netloc + urlparse(url).path
        if full_save_path[:-len(os.path.basename(full_save_path))] != '':
            return (full_save_path[:-len(os.path.basename(full_save_path))], full_save_path)
        if full_save_path.split("/")[-1] != '':
            filename = full_save_path.split("/")[-1]
        else:
            filename = full_save_path.split("/")[-2]
        save_path = os.path.join(full_save_path, filename + ".html")
        return (full_save_path, save_path)
    
    def __is_in_url_list(self, url):
        """ 
        check if url has been crawled and add to crawled list if not 
        
        :param url: url to check
        :type url: str
         """
        if url not in self.saved_urls:
            self.saved_urls.append(url)
            (_, local_url_dest) = self.__url_to_local_path(url)
            self.saved_url_dest.append(local_url_dest)

    def __save_file(self, resp, depth):   
        """ 
        save directory and file if they don't exist
        
        :param resp: response to save file from
        :type resp: requests.Response
        :param depth: depth of recursion
        :type depth: int
        """
        if depth < self.max_depth + 1:
            (save_path, filename) = self.__url_to_local_path(resp.url)
            (file, file_mode) = self.__file_mode(resp)
            self.__path_exists(save_path)
            self.__is_in_url_list(resp.url)
            if not os.path.exists(filename):
                with open(filename, file_mode) as file_open:
                    file_open.write(file)
            self.__file_saved_status(filename, depth, True)        
            return filename
        return None

    def __get_imgs(self, soup, resp, url, filename, depth):
        # pylint: disable=too-many-arguments
        """
        get images from html and save them

        :param soup: soup of html
        :type soup: BeautifulSoup
        :param resp: response to get images from
        :type resp: requests.Response
        :param url: url to get images from
        :type url: str
        :param filename: filename of html
        :type filename: str
        :param depth: depth of recursion
        :type depth: int
        """
        img_tags = soup.findAll('img')
        for img_tag in img_tags:
            if re.match("^(?!http|ftp)", img_tag['src']):
                img_tag['src'] = resp.url + img_tag['src']
            img_req = requests.get(img_tag['src'], timeout=self.url_timeout)
            try:
                if img_req.status_code == 200:
                    img_tag['src'] = self.__save_file(img_req, depth)
                    print(f"commonpath  {os.path.realpath(filename)}")
                    img_tag['src'] = self.__calc_root_dir(img_tag['src'], 1)
                    with open(filename, 'w', encoding='UTF-8') as file_open:
                        file_open.write(soup.prettify())
            except requests.exceptions.RequestException as error:
                self.__print_crawl_error(url, error, depth)

    def __web_crawl(self, url, depth):
        """ 
        web request a single url and recursively crawl it
        
        :param url: url to crawl
        :type url: str
        :param depth: depth of recursion
        :type depth: int
        """
        # Attempt a web request #
        if self.__no_go_domain(url, depth):
            return
        try:
            resp = requests.get(url, timeout=self.url_timeout)
            if resp.status_code == 200:
                self.__url_status_stdout(resp.url, depth)
                # save base url #
                file_nem = self.__save_file(resp, depth)
                soup = BeautifulSoup(requests.get(resp.url, timeout=self.url_timeout).text, 'html.parser')
                if depth < self.max_depth:
                    self.__get_imgs(soup, resp, url, file_nem, depth)
                    for link in soup.find_all(self.tag_list, href=re.compile(self.file_type_regex)):
                        # patch url if internal #
                        if re.match("^(?!http|ftp)", link['href']):
                            link['href'] = resp.url + link['href']
                        # no go domain check #
                        if not self.__no_go_domain(link['href'], depth):
                            temp_link = link['href']
                            (_, filename) = self.__url_to_local_path(link['href'])
                            # update url to local path #
                            link['href'] = self.__calc_root_dir(filename, 2)
                            with open(file_nem, "w", encoding='UTF-8') as file_open:
                                file_open.write(soup.prettify())
                            self.__web_crawl(temp_link, depth + 1)
        # Error handling #
            elif resp.status_code == 404:
                self.__print_crawl_error(url, "404", depth)
                # CHANGE INTERNAL 404 LINKS TO EXTERNAL ONES #
        except requests.exceptions.RequestException as error:
            self.__print_crawl_error(url, error, depth)

    #                    #
    # EXTERNAL FUNCTIONS #
    #                    #
    def crawl(self, url_list):
        """ 
        crawl webpages and save to local directory
        
        :param url_list: list of urls to crawl
        :type url_list: list[str]
        
        :return: tuple of saved urls and saved url destinations
        :rtype: tuple(list[str], list[str])  
        """
        self.url_list = url_list
        for url in url_list:
            self.__web_crawl(url, 0)
        return (self.saved_urls, self.saved_url_dest)
