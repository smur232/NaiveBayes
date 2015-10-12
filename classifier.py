import string, pickle, time
from math import log
from collections import Counter, defaultdict, deque

from web_crawler import begin_crawling_from_this_page, determine_category_file, collect_links
from article_parser import get_all_body_p_tags_bbc, get_soup_of_page
from pickle_reader import read_object_from


def get_most_likely_category(word_count_new_article):
    probability_dict = dict()
    categories = ['business', 'asia', 'technology', 'uk', 'europe']
    for category in categories:
        update_probabilities(category)
        category_word_probabilities = read_object_from(category + '_probability.p', defaultdict)
        probability_dict[category] = get_total_probability(category_word_probabilities, word_count_new_article, category)
    largest_probability = max(probability_dict.values())
    likely_category = [x for x, y in probability_dict.items() if y == largest_probability]
    return likely_category[0]


def count_words_in_article(url):
    soup = get_soup_of_page(url)
    p_tags = get_all_body_p_tags_bbc(soup)
    word_counter = Counter()
    for pTag in p_tags:
        contents = str(pTag.contents[0])

        if 'href' not in contents and 'span' not in contents:
            word_counter.update(split_into_words(contents))
    return word_counter


def split_into_words(contents):
    return [word.strip(string.punctuation).lower() for word in contents.split()]


def get_probability_of_word(word, probability_dict, total_word_count):
    probability = probability_dict[word]
    if probability == 0:
        return 1/(total_word_count+2)
        # (1/ 1000000) (1/100
    return probability


def get_probability_of_category(category):
    a = read_object_from('articles_read_counter.p', Counter)
    total_num_articles = sum(a.values())
    return a[category] / total_num_articles


def get_total_probability(probability_of_words_for_category, new_article_word_counter, category):
    total_probability = get_probability_of_category(category)
    total_num_of_words = probability_of_words_for_category['num_of_words']
    for word, count in new_article_word_counter.items():
        if len(word) > 3:
            total_probability += (log(get_probability_of_word(word, probability_of_words_for_category, total_num_of_words)))
    return total_probability


def update_probabilities(category):
    word_count = read_object_from(category + '.p', Counter)
    total_num_words = sum(word_count.values())
    # prob_of_word_not_seen = lambda: 1/total_num_words
    word_probabilities = defaultdict(int)

    word_probabilities['num_of_words'] = total_num_words

    for word, count in word_count.items():
        # 全てのカウントに１を足します
        word_probabilities[word] = (count+1)/(total_num_words + 2)
    pickle.dump(word_probabilities, open(category + '_probability.p', 'wb'))
    return word_probabilities


def get_count_from_text_file(filename):
    word_counter = Counter()
    with open(filename) as f:
        lines = f.readlines()
        for line in lines:
            word_counter.update(split_into_words(line))
        return word_counter


def test_precision_recall(url, category, max_num_of_articles):
    links = deque()
    links.append(url)
    count = 0

    articles_in_training_set = read_object_from('visited_pages_set.p', set)
    articles_in_testing = read_object_from('tested_articles_url.p', set)
    print(articles_in_testing)
    while links and count < max_num_of_articles:
        try:
            next_url = links.popleft()
            soup = get_soup_of_page(next_url)
            links.extend(collect_links(soup))

            if next_url in articles_in_training_set or next_url in articles_in_testing:
                continue

            time.sleep(1)

            article_category = determine_category_file(next_url)
            if article_category != category:
                continue

            word_counter_new_article = count_words_in_article(next_url)
            category_guess = get_most_likely_category(word_counter_new_article)

            print('Currently going through ', next_url, ':')
            articles_in_testing.add(next_url)
            count += 1
            print('     Your guess is', category_guess, '. The actual category is', article_category)

        except AttributeError:
            print('something went wrong, here', next_url, 'we will look at the next link')
            continue

        except Exception as e:
            print('an unexpected error occurred, we will look at the next link: ', e)
            continue

    print('I have looked at', count, 'articles')
    pickle.dump(articles_in_testing, open('tested_articles_url.p', 'wb'))
