from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from image.models import Image


def upload_img(request):
    """
    上传图片
    :param request: 图片名name, 图片文件
    :return:
    """
    if request.method == 'POST':
        image = Image(
            name=request.POST.get('name'),
            img=request.FILES.get('img'),
        )
        image.save()
    return JsonResponse(data={"result": "upload success"})


def show_img(request):
    """
    展示图片
    :param request: 图片id
    :return:
    """
    image = Image.objects.get(id=request.GET['imageID'])
    return JsonResponse(data={"result": image.img.url})
