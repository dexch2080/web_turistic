from django.shortcuts import render
from django.views.generic import ListView,DetailView
from . import models,forms,verificator
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import template
from django.views.decorators.csrf import csrf_protect
from ipware import get_client_ip

register = template.Library()

class Places(ListView):
    model = models.Tour
    template_name = "places/touristic_zones.html"

class Place(DetailView):
    queryset = models.Tour.objects.all()
    template_name = "places/tour.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = super().get_object()
        context['images'] = models.Image.objects.filter(tour=obj.pk)
        return context

@csrf_protect
def login(request):
    success = None
    if request.method == 'POST':
        form = forms.Account(request.POST)    
        success = False
        if form.is_valid():
            (ip,routable) = get_client_ip(request)
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            (verified, success) = verificator.rand_sender(name,email,ip)
    else:
        form = forms.Account()
        
    return render(request,'places/user.html',{'form': form , 'success': success})

@csrf_protect
def verify(request):
    token = request.POST.get('token')
    email = request.POST.get('email')
    if verificator.check_token(token,email):
        return HttpResponseRedirect(reverse('places:tours'))
    else:
        return HttpResponseRedirect(reverse('places:login'))

@csrf_protect
def leave_comment(request,pk):
    (ip,_) = get_client_ip(request)    
    verified = verificator.check_verification(ip)

    #if verified
    if verified:
        tour = models.Tour.objects.get(pk=pk)
        account = models.Account.objects.get(ip=ip)
        cmt = request.POST.get('comment')
        models.Comment.objects.create(tour=tour,account=account,comment=cmt)
    #if not 


    return HttpResponseRedirect(reverse('places:tour',{'pk':pk}))

def only_test(request):
    (ip,_) = get_client_ip(request)
    verificator.test(ip)
    return HttpResponseRedirect(reverse('places:tours'))