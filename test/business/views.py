from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
# from forms import BusinessForm, BugsForm
from models import Business,Bugs
# Create your views here.

@permission_required('assets.Can_add_business', login_url='/auth_error/')
def business_list(request):
    business_data = Business.objects.all()
    return render(request,'business/business_list.html',locals())


@permission_required('assets.Can_add_business', login_url='/auth_error/')
def bugs_list(request):
    bugs_data = Bugs.objects.all()
    return render(request,'business/bugs_list.html',locals())

