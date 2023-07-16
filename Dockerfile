#파이썬 3.9버전 이미지를 사용해 빌드
FROM python:3.9

# .pyc 파일을 생성하지 않도록 설정합니다.
ENV PYTHONDONTWRITEBYTECODE 1
# 파이썬 로그가 버퍼링 없이 즉각적으로 출력하도록 설정합니다.
ENV PYTHONUNBUFFERED 1
ENV PYTHONIOENCODING=utf-8

# docker 내 프로젝트 루트폴더 생성
RUN mkdir /app 
# 현재 디렉토리 모든 폴더/파일 옮기기
ADD . /app 

# docker 작업 폴더설정
WORKDIR /app 

RUN python3 -m pip install --upgrade pip
# 프로젝트 실행에 필요한 패키지들을 설치합니다.
RUN pip3 install poetry
# 가상환경 안만들기
RUN poetry config virtualenvs.create false
# --no-root : doest not contain any element 오류 해결
RUN poetry install --no-root

EXPOSE 8000
CMD python3 manage.py makemigrations && python3 manage.py migrate && python3 manage.py runserver 0.0.0.0:8000
