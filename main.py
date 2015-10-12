from web_crawler import whats_in_my_pickle, begin_crawling_from_this_page
from classifier import get_most_likely_category, get_count_from_text_file, count_words_in_article, test_precision_recall


def main():
    # カテゴリーごとに記事を何ページ読んだかをプリントします
    whats_in_my_pickle()

    # URL からクロールします
    # begin_crawling_from_this_page('http://www.bbc.co.uk/news/technology-32545081', 20)

    # テストするには、まず文字のカウンターをURL かテキストファイルからつくって、get_most_likely_category
    # にインプットしてください。

    # テキストファイルから、文字のカウンターオブジェクトを作ります
    # word_counter_new_article = get_count_from_text_file('new_article')

    # URL から文字カウンターを作ります
    # word_counter_new_article = count_words_in_article('http://www.bbc.com/news/world-asia-india-34472166')

    # カウンターオブジェクトを使って、カテゴリーをアウットプットします
    # get_most_likely_category(word_counter_new_article)

    # ここにURL を入れて、クロールしたいカテゴリーを入れて、探し出すページ数をいれると、
    # 教師データには入っていない記事のカテゴリーを判断して、プリントします
    # ですが、教師データに入っていない記事を見つけるのが難しいと、時間がかかってしまうときがあるので、
    # その場合は上の方法でテストをお願いいたします。

    # test_precision_recall('http://www.bbc.com/news/world/asia', 'asia', 35)

main()
