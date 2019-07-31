# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
import test_call
import create_account
import json
import change_campaign_state
import get_campaigns
import get_adgroups
import create_ad_group
import newtest
import add_search_ad
import add_display_ad as create_display_ad
import add_conversion_tracker
import create_AdGroup
import location_track
import get_report

# Create your views here.
def create_campaign(request):
    mydata = json.loads(request.body.decode("utf-8"))
    print(mydata)
    result = test_call.main(mydata)
    print(result)
    text = """<h1>You have succesfully created a search campaign!</h1>"""
    return JsonResponse(result, safe=False)

def create_new_account(request):
    mydata = json.loads(request.body.decode("utf-8"))
    manager_customer_id = mydata['manager_customer_id']
    account_name = mydata['account_name']
    currency_code = mydata['currency_code']
    time_zone = mydata['time_zone']

    response = create_account.create(manager_customer_id, account_name, currency_code, time_zone)
    result = {}
    result['customer_id']  = (response.resource_name)[10:]
    return JsonResponse(result, safe=False)

def set_campaign_state(request):
    mydata = json.loads(request.body.decode("utf-8"))
   
    change_campaign_state.main(mydata)

    if (mydata['state'] == "ENABLED"):
        text = """<h1>You have enabled the requested campaign</h1>"""
    else:
       text = """<h1>You have paused the requested campaign</h1>""" 
    
    return HttpResponse(text)

def get_campaign_data(request):
    print(request.body)
    mydata = json.loads(request.body.decode("utf-8"))
    customer_id = mydata['customer_id']
    campaign_id = mydata['campaign_id']

    result = get_campaigns.main(customer_id, campaign_id, 0)
    result['id'] = customer_id
    return JsonResponse(result, safe=False)

def get_ad_groups(request):
    mydata = json.loads(request.body.decode("utf-8"))
    customer_id = mydata['customer_id']
    campaign_id = mydata['campaign_id']

    result = get_adgroups.main(customer_id, campaign_id)
    return JsonResponse(result, safe=False)

def add_ad_groups(request):
    mydata = json.loads(request.body.decode("utf-8"))
    print(mydata)
    result = create_ad_group.main(mydata)
    return JsonResponse(result, safe=False)

def add_text_ad(request):
    mydata = json.loads(request.body.decode("utf-8"))
    print(mydata)
    result = add_search_ad.main(mydata)
    return JsonResponse(result, safe=False)

def add_display_ad(request):
    mydata = json.loads(request.body.decode("utf-8"))
    print(mydata)
    result = create_display_ad.main(mydata)
    return JsonResponse(result, safe=False)


def test(request):
    mydata = json.loads(request.body.decode("utf-8"))
    newtest.main(mydata)
    text = """<h1>You have paused the requested campaign</h1>"""
    return HttpResponse(text)

def create_conversion_tracker(request):
    mydata = json.loads(request.body.decode("utf-8"))
    add_conversion_tracker.main(mydata)

    text = """<h1>You have paused the requested campaign</h1>"""
    return HttpResponse(text)

def test_new_ad_group(request):
    mydata = json.loads(request.body.decode("utf-8"))
    create_AdGroup.main(mydata)
    text = """<h1>You have paused the requested campaign</h1>"""
    return HttpResponse(text)

def get_location(request):
    location_track.main()
    text = """<h1>You have paused the requested campaign</h1>"""
    return HttpResponse(text)

def get_statistics(request):
    mydata = json.loads(request.body.decode("utf-8"))
    result = get_report.main(mydata)
    
    return JsonResponse(result, safe=False)
