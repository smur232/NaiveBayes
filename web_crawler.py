import re, pickle, string, time, traceback

from collections import deque, Counter, defaultdict
from article_parser import get_all_body_p_tags_bbc, get_soup_of_page, get_all_body_p_tags_nyt
from pickle_reader import read_object_from


def begin_crawling_from_this_page(url, max_num_of_articles=20):
    # max_num_of_articles は何ページアクセスする数ではなくて、何ページものの記事が欲しいかを決めます。
    # 現在はページをアクセスするたびに console に print しているので結構console output が多いです

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
        soup = get_soup_of_page(url)
        links.extend(collect_links(soup))

        p_tags = get_all_body_p_tags_bbc(soup)

        word_counter = read_object_from(article_category + '.p', Counter)
        for pTag in p_tags:
            contents = str(pTag.contents[0])

            # 後で見れるように、CSV ファイルにも書いて、pickle にも文字のカウンターをアップデートします
            if 'href' not in contents and 'span' not in contents:
                f.write(contents + '\n')
                word_counter.update(word.strip(string.punctuation).lower() for word in contents.split())
        pickle.dump(word_counter, open(article_category + '.p', 'wb'))

    except AttributeError:
        print('     This page does not have a body article: ', url)

    except Exception as e:
        print('Had some problem parsing through this page: ', url, e)
        traceback.print_exc()

    else:
        print('     successfully written to file', article_category)

    finally:
        f.close()
        return article_category


def collect_links(soup):
    links = ['http://www.bbc.com' + link.get('href') for link in soup.find_all(href=path_to_articles)]
    return links


def path_to_articles(href):
    # (?<![a-z]) this is saying to find all the /news/somestringofwords/stringofnumbers
    # that do not have any preceding alphabets, so those will be ones with .co.uk/news or .com/news
    return href and re.compile("(?<![a-z])/news/[\w-]+-[\d]+").search(href)


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
    print(' Total number of articles:', sum(a.values()))
    print(' Total number of links:', len(b))
    print(a)


# TODO:
# 1) take an article, parse the body text DONE
# 2) get the counts of those words DONE
# 3) then find the probability that this word occurs given it is a certain category DONE
# 4) automate getting probability for each category
# 5) take the best probability and output the result category
# implement a separate file that will take a new article, find the probabilities that it could be each
# of the categories, then take the category with the highest probability

# also we separate helper functions used in both article category determination and adding training data to
# a separate file so web crawler and determine category can use the same functions
