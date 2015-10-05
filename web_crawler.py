import requests
import re
import time
import pickle

from collections import deque
from collections import Counter
from bs4 import BeautifulSoup
from trying_pickle import whats_in_my_pickle


def begin_crawling_from_this_page(url, max_num_of_articles=20):
    # max_num_of_articles は何ページアクセスする数ではなくて、何ページものの記事が欲しいかを決めます。
    # 現在はページをアクセスするたびにconsoleにprintしているので結構console output が多いです

    links = deque()
    links.append(url)
    count = 0
    pages_visited = get_pages_visited()
    articles_read_for_category = get_article_counts()
    print('pages visited before: ', pages_visited)
    print('articles read before: ', articles_read_for_category)

    while links and count < max_num_of_articles:
        url = links.popleft()

        if url in pages_visited:
            continue
        pages_visited.add(url)
        time.sleep(1)

        written_to_file = write_body_to_file(url, links)

        if written_to_file:
            # .update takes a file name and increments the counter for it
            articles_read_for_category.update([written_to_file])
            count += 1

    pickle.dump(articles_read_for_category, open('articles_read_counter.p', 'wb'))
    pickle.dump(pages_visited, open('url_visited_sites_set.p', 'wb'))
    return

def get_pages_visited():

    try:
        return pickle.load(open('url_visited_sites_set.p', 'rb')) # just in case the input was not a set

    except FileNotFoundError:
        return set()


def get_article_counts():
    try:
        return pickle.load(open('articles_read_counter.p', 'rb'))
    except FileNotFoundError:
        return Counter()


def write_body_to_file(url,links):
    file_to_write_to = determine_category_file(url)

    if file_to_write_to == 'ignore':
        print('This url was ignored:', url)
        return

    print('Currently going through ', url, ':')
    f = open(file_to_write_to, 'a')

    try:
        r = requests.get(url)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        # it is getting a div called component__tweet!!
        links.extend(collect_links(soup))

        pTags = get_all_body_p_tags(soup)

        for pTag in pTags:
            contents = str(pTag.contents[0])
            if 'href' not in contents and 'span' not in contents:
                f.write(contents + '\n')

    except AttributeError:
        print('     This page does not have a body article: ', url)

    except Exception as e:
        print('Had some problem parsing through this page: ', url, e)

    else:
        print('     successfully written to file', file_to_write_to)

    finally:
        f.close()
        return file_to_write_to


def get_all_body_p_tags(soup):
    # 後で、新しい記事のカテゴリーを決める時に使える function です
    body_div_tag = soup.find('div', {'class': 'story-body__inner'})
    p_tags = body_div_tag.find_all('p', class_=lambda class_tag: class_tag == 'story-body__introduction' or class_tag == None, attrs={'style':None})
    return p_tags


def collect_links(soup):
    links = ['http://www.bbc.com' + link.get('href') for link in soup.find_all(href=path_to_articles)]
    return links


def path_to_articles(href):
    # (?<![a-z]) this is saying to find all the /news/somestringofwords/stringofnumbers
    # that do not have any preceding alphabets, so those will be ones with .co.uk/news or .com/news
    return href and re.compile("(?<![a-z])/news/[\w-]+-[\d]+").search(href)


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
        return 'middle_east.csv'
    elif 'latin-america' in url:
        return 'latin_america.csv'
    elif 'africa' in url:
        return 'africa.csv'
    elif 'canada' in url:
        return 'us_canada.csv'
    elif 'science' in url:
        return 'science.csv'
    elif 'uk' in url:
        return 'uk.csv'
    elif 'education' in url:
        return 'education.csv'
    else:
        return 'ignore'


def whats_in_my_pickle():
    a = get_article_counts()
    b = get_pages_visited()
    print('Total number of articles: ', sum(a.values()))
    print('Total number of links: ', len(b))
    print(a)
    print(b)


begin_crawling_from_this_page('http://www.bbc.com/news/world-asia-34398371', 10)
whats_in_my_pickle()
