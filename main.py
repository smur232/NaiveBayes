from web_crawler import whats_in_my_pickle, begin_crawling_from_this_page
from classifier import get_most_likely_category, get_count_from_text_file, count_words_in_article

# カテゴリーごとに記事を何ページ読んだかをプリントします
whats_in_my_pickle()

# URL からクロールします
# begin_crawling_from_this_page('http://www.bbc.co.uk/news/technology-32545081', 20)
# begin_crawling_from_this_page('http://www.bbc.co.uk/news/technology-34199825', 20)
# begin_crawling_from_this_page('http://www.bbc.com/news/world-asia-india-34387986', 20)

# テキストファイルから、文字のカウンターオブジェクトを作ります
# word_counter_new_article = get_count_from_text_file('new_article')

# URL から文字カウンターを作ります
# word_counter_new_article = count_words_in_article('http://www.bbc.com/news/world-asia-india-34472166')

# カウンターオブジェクトを使って、カテゴリーをアウットプットします
# print(get_most_likely_category(word_counter_new_article))
