from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from assets.forms import RAMForm,AssetForm,NICForm
from assets.models import Asset, NIC
import time

# Create your views here.
def index(request):
    return render(request,'default/index.html',locals())

def auth_error(request):
    return render(request,'default/error_auth.html',locals())

def success(request):
    return render(request,'default/success.html',locals())

def test(request):

    nowtime = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
    asset_num = "DS-server" + nowtime
    af = Asset.objects.create(asset_number = asset_num)
    print af.asset_number

    if request.method == 'POST':
        auuid = af.uuid
        adata = Asset.objects.filter(uuid=auuid).update(mark='True')
        for i in range(6):
            nic_name = "nic_name" + str(i)
            nic_name = request.POST.get(nic_name)

            nic_memo = "nic_memo" + str(i)
            nic_memo = request.POST.get(nic_memo)

            nic_macaddress = "nic_macaddress" + str(i)
            nic_macaddress = request.POST.get(nic_macaddress)

            nic_ipaddress = "nic_ipaddress" + str(i)
            nic_ipaddress = request.POST.get(nic_ipaddress)

            nic_netmask = "nic_netmask" + str(i)
            nic_netmask = request.POST.get(nic_netmask)

            nic_model = "nic_model" + str(i)
            nic_model = request.POST.get(nic_model)

            if nic_name and nic_macaddress:
                NIC.objects.create(asset = af,name=nic_name,model=nic_model,macaddress=nic_macaddress,
                ipaddress=nic_ipaddress,netmask=nic_netmask,memo=nic_memo)
        return HttpResponseRedirect('/allow/welcome/')

    if af.mark == 'False':
        af.delete()
        print 'af DELETE'



    # nowtime = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
    # asset_num = "DS-server" + nowtime
    # af = Asset.objects.create(asset_number = asset_num)
    # print af.uuid
    # print af.mark
    # nf = NICForm()
    # if request.method == 'POST':
    #     auuid = af.uuid
    #     adata = Asset.objects.filter(uuid=auuid).update(mark='True')
    #     nf = NICForm(request.POST)
    #     if nf.is_valid():
    #         result = nf.save(commit=False)
    #         result.asset = af
    #         result.save()
    #         return HttpResponseRedirect('/allow/welcome/')

    # if af.mark == 'False':
    #     af.delete()
    #     print 'DELETE'
    return render(request,'default/test233.html',locals())
    #     assetid = Asset.objects.get(asset_number='DS-server20160629001')

    # nf = NICForm()
    # if request.method == 'POST':
    #     nf = NICForm(request.POST)

    #     if nf.is_valid():
    #         result = nf.save(commit=False)
    #         result.asset = assetid
    #         result.save()
    #         return HttpResponseRedirect('/allow/welcome/')
    # return render(request,'default/test.html',locals())

def navtest(request):
    return render(request,'default/test233.html',locals())