from django.core.paginator import Paginator, EmptyPage

from django.conf import settings

import jwt

def paginate_webhooks(request, webhooks, results):
    page = request.GET.get('page', 1)
    paginator = Paginator(webhooks, results)
    try:
            webhooks = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        webhooks = paginator.page(page)

    left_index = (int(page) - 2)
    if left_index < paginator.num_pages:
        left_index = 1

    right_index = (int(page) + 3)
    if right_index > paginator.num_pages:
        right_index = paginator.num_pages + 1
        
    custom_range = range(left_index, right_index)

    return custom_range, webhooks

def create_jwt(name):
    encoded_jwt = jwt.encode({'webhook': name }, settings.JWT_SECRET, algorithm="HS256")

    return encoded_jwt


