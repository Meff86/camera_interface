from django.core.serializers.json import DjangoJSONEncoder
from datetime import datetime

class CustomJSONEncoder(DjangoJSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.strftime('%Y-%m-%d %H:%M:%S')
        return super().default(o)
