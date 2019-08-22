#!/usr/bin/env python
#
# Copyright 2016 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""This example adds campaigns.

To get campaigns, run get_campaigns.py.

The LoadFromStorage method is pulling credentials and properties from a
"googleads.yaml" file. By default, it looks for this file in your home
directory. For more information, see the "Caching authentication information"
section of our README.

"""

import datetime
import uuid
from googleads import adwords
import add_conversion_tracker
import location_track

  
def CreateBiddingStrategy(client, bidding_strategy, amount):
  """Creates a bidding strategy object.

  Args:
    client: AdWordsClient the client to run the example with.

  Returns:
    dict An object representing a bidding strategy.
  """



  if (amount > 0):
      amount = float(amount * 100000.0)
  # Initialize appropriate service.
  bidding_strategy_service = client.GetService(
      'BiddingStrategyService', version='v201809')

  shared_bidding_strategy = 0

  if (bidding_strategy == "CPC"):
      shared_bidding_strategy = {
      'name': 'CPC %s' % uuid.uuid4(),
      'biddingScheme': {
          'xsi_type': 'ManualCpcBiddingScheme',
      }
    }
  elif (bidding_strategy == "CPM"):
      shared_bidding_strategy = {
      'name': 'CPM %s' % uuid.uuid4(),
      'biddingScheme': {
          'xsi_type': 'ManualCpmBiddingScheme',
      }
    }
  elif (bidding_strategy == "CPA"):
      shared_bidding_strategy =  {
           'name': "CPA %s" % uuid.uuid4(),
           'biddingScheme': {
                'xsi_type': 'TargetCpaBiddingScheme',
                 # Optionally set additional bidding scheme parameters.
                'targetCpa': {
                    'microAmount': '2000000'
                }
            }
      }

  operation = {
      'operator': 'ADD',
      'operand': shared_bidding_strategy
  }

  response = bidding_strategy_service.mutate([operation])
  new_bidding_strategy = response['value'][0]

  print ('Shared bidding strategy with name "%s" and ID "%s" of type "%s"'
         'was created.' %
         (new_bidding_strategy['name'], new_bidding_strategy['id'],
          new_bidding_strategy['biddingScheme']['BiddingScheme.Type']))

  return new_bidding_strategy

def main(req):
  # Initialize appropriate services.
  result = {}
  client = adwords.AdWordsClient.LoadFromStorage()
  client.client_customer_id = req['customer_id']

  campaign_service = client.GetService('CampaignService', version='v201809')
  budget_service = client.GetService('BudgetService', version='v201809')

  #bidding_strategy = CreateBiddingStrategy(client, req['bidding_strategy'],10)
  #bidding_strategy_id = bidding_strategy['id']

  # Create a budget, which can be shared by multiple campaigns.

  amount = str(10000 * req['budget'])

  budget = {
      'name': '%s budget' % uuid.uuid4(),
      'amount': {
          'microAmount': amount
      },
      'deliveryMethod': 'STANDARD'
  }

  budget_operations = [{
      'operator': 'ADD',
      'operand': budget
  }]

  # Add the budget.
  budget_id = budget_service.mutate(budget_operations)['value'][0]['budgetId']
  bidding_obj = {}
  if (req['bidding_strategy'] == "CPC"):
      bidding_obj = {'biddingStrategyType': 'MANUAL_CPC',}
      result['bidding_strategy_id'] = "CPC"
  elif (req['bidding_strategy'] == "CPM"):
      bidding_obj = {'biddingStrategyType': 'MANUAL_CPM',}
      result['bidding_strategy_id'] = "CPM"
  elif (req['bidding_strategy'] == "CPA"):
      bidding_strategy = CreateBiddingStrategy(client, req['bidding_strategy'],10)
      bidding_strategy_id = bidding_strategy['id']
      bidding_obj = {'biddingStrategyId': bidding_strategy_id}
      result['bidding_strategy_id'] = bidding_strategy_id




  operations = [{
      'operator': 'ADD',
      'operand': {
          'name': req['name'] + '/SEARCH' + '/' + req['celes_campaign_id'],
          # Recommendation: Set the campaign to PAUSED when creating it to
          # stop the ads from immediately serving. Set to ENABLED once you've
          # added targeting and the ads are ready to serve.
          'status': 'PAUSED',
          'advertisingChannelType': 'SEARCH',
          'biddingStrategyConfiguration': bidding_obj,
          'endDate': datetime.date(req['end_year'], req['end_month'], req['end_day']),
          # Note that only the budgetId is required
          'budget': {
              'budgetId': budget_id
          },
          'networkSetting': {
              'targetGoogleSearch': 'true',
              'targetSearchNetwork': 'true',
              'targetContentNetwork': 'false',
              'targetPartnerSearchNetwork': 'false'
          },
          # 'adServingOptimizationStatus': req['adServingOptimization'],
          # Optional fields
          'startDate': datetime.date(req['start_year'], req['start_month'], req['start_day']),
          'frequencyCap': {
              'impressions': '5',
              'timeUnit': 'DAY',
              'level': 'ADGROUP'
          },
          'settings': [
              {
                  'xsi_type': 'GeoTargetTypeSetting',
                  'positiveGeoTargetType': 'DONT_CARE',
                  'negativeGeoTargetType': 'DONT_CARE'
              }
          ]
      }
  }]

  operations.append({
      'operator': 'ADD',
      'operand': {
          'name': req['name'] + "/DISPLAY" +'/' + req['celes_campaign_id'],
          # Recommendation: Set the campaign to PAUSED when creating it to
          # stop the ads from immediately serving. Set to ENABLED once you've
          # added targeting and the ads are ready to serve.
          'status': 'PAUSED',
          'advertisingChannelType': 'DISPLAY',
          'biddingStrategyConfiguration': bidding_obj,
          'endDate': datetime.date(req['end_year'], req['end_month'], req['end_day']),
          # Note that only the budgetId is required
          'budget': {
              'budgetId': budget_id
          },
          'networkSetting': {
              'targetGoogleSearch': 'true',
              'targetSearchNetwork': 'true',
              'targetContentNetwork': 'false',
              'targetPartnerSearchNetwork': 'false'
          },
          # 'adServingOptimizationStatus': req['adServingOptimization'],
          # Optional fields
          'startDate': datetime.date(req['start_year'], req['start_month'], req['start_day']),
          'frequencyCap': {
              'impressions': '5',
              'timeUnit': 'DAY',
              'level': 'ADGROUP'
          },
          'settings': [
              {
                  'xsi_type': 'GeoTargetTypeSetting',
                  'positiveGeoTargetType': 'DONT_CARE',
                  'negativeGeoTargetType': 'DONT_CARE'
              }
          ]
      }
  })

  if (True):
      print("display campaign created")
      operations[1]['operand']['networkSetting']['targetGoogleSearch'] = 'false'
      operations[1]['operand']['networkSetting']['targetSearchNetwork'] = 'false'
      operations[1]['operand']['networkSetting']['targetContentNetwork'] = 'true'
  

  trackers = add_conversion_tracker.main(req)

  campaigns = campaign_service.mutate(operations)

  # Display results.
  location_id_list = location_track.main(req['locations'])

  for campaign in campaigns['value']:
    print ('Campaign with name "%s" and id "%s" was added.' % (campaign['name'], campaign['id']))
    if "/DISPLAY" in campaign['name']:
        result['display_campaign_id'] = campaign['id']
    else:
        
        result['campaign_id'] = campaign['id']
    if location_id_list is not None:
        add_location_criterion(location_id_list, campaign['id'], client)
  
  
  print(req['locations'][0])
  



  
  result['budget_id'] = budget_id
  result['trackers'] = trackers
 
 
  return result

def add_location_criterion(location_id_list, campaignId, client):
    campaign_criterion_service = client.GetService('CampaignCriterionService', version='v201809')
    criteria = []
    for _id in location_id_list:
        criteria.append({
            'xsi_type': 'Location',
            'id': _id
        })
    operations = []
    for criterion in criteria:
        operations.append({
            'operator': 'ADD',
            'operand': {
                'campaignId': campaignId,
                'criterion': criterion
            }
        })
    # Make the mutate request.
    if (len(operations) > 0):
        result = campaign_criterion_service.mutate(operations)

  # Display the resulting campaign criteria.
    # for campaign_criterion in result['value']:
    #     print ('Campaign criterion with campaign id "%s", criterion id "%s", '
    #         'and type "%s" was added.'
    #         % (campaign_criterion['campaignId'],
    #             campaign_criterion['criterion']['id'],
    #             campaign_criterion['criterion']['type']))