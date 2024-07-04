[공식문서](https://docs.djangoproject.com/ko/5.0/intro/tutorial01/)를 참고했습니다.

```jsx
$ pip install django

$ python -m django --version
5.0.6
```

<br>

현재 디렉토리에서 `mysite`라는 디렉토리를 생성

mysited안에는 자동으로 생성된 파일들이 있음 

```jsx
$ django-admin startproject mysite

$ tree 
.
└── mysite
    ├── manage.py
    └── mysite
        ├── __init__.py
        ├── asgi.py
        ├── settings.py
        ├── urls.py
        └── wsgi.py

2 directories, 6 files
```

```bash
# 실행
$ python manage.py runserver
```

Django 개발 서버를 시작

개발 서버는 순수 Python으로 작성된 경량 웹 서버

![img](./tmp_img_folder/Untitled%20(21).png)

<br>

## 데이터베이스 (기본)


**mysite/settings.py :  Django 설정을 모듈 변수로 표현한 보통의 Python 모듈**

```bash
$ sudo apt-get update --fix-missing
$ sudo apt-get install -f

# 위 두 명령을 하지 않으면 오류가 떴다.
$ sudo apt install sqlite3
```

```bash
# 실행 
$ sqlite3 db.sqlite3
SQLite version 3.37.2 2022-01-06 13:25:41
Enter ".help" for usage hints.
sqlite> 
```

<br>

**기본 명령어**

```sql
# 사용 중인 DB를 볼 수 있다 
> .databases
main: /home/eunha/website2/mysite/db.sqlite3 r/w
```

```sql
# 생성된 테이블 확인 
> .tables
auth_group                  auth_user_user_permissions
auth_group_permissions      django_admin_log          
auth_permission             django_content_type       
auth_user                   django_migrations         
auth_user_groups            django_session  
```

<br>

나는 검색 키워드를 sort해서 상위 3개의 키워드만 노출하는 DB를 생성하고싶기 때문에 새로운 애플리케이션을 설치해주었다. 
searchkeyword 디렉토리 생성 됨 

```bash
$ python manage.py startapp searchkeyword

/mysite/searchkeyword$ tree
.
├── __init__.py
├── admin.py
├── apps.py
├── migrations
│   └── __init__.py
├── **models.py**
├── tests.py
└── views.py
```

<br>

**models.py 를 수정한다.**

```python
from django.db import models

class Search(models.Model):
    keyword = models.CharField(max_length=255)

    def __str__(self):
        return self.keyword
```

<br>

setting.py 에 내가 만든 테이블을 추가한다. (mysite에 있음)

```python
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    **'searchkeyword'**
]
```

<br>

데이터베이스에 저장한다.

```python
$ python manage.py makemigrations
Migrations for 'searchkeyword':
  **searchkeyword**/migrations/0001_initial.py
    - Create model Search
    
$ python manage.py migrate
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, searchkeyword, sessions
Running migrations:
  Applying **searchkeyword**.0001_initial... OK
```

<br>

`search` 테이블을 Django Admin 인터페이스를 통해 관리할 수 있도록 설정

admin.py 수정 

```python
from django.contrib import admin
from .models import Search

admin.site.register(Search)
```

<br>

사용자 생성

```python
$ python manage.py createsuperuser
Username (leave blank to use 'eunha'): eunha
Email address: 
Password: 1234
Password (again): 1234
# 너무 짧다고 하는데 그냥 yes 해주었다
```

<br>

서버를 연다 

```python
python manage.py runserver
```

/admin 경로로 이동하면 administrator 페이지로 접근 된다. 

![img](./tmp_img_folder/Untitled%20(22).png)

<br>

**방법 1. 웹페이지에서 직접**

![img](./tmp_img_folder/Untitled%20(25).png)

**방법 2.터미널 창에서 작업**

```python
$ python manage.py shell
>>> from searchkeyword.models import Search
>>> new_search = Search(keyword="감성")
>>> new_search.save()
>>> Search.objects.all()
<QuerySet [<Search: 힐링>, <Search: 감성>, <Search: 감성>]>
```

<br>

## 데이터베이스 (상위 3개만 index 페이지에 노출)

views.py 를 수정한다

```python
from django.shortcuts import render
from django.db.models import Count
from .models import Search

def index(request):
    # keyword 상위 3개 가져오기
    top_keywords = Search.objects.values('keyword').annotate(keyword_count=Count('keyword')).order_by('-keyword_count')[:3]
    return render(request, 'index.html', {'top_keywords': top_keywords})

```

<br>

urls.py 수정 (mysite 에 있음)

```python
from django.contrib import admin
from django.urls import path
from searchkeyword import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),  # index 뷰와 연결
]

```

<br>

mysite/templates/index.html 생성

```python
<!DOCTYPE html>
<html>
<head>
    <title>Top Keywords</title>
</head>
<body>
    <h1>Top 3 Keywords</h1>
    <ul>
        {% for keyword in top_keywords %}
            <li>{{ keyword.keyword }} ({{ keyword.keyword_count }} times)</li>
        {% endfor %}
    </ul>
</body>
</html>

```

<br>

settings.py 에 내용 추가

```python
**import os**

# ... (기존 설정)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [**os.path.join(BASE_DIR, 'templates')**],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# ... (기존 설정)
```

![img](./tmp_img_folder/Untitled%20(23).png)

searchkeyword 테이블에 저장된 상위 3개 (현재는 2개밖에 없음) 가 띄워진다.  따봉!! 

<br>

## 데이터베이스 (상위 3개만 index 페이지에 노출)

사용자 입력이 DB에 들어가도록 수정한다.

searchkeyword/forms.py  생성 

```python
from django import forms
from .models import Search

class SearchForm(forms.ModelForm):
    class Meta:
        model = Search
        fields = ['keyword']
```

<br>

searchkeyword/views.py를 수정한다.

```python
from django.shortcuts import render, redirect
from django.db.models import Count
from .models import Search
from .forms import SearchForm

def index(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = SearchForm()

    # keyword 상위 3개 가져오기 (기존 코드)
    top_keywords = Search.objects.values('keyword').annotate(keyword_count=Count('keyword')).order_by('-keyword_count')[:3]
    return render(request, 'index.html', {'form': form, 'top_keywords': top_keywords})

```

<br>

templates/index.html 수정

```python
<!DOCTYPE html>
<html>
<head>
    <title>Top Keywords</title>
</head>
<body>
    <h1>Top 3 Keywords</h1>
    <ul>
        {% for keyword in top_keywords %}
            <li>{{ keyword.keyword }} ({{ keyword.keyword_count }} times)</li>
        {% endfor %}
    </ul>

    <h2>Add a Keyword</h2>
    <form method="post">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit">Add Keyword</button>
    </form>
</body>
</html>

```

<br>

```python
python manage.py runserver
```

![img](./tmp_img_folder/Untitled%20(24).png)

잘 된다.