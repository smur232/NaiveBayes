import requests
from bs4 import BeautifulSoup
import re

def determine_category_file(url):
    if 'entertainment' in url:
        return 'entertainment.txt'

def write_body_to_file(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    links = collect_links(soup)
    print(links)
    f = open(determine_category_file(url), 'w')

# print(soup.find_all("div", class_="story-body__inner"))
    for tag in soup.find_all('p', class_=lambda class_tag: class_tag == 'story-body__introduction' or class_tag == None, attrs={'style':None}):
        f.write(str(tag.contents[0]) + '\n')
    f.close()

def collect_links(soup):
    links = []
    # for link in soup.find_all('a'):
    for link in soup.find_all(href=not_lacie):
        url = link.get('href')
        if url != None and 'news' in url:
            links.append(url)
    return links

def not_lacie(href):
    return href and re.compile("(?<![a-z])/news/[\w-]+-[\d]+").search(href)
    #(?<![a-z]) this is saying to find all the /news/somestringofwords/stringofnumbers
    #that do not have any preceding alphabets, so those will be ones with .co.uk/news or .com/news

write_body_to_file('http://www.bbc.com/news/entertainment-arts-34380060')

#r = requests.get('http://bbc.co.uk')
# soup = BeautifulSoup(r.text, "html.parser")
#
# for link in soup.find_all('a'):
#     mylink = link.get('href')
#     if 'news' in mylink:
#         print(mylink)

# import requests
# from lxml import html
#
# response = requests.get('http://jakeaustwick.me')
#
# # Parse the body into a tree
# parsed_body = html.fromstring(response.text)
#
# # Perform xpaths on the tree
# print(parsed_body.xpath('//title/text()')) # Get page title
# print(parsed_body.xpath('//a/@href'))