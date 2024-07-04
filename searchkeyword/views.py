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
