# Marine Mate

무더운 여름, 해수욕을 즐기고자 하는 사람들을 위해 각 지역별 수질, 수온, 해파리 출몰 예측과 같은 안전에 관한 정보를 제공하며, 해양레저/스포츠를 즐기려는 이들을 위해 지역별 운영 중인 추천 서비스 목록과 주변 편의시설 및 유동인구, 인구 밀집도에 따른 추천 알고리즘과 같은 인프라 정보를 제공합니다. 

## Tech Stack

**Framework:** Django REST framework

**DB:** (Local) SQLite / (Prod) MySQL

## Run Locally

Clone the project

```bash
  git clone git@github.com:weatherbetter/project-MarineMate-api.git
```

Prerequisite in Local

```bash
  pip install poetry
  poetry install
  pre-commit install
```
Start the server in Local

```bash
  poetry shell
  python manage.py makemigrations --settings=config.settings.local
  python manage.py migrate --settings=config.settings.local
  python manage.py runserver --settings=config.settings.local
```
