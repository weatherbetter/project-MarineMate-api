from django.contrib import admin


#db 생성 테스트

from .models import Beach
from .models import BeachInfra
from .models import WindSpeed
from .models import BeachScore
from .models import JellyfishScore
from .models import RainfallScore
from .models import Accident

# Register your models here.
admin.site.register(Beach)
admin.site.register(BeachInfra)
admin.site.register(WindSpeed)
admin.site.register(BeachScore)
admin.site.register(JellyfishScore)
admin.site.register(RainfallScore)
admin.site.register(Accident)