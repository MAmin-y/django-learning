from .models import Project, Tag
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def search_project(request):
    search_query = ""

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')
    
    tags = Tag.objects.filter(name__icontains=search_query)
    projects = Project.objects.distinct().filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(owner__name__icontains=search_query) |
            Q(tags__in=tags)
        )
    return projects, search_query


def paginate_project(request, projects, results):
    page = request.GET.get('page')
    paginator = Paginator(projects, results)
    
    try:
        projects = paginator.page(page)
    except EmptyPage:                                       # age ye page bishtar az mojood dade shod boro page akhar
        page = paginator.num_pages
        projects = paginator.page(page)
    except PageNotAnInteger:                                # defult page 1 bashe
        page = 1
        projects = paginator.page(page)
    
    left_index = int(page) - 4
    if left_index < 1:
        left_index = 1
    
    rigt_index = int(page) +5
    if rigt_index > paginator.num_pages:
        rigt_index = paginator.num_pages

    custom_range = range(left_index, rigt_index + 1)
    return custom_range , projects