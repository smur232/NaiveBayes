import requests
from bs4 import BeautifulSoup
import re
from collections import deque

def begin_crawling_from_this_page(url, max_num_of_articles=20):
    links = deque()
    links.append(url)
    count = 0
    while links and count < max_num_of_articles:
        write_body_to_file(links.popleft(), links, max_num_of_articles)
        count += 1

def write_body_to_file(url,links, max_num_of_articles):
    file_to_write_to = determine_category_file(url)

    if file_to_write_to == 'ignore':
        return

    print('Current going through ', url, ':')
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    links.extend(collect_links(soup))
    f = open(file_to_write_to, 'a')
    try:
        for tag in soup.find_all('p', class_=lambda class_tag: class_tag == 'story-body__introduction' or class_tag == None, attrs={'style':None}):
            # print(tag)
            contents = str(tag.contents[0])
            if 'href' not in contents and 'span' not in contents:
                f.write(contents + '\n')
    except:
        print('had some problem parsing through this page', url)
    else:
        print('     successfully written to file', file_to_write_to)
    finally:
        f.close()

def collect_links(soup):
    links = ['http://www.bbc.com' + link.get('href') for link in soup.find_all(href=path_to_articles)]
    return links

def path_to_articles(href):
    return href and re.compile("(?<![a-z])/news/[\w-]+-[\d]+").search(href)
    #(?<![a-z]) this is saying to find all the /news/somestringofwords/stringofnumbers
    #that do not have any preceding alphabets, so those will be ones with .co.uk/news or .com/news

def determine_category_file(url):
    if 'entertainment' in url:
        return 'entertainment.csv'
    elif 'business' in url:
        return 'business.csv'
    elif 'australia' in url:
        return 'australia.csv'
    elif 'asia' in url:
        return 'asia.csv'
    elif 'technology' in url:
        return 'technology.csv'
    elif 'europe' in url:
        return 'europe.csv'
    elif 'middle-east' in url:
        return 'europe.csv'
    elif 'latin_america' in url:
        return 'latin_america.csv'
    elif 'africa' in url:
        return 'africa.csv'
    else:
        return 'ignore'

begin_crawling_from_this_page('http://www.bbc.com/news/technology-34391038', 3)
