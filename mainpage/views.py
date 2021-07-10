import json
from django.http import HttpResponse


def add_article(request):
    """
    用于新增文章
    :param request: {
        articleID, authorId, articleText
            articleAudio(默认先不管这个 默认这个为空) articleTitle
                articleType1 articleType2 articleType3
        }
    :return: json形式的 {result: "yes"/"no"}
    """
    pass


def add_comment(request):
    """

    :param request: {
        commentText, commentID, articleID
            commentAudio(先默认为空)
        }
    :return:
    """
