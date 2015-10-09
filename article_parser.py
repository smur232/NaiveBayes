import requests
from bs4 import BeautifulSoup


def get_all_body_p_tags_bbc(soup):
    # 後で、新しい記事のカテゴリーを決める時に使える function です
    body_div_tag = soup.find('div', {'class': 'story-body__inner'})
    p_tags = body_div_tag.find_all('p', class_=lambda class_tag: class_tag == 'story-body__introduction'or class_tag is None, attrs={'style': None})
    return p_tags


def get_all_body_p_tags_nyt(soup):
    # New York Times の記事のボディーをとります
    # TODO: collect_links and path_to_articles for nyt

    p_tags = soup.find_all('p', {'class': 'story-body-text'})
    return p_tags


def get_soup_of_page(url):
    r = requests.get(url)
    r.raise_for_status()
    return BeautifulSoup(r.text, "html.parser")

