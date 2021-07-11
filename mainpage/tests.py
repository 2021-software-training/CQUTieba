from mainpage.models import Article


def show_user_article(request):
    """
    获得指定用户的历史文章，并将文章放入列表之中[article1, article2, ....]
    article为dict <--> json
    包括标题title，时间time，类别1article_type1, 类别2article_type2，类别3article_type3
    :param request {
        authorID: author_id
        }:
    :return [article1, article2, ....]:
    """