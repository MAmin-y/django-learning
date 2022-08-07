from .models import Profile, Skill
from django.db.models import Q     #baraye and va or kardan parametr haye filter to search


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