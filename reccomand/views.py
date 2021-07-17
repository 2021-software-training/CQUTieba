from django.shortcuts import render
from recommand.base_on_tag import tag_recommand
from recommand.base_on_weight import weight_recommand
from recommand.base_on_content import content_recommand
# Create your views here.
def get_recommand(request):
    if request.method == 'GET':
        user_id = request.GET['userID']
        temp = []
        temp.append(weight_recommand())
        temp += content_recommand(user_id)[1]
        temp += tag_recommand(user_id)
        return temp
    #获取推荐的文章