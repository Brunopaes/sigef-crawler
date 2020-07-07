#!-*- coding: utf8 -*-
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from bs4 import BeautifulSoup
from tqdm import tqdm

import datetime
import requests
import pandas
import os


class SigefRequests:
    """Class responsible for accessing, extracting and parsing sigef
    information into a csv file.

    The output file will be at ./data/outputs

    """
    def __init__(self, path):
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        self.url_list = self.reading_url_file(path)
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:54.0) "
                          "Gecko/20100101 Firefox/54.0",
            "Connection": "close",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,/"
                      ";q=0.8",
            "Upgrade-Insecure-Requests": "1"
        }
        self.session = requests.session()
        self.data = {
            'código': [],
            'denominação': [],
            'área': [],
            'data de entrada': [],
            'situação - parcela': [],
            'responsável técnico': [],
            'ART': [],
            'envio': [],
            'requerimento': [],
            'status': [],
            'data': [],
            'situação - georeferência': [],
            'natureza': [],
            'número de parcelas': [],
            'municípios': [],
            'nome': [],
            'cpf/cnpj': [],
        }

    # Used in __init__
    @staticmethod
    def reading_url_file(path):
        """This function reads the links.txt file and return a links list.

        Parameters
        ----------
        path : str
            The path to links.txt file.
            (By default this file is in data folder).

        Returns
        -------
        url_list : iterator
            The links list.

        """
        return open(
            os.path.abspath('../' + path)
        ).readlines()

    # Used in __call__
    def requesting(self, url):
        """This function makes a GET requisition into the given sigef url.

        Parameters
        ----------
        url : str
            Sigef's URL.

        Returns
        -------
        response : requests.models.Response
            The GET Requisition response.

        """
        return self.session.get(url, verify=False, headers=self.headers)

    # Used in __call__
    @staticmethod
    def soup(html):
        """This function parses the html.

        Parameters
        ----------
        html : requests.models.Response
            Unparsed html.

        Returns
        -------
        parsed_html : bs4.BeautifulSoup
            Parsed html.

        """
        return BeautifulSoup(html.content, 'html5lib')

    # Used in __call__
    def filtering_content(self, html):
        """This function filters the page content and looks for the relevant
        data.

        Parameters
        ----------
        html : bs4.BeautifulSoup
            Parsed html.

        Returns
        -------

        """
        tables = html.find_all('table', {
            'class': 'table table-hover tabela-atributos'
        })

        content_list = []
        for table in tables:
            for row in table.find_all('td'):
                content_list.append((row.text.strip()))

        content_list.pop(7)
        content_list.pop(11)
        content_list.pop(14)

        for key, value in zip(self.data.keys(), content_list):
            self.data.get(key).append(value)

        self.parsing_to_csv()

    # Used in filtering_content
    def parsing_to_csv(self):
        """This function parses the acquired data into a csv file.

        Returns
        -------

        """
        pandas.DataFrame(self.data).set_index('código').to_csv(os.path.abspath(
            '../data/outputs/sigef-{}.csv'.format(datetime.date.today())),
            encoding='latin-1'
        )

    def __call__(self, *args, **kwargs):
        for url in tqdm(self.url_list):
            self.filtering_content(self.soup(self.requesting(url)))


if __name__ == '__main__':
    SigefRequests(r'data\links.txt').__call__()
