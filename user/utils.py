from .models import Profile, Skill
from django.db.models import Q     #baraye and va or kardan parametr haye filter to search
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def search_profiles(request):
    search_query = ""

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')
    
    skills = Skill.objects.filter(name__icontains=search_query)
    profiles = Profile.objects.distinct().filter(Q(name__icontains=search_query) | 
                                           Q(short_intro__icontains=search_query) |
                                           Q(skill__in=skills))                    #age search_query khali bashe hamaro mide age
                                                                                    # na filter mikone oon arguman bara case sensitive boodaneshe
                                                                                    # mishod jaye | , & gozasht
                                                                                    #age distinct nabashe duplicate mishe 
    return profiles, search_query


def paginate_profiles(request, profiles, results):
    page = request.GET.get('page')
    paginator = Paginator(profiles, results)
    
    try:
        profiles = paginator.page(page)
    except EmptyPage:                                       # age ye page bishtar az mojood dade shod boro page akhar
        page = paginator.num_pages
        profiles = paginator.page(page)
    except PageNotAnInteger:                                # defult page 1 bashe
        page = 1
        profiles = paginator.page(page)
    
    left_index = int(page) - 4
    if left_index < 1:
        left_index = 1
    
    rigt_index = int(page) +5
    if rigt_index > paginator.num_pages:
        rigt_index = paginator.num_pages

    custom_range = range(left_index, rigt_index + 1)
    return custom_range , profiles