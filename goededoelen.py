"""
The deliverable is an Excel file with the columns: name, street + street number,
postal code, city, telephone number, email address, website, facebook page, linkedin page, number of employees, budget

That information of more than 6000 nonprofits in Belgium.

For example:

https://www.goededoelen.be/search/?SearchTerm=social&OrgName=&Citydistance=5

https://www.bonnescauses.be/organisation/?id=0450059610&SearchTerm=social&Citydistance=5&searchlang=nl
"""

import time
import requests
from tools import (parsed_page, decode_email, check_link)
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from pprint import pprint

for i in range(1, 8):
    page_num = i
    html = f'https://www.goededoelen.be/search/?SearchTerm=social&OrgName=&Citydistance=5&Page={page_num}#search-results'


    def get_link():
        """Get link from page"""
        data = parsed_page(html)
        return data


    def get_data():
        """Get info from link"""
        links = get_link()
        company_info = []
        #  we`ll get 15 links from searching page, so we`ll use 15 workers to quickly get info that we need!
        #  it will be faster then step by step
        with ThreadPoolExecutor(15) as executor:

            # используем map сразу для всех 15 обектов(сначала получаем 15 ссылок, затем 15 распарсенных страниц и т.д.)
            r = list(executor.map(requests.get, links))  # get unparsed pages (we will get 15 response)
            soup = list(executor.map(lambda x: BeautifulSoup(x.content, 'html.parser'), r))  # get parsed pages
            names = list(executor.map(lambda x: x.find_all('span', class_='lbl_2_1 fl_left'), soup))
            addresses = list(executor.map(lambda x: x.find_all('p', class_='fl_left m_b_20 f_14 f_300 l_h_24'), soup))
            telephones = list(executor.map(lambda x: x.find_all('span', class_='l_h_24'), soup))
            emails = list(executor.map(lambda x: x.find_all('a', class_='ic_mail f_c2 f_600 f_14'), soup))
            sites = list(executor.map(lambda x: x.find_all('a', class_='ic_url f_c2 f_600 f_14'), soup))
            socials = list(executor.map(lambda x: x.find_all('a', class_='socialMediaLink'), soup))
            finances = list(executor.map(lambda x: x.find_all('p', class_='txt_center f_600'), soup))

            # for i in finance:
            #     pprint(i[1].get_text(strip=True) if i else 'Not available')

        # check objects on the availability of information and put in list index of objects with no data
        index_links = check_link(names)

        # move all info in zip to extract in with one 'for' and puts it in dictionary
        data = zip(names, addresses, telephones, emails, sites, socials, finances)

        for name, address, telephone, email, site, social, finance in data:
            company_info.append(
                {
                    'Name': name[0].get_text(strip=True) if name else 'No available information',
                    'Address':
                        address[0].get_text(strip=True).replace('Adresse', '')
                        if address else 'No available information',
                    'Telephone': telephone[0].get_text() if telephone else 'No available information',
                    'Email':
                        decode_email(email[0].get('href').replace('/cdn-cgi/l/email-protection#', ''))
                        if email else 'No available information',
                    'Site': site[0].get('href') if site else 'No available information',
                    'Facebook': social[0].get("href") if len(social) > 0 else 'No available information',
                    'Twitter': social[1].get("href") if len(social) > 1 else 'No available information',
                    'Linkedin': social[2].get("href") if len(social) > 2 else 'No available information',
                    'Finance': finance[1].get_text(strip=True) if finance else 'No available information'
                }
            )

        # delete elements from dict with no available information
        company_info[:] = [x for i, x in enumerate(company_info) if i not in index_links]
        pprint(company_info)
        print(f'This company have not got info:')
        company_no_data = [links[i][42:55] for i in index_links]
        pprint(company_no_data)


    tic = time.perf_counter()
    get_data()
    toc = time.perf_counter()
    print(f"Started {toc - tic:0.4f} seconds")
