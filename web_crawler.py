import requests
import re
import time
import pickle
import string
import traceback

from collections import deque
from collections import Counter
from bs4 import BeautifulSoup


def begin_crawling_from_this_page(url, max_num_of_articles=20):
    # max_num_of_articles は何ページアクセスする数ではなくて、何ページものの記事が欲しいかを決めます。
    # 現在はページをアクセスするたびにconsoleにprintしているので結構console output が多いです

    links = deque()
    links.append(url)
    count = 0
    pages_visited = read_object_from('visited_pages_set.p', set)
    articles_read_for_category = read_object_from('articles_read_counter.p', Counter)
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
    pickle.dump(pages_visited, open('visited_pages_set.p', 'wb'))
    return


def write_body_to_file(url,links):
    # トレイニングデータを作るために使います
    article_category = determine_category_file(url)

    if article_category == 'ignore':
        print('This url was ignored:', url)
        return

    print('Currently going through ', url, ':')
    f = open(article_category + '.csv', 'a')

    try:
        r = requests.get(url)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        links.extend(collect_links(soup))

        p_tags = get_all_body_p_tags(soup)
        a = read_object_from(article_category + '.p', Counter)
        for pTag in p_tags:
            contents = str(pTag.contents[0])

            # 後で見れるように、CSV ファイルにも書いて、pickle にも文字のカウンターをアップデートします
            if 'href' not in contents and 'span' not in contents:
                f.write(contents + '\n')
                a.update(word.strip(string.punctuation).lower() for word in contents.split())
        pickle.dump(a, open(article_category + '.p', 'wb'))

    except AttributeError:
        print('     This page does not have a body article: ', url)

    except Exception as e:
        ('Had some problem parsing through this page: ', url, e)
        traceback.print_exc()

    else:
        print('     successfully written to file', article_category)

    finally:
        f.close()
        return article_category


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


def read_object_from(filename, object_type):
    # pickle からオブジェクとを読み取ります、欲しい object_type とマッチしているかをチェックします
    # object_type　がマッチしなければ、空の object_type を return します

    try:
        read_object = pickle.load(open(filename, 'rb'))
        assert type(read_object) is object_type
        return read_object

    except FileNotFoundError:
        return object_type()

    except AssertionError:
        print('         The object read from', filename, 'is not a', object_type, '!')
        return object_type()

    except Exception:
        return object_type()


def determine_category_file(url):
    if 'entertainment' in url:
        return 'entertainment'
    elif 'business' in url:
        return 'business'
    elif 'australia' in url:
        return 'australia'
    elif 'asia' in url:
        return 'asia'
    elif 'technology' in url:
        return 'technology'
    elif 'europe' in url:
        return 'europe'
    elif 'middle-east' in url:
        return 'middle_east'
    elif 'latin-america' in url:
        return 'latin_america'
    elif 'africa' in url:
        return 'africa'
    elif 'canada' in url:
        return 'us_canada'
    elif 'science' in url:
        return 'science'
    elif 'uk' in url:
        return 'uk'
    elif 'education' in url:
        return 'education'
    else:
        return 'ignore'


def whats_in_my_pickle():
    print("\nWhat's in my pickle objects? ")
    a = read_object_from('articles_read_counter.p', Counter)
    b = read_object_from('visited_pages_set.p', set)
    c = read_object_from('europe.p', Counter)
    print(' Total number of articles:', sum(a.values()))
    print(' Total number of links:', len(b))
    print(a)
    print(b)
    print(c)


#begin_crawling_from_this_page('http://www.bbc.com/news/world-europe-34442121', 2)
whats_in_my_pickle()
