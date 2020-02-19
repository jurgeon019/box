from django.shortcuts import render



def index(request):
    return render(request, 'index.html', locals())



def about(request):
    return render(request, 'about.html', locals())



def blog(request):
    return render(request, 'blog.html', locals())



def post(request, slug=None):
    return render(request, 'post.html', locals())



def contacts(request):
    return render(request, 'contacts.html', locals())



def catalog(request, slug=None):
    return render(request, 'catalog.html', locals())



def item(request, slug):
    return render(request, 'item.html', locals())


