from django.db import models

# Create your models here.
from django.db import models

#---------------------------해수욕장 추천----------------------------------#

# 해수욕장
class Beach(models.Model):
    id = models.IntegerField(primary_key=True, null=False, default=0) # 해수욕장 코드
    beach_name = models.CharField(max_length=15) # 해수욕장명
    location = models.CharField(max_length=10) # 지역
    sigungu = models.CharField(max_length=10) # 시군구
    
    # 테이블명 지정
    class Meta:
        db_table = "Beach"
        
# 구급인프라
class SafetyInfra(models.Model):
    location = models.CharField(max_length=10) # 지역
    fs_cnt = models.IntegerField() # 소방서수
    sc_cnt = models.IntegerField() # 안전센터수
    fb_cnt = models.IntegerField() # 펌뷸런스수
    
    class Meta:
        db_table = "SafetyInfra"

# 인명구조장비
class LifesavingEquipment(models.Model):
    equipment_long = models.FloatField() # 인명구조장비함 경도
    equipment_lat = models.FloatField() # 인명구조장비함 위도
    spot = models.CharField(max_length=20) # 설치장소
    
    class Meta:
        db_table = "LifesavingEquipment"

# 해수욕장 시설
class BeachInfra(models.Model):
    shower_room = models.IntegerField() # 샤워장
    toilet = models.IntegerField() # 화장실
    dressing_room = models.IntegerField() # 탈의장
    watch_tower = models.IntegerField() # 망루대
    tap_water = models.IntegerField() # 공동수도
    # ForeignKey
    beach_id = models.ForeignKey(Beach, on_delete=models.CASCADE, db_column="beach_id")
    
    class Meta:
        db_table = "BeachInfra"

# 풍속
class WindSpeed(models.Model):
    date = models.DateField(auto_now=True) # 날짜
    wind_speed = models.IntegerField() # 풍속
    beach_name = models.CharField(max_length=15) # 해수욕장명
    # ForeignKey
    beach_id = models.OneToOneField(Beach, on_delete=models.CASCADE, db_column="beach_id")
    
    class Meta:
        db_table = "WindSpeed"

# 낮 최고기온
class MaxTemperature(models.Model):
    date = models.DateField(auto_now=True) # 날짜
    day_max_temp = models.FloatField() # 낮 최고기온
    beach_name = models.CharField(max_length=15) # 해수욕장명
    # ForeignKey
    beach_id = models.OneToOneField(Beach, on_delete=models.CASCADE, db_column="beach_id")
    
    class Meta:
        db_table = "MaxTemperature"

# 파고
class WaveHeight(models.Model):
    date = models.DateField(auto_now=True) # 날짜
    wave_height = models.FloatField() # 파고
    beach_name = models.CharField(max_length=15) # 해수욕장명
    # ForeignKey
    beach_id = models.OneToOneField(Beach, on_delete=models.CASCADE, db_column="beach_id")
    
    class Meta:
        db_table = "WaveHeight"

# 풍향
class WindDirection(models.Model):
    date = models.DateField(auto_now=True) # 날짜
    wind_direction = models.CharField(max_length=10) # 풍향
    beach_name = models.CharField(max_length=15) # 해수욕장명
    # ForeignKey
    beach_id = models.OneToOneField(Beach, on_delete=models.CASCADE, db_column="beach_id")
    
    class Meta:
        db_table = "WindDirection"

#---------------------------추천 모델----------------------------------#

# 해수욕장 점수
class BeachScore(models.Model):
    beach_name = models.CharField(max_length=15) # 해수욕장명
    water_score = models.FloatField() # 수질점수
    soil_score = models.FloatField() # 토양점수
    facility_score = models.FloatField() # 시설점수
    location = models.CharField(max_length=10) # 지역
    # ForeignKey
    beach_id = models.ForeignKey(Beach, on_delete=models.CASCADE, db_column="beach_id")
    
    class Meta:
        db_table = "BeachScore"

# 해파리 점수
class JellyfishScore(models.Model):
    jellyfish_score = models.IntegerField() # 해파리 점수
    date = models.DateField(auto_now=True) # 날짜
    location = models.CharField(max_length=10) # 지역
    # ForeignKey
    beach_id = models.ForeignKey(Beach, on_delete=models.CASCADE, db_column="beach_id")
    
    class Meta:
        db_table = "JellyfishScore"

# 강수 점수
class RainfallScore(models.Model):
    rain_score = models.FloatField() # 강수 점수
    rain_prob = models.FloatField() # 강수 확률
    date = models.DateField(auto_now=True) # 날짜
    beach_name = models.CharField(max_length=15) # 해수욕장
    # ForeignKey
    beach_id = models.ForeignKey(Beach, on_delete=models.CASCADE, db_column="beach_id")
    
    class Meta:
        db_table = "RainfallScore"


#---------------------------수난사고 현황----------------------------------#

# 수난사고
class Accident(models.Model):
    location = models.CharField(max_length=10) # 지역
    sigungu = models.CharField(max_length=10) # 시군구
    month = models.IntegerField() # 월
    place = models.CharField(max_length=10) # 장소
    cause  = models.CharField(max_length=30) # 원인
    
    class Meta:
        db_table = "Accident"



