import datetime
import json
import logging

from django.contrib.auth.models import User
from django.forms.models import model_to_dict
from django.http import HttpResponse

logger = logging.getLogger(__name__)



class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, (datetime.datetime, datetime.date)):
            return o.isoformat()
        return json.JSONEncoder.default(self, o)


def users(request):
    users = [
        {
            k:v
            for k, v in model_to_dict(user).items()
            if k in ("id", "username", "first_name", "last_name", "email", "is_active")
        }
        for user in User.objects.all()
    ]
    logger.info("headers in view.users: %r", request.headers)
    return HttpResponse(
        json.dumps({"users": users}, ensure_ascii=False, cls=JSONEncoder),
        content_type="application/json",
    )
