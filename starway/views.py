from django.shortcuts import render, redirect, get_object_or_404
from page.models import Page 
from .models import Member, Case, Service, CaseCategory, ServiceCategory




def index(request):
    page, _ = Page.objects.get_or_create(code="index")
    return render(request, 'starway/index.html', locals())

    
def contacts(request):
    page, _ = Page.objects.get_or_create(code="contacts")
    return render(request, 'starway/contacts.html', locals())

    
def profile(request):
    page, _ = Page.objects.get_or_create(code="profile")
    return render(request, 'starway/profile.html', locals())


    
def service_categories(request):
    page, _ = Page.objects.get_or_create(code="service_categories")
    service_categories = ServiceCategory.objects.all()
    return render(request, 'starway/service_categories.html', locals())

    
def services_list(request, slug):
    service_category = get_object_or_404(ServiceCategory, slug=slug)
    page = service_category 
    services = Service.objects.all().filter(category=service_category)
    services = service_category.services.all()
    return render(request, 'starway/services_list.html', locals())

    
def service(request, slug):
    service = get_object_or_404(Service, slug=slug)
    page = service
    return render(request, 'starway/service.html', locals())

    
def case_categories(request):
    page, _ = Page.objects.get_or_create(code="case_categories")
    case_categories = CaseCategory.objects.all()
    return render(request, 'starway/case_categories.html', locals())

    
def cases_list(request, slug):
    case_category = get_object_or_404(CaseCategory, slug=slug)
    slug  = case_category
    cases = Case.objects.filter(category=case_category)
    cases = case_category.cases.all()
    return render(request, 'starway/cases_list.html', locals())

    
def case(request, slug):
    page, _ = Page.objects.get_or_create(code="case")
    case = get_object_or_404(Case, slug=slug)
    return render(request, 'starway/case.html', locals())

    
def about(request):
    page, _ = Page.objects.get_or_create(code="about")
    return render(request, 'starway/about.html', locals())

    
def how_it_works(request):
    page, _ = Page.objects.get_or_create(code="how_it_works")
    return render(request, 'starway/how_it_works.html', locals())

    
def story(request):
    page, _ = Page.objects.get_or_create(code="story")
    return render(request, 'starway/story.html', locals())

    
def team(request):
    page, _ = Page.objects.get_or_create(code="team")
    team = Member.objects.all()
    return render(request, 'starway/team.html', locals())

    
def member(request, slug):
    page, _ = Page.objects.get_or_create(code="member")
    member = get_object_or_404(Member, slug=slug)
    return render(request, 'starway/member.html', locals())

    
def become_member(request):
    page, _ = Page.objects.get_or_create(code="become_member")
    return render(request, 'starway/become_member.html', locals())

    

