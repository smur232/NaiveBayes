import requests
import re
import time
from collections import deque
from collections import Counter
from bs4 import BeautifulSoup


def begin_crawling_from_this_page(url, max_num_of_articles=20, pages_visited = set()):
    # max_num_of_articles は何ページアクセスする数ではなくて、何ページものの記事が欲しいかを決めます。
    # 現在はページをアクセスするたびにconsoleにprintしているので結構console output が多いです

    links = deque()
    pages_visited = set(pages_visited) # just in case the input was not a set
    links.append(url)
    count = 0
    articles_read_for_category = Counter()

    while links and count < max_num_of_articles:
        url = links.popleft()

        if url in pages_visited:
            continue
        pages_visited.add(url)
        time.sleep(1)

        written_to_file = write_body_to_file(url, links)

        if written_to_file:
            articles_read_for_category.update([written_to_file])
            count += 1

    return articles_read_for_category, pages_visited


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

    except AttributeError as e:
        print('     This page does not have a body article: ', url, e)

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
    else:
        return 'ignore'

latin_america_count, visited_pages = begin_crawling_from_this_page('http://www.bbc.com/news/world-latin-america-34405302', 10)
print('Read', sum(latin_america_count.values()), 'articles')
print(latin_america_count.items())

f = open('Articles_Read', 'a')
f.write(str(visited_pages) + '\n')
f.write(str(latin_america_count.items()) + '\n')
f.close()
