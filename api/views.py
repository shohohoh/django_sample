# -*- coding: utf-8 -*-

import json
from collections import OrderedDict
from django.http import HttpResponse, Http404
from cms.models import Book
from django.views.decorators.csrf import csrf_exempt
import pdb

def render_json_response(request, data, status=None):
    '''response を JSON で返却'''
    json_str = json.dumps(data, ensure_ascii=False, indent=2)
    callback = request.GET.get('callback')
    if not callback:
        callback = request.REQUEST.get('callback')  # POSTでJSONPの場合
    if callback:
        json_str = "%s(%s)" % (callback, json_str)
        response = HttpResponse(json_str, content_type='application/javascript; charset=UTF-8', status=status)
    else:
        response = HttpResponse(json_str, content_type='application/json; charset=UTF-8', status=status)
    return response

def book_list(request):
    '''書籍と感想のJSONを返す'''
    books = []
    for book in Book.objects.all().order_by('id'):

        impressions = []
        for impression in book.impressions.order_by('id'):
            impression_dict = OrderedDict([
                ('id', impression.id),
                ('comment', impression.comment),
            ])
            impressions.append(impression_dict)

        book_dict = OrderedDict([
            ('id', book.id),
            ('name', book.name),
            ('publisher', book.publisher),
            ('page', book.page),
            ('impressions', impressions)
        ])
        books.append(book_dict)

    data = OrderedDict([ ('books', books) ])
    return render_json_response(request, data)

@csrf_exempt
def receive_json(request):
    print 'aaaaaaaaaaaaaaaa'
    # pdb.set_trace()
    '''受け取ったJSONを返す'''
    if request.method == 'POST':
        data = request.POST
        # aaa = json.loads(request.body)
        # print request.body
        datas = OrderedDict([ ('receive', "send from python!!") ])
        return render_json_response(request, datas)
    else:
        raise Http404