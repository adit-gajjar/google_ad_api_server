# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""This example adds an ad group.

To get ad groups, run get_ad_groups.py.
"""

from __future__ import absolute_import

import argparse
import six
import sys
import uuid



from googleads import adwords

# enumeration constants #

# ages ranges
START_AGE_RANGE = 503001
UNDETERMINED_AGE = 503999

# gender
GENDER_MALE = 10
GENDER_FEMALE = 11
UNDETERMINED_GENDER = 20

# income
END_INCOME_RANGE = 510006

# parental status
START_PARENTAL_RANGE = 300

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

"""This example adds ad groups to a given campaign.

To get ad groups, run get_ad_groups.py.

The LoadFromStorage method is pulling credentials and properties from a
"googleads.yaml" file. By default, it looks for this file in your home
directory. For more information, see the "Caching authentication information"
section of our README.

"""




def CreateBiddingStrategy(client):
  """Creates a bidding strategy object.

  Args:
    client: AdWordsClient the client to run the example with.

  Returns:
    dict An object representing a bidding strategy.
  """
  # Initialize appropriate service.
  bidding_strategy_service = client.GetService(
      'BiddingStrategyService', version='v201809')

  # Create a shared bidding strategy.
  shared_bidding_strategy = {
      'name': 'Maximize Clicks %s' % uuid.uuid4(),
      'biddingScheme': {
          'xsi_type': 'TargetCpaBiddingScheme',
          # Optionally set additional bidding scheme parameters.
          
          'targetCpa': {
              'microAmount': '2000000'
          }
      }
  }

  # Create operation.
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
  # Initialize appropriate service.
  client = adwords.AdWordsClient.LoadFromStorage()
  client.client_customer_id = req['customer_id']
  ad_group_service = client.GetService('AdGroupService', version='v201809')
  ad_group_criterion_service = client.GetService('AdGroupCriterionService', version='v201809')

  # Construct operations and add ad groups.
  bidding_obj = {}
  if (req['bidding_strategy_id'] == "CPC"):
      bidding_obj = {'bids': [
                  {
                      'xsi_type': 'CpcBid',
                      'bid': {
                          'microAmount': '1000000'
                      },
                  }
              ]
              }

  elif (req['bidding_strategy_id'] == "CPM"):
     bidding_obj =  {'bids': [
                  {
                      'xsi_type': 'CpmBid',
                      'bid': {
                          'microAmount': '1000000'
                      },
                  }
              ]}

  else :
      bidding_obj = {'bids': [
                  {
                      'xsi_type': 'CpaBid',
                      'bid': {
                          'microAmount': '1000000'
                      },
                  }
              ]}

  operations = [{
      'operator': 'ADD',
      'operand': {
          'campaignId': req['campaign_id'],
          'name': 'Earth to Mars Cruises #%s' % uuid.uuid4(),
          'status': 'ENABLED',
          'biddingStrategyConfiguration': bidding_obj,
          'settings': [
              {
                  # Targeting restriction settings. Depending on the
                  # criterionTypeGroup value, most TargetingSettingDetail only
                  # affect Display campaigns. However, the
                  # USER_INTEREST_AND_LIST value works for RLSA campaigns -
                  # Search campaigns targeting using a remarketing list.
                  'xsi_type': 'TargetingSetting',
                  'details': [
                      # Restricting to serve ads that match your ad group
                      # placements. This is equivalent to choosing
                      # "Target and bid" in the UI.
                      {
                          'xsi_type': 'TargetingSettingDetail',
                          'criterionTypeGroup': 'PLACEMENT',
                          'targetAll': 'false',
                      },
                      # Using your ad group verticals only for bidding. This is
                      # equivalent to choosing "Bid only" in the UI.
                      {
                          'xsi_type': 'TargetingSettingDetail',
                          'criterionTypeGroup': 'VERTICAL',
                          'targetAll': 'true',
                      },
                  ]
              }
          ]
      }
  }]
  ad_groups = ad_group_service.mutate(operations)


  ad_group_id = ""
  # Display results.
  for ad_group in ad_groups['value']:
    print ('Ad group with name "%s" and id "%s" was added.'
           % (ad_group['name'], ad_group['id']))
    ad_group_id = ad_group['id']

  

  criteria_list = []

    # demographic criteria
  add_age_criteria(req['age'], criteria_list, ad_group_id)
  add_gender_criteria(req['gender'], criteria_list, ad_group_id)
  add_house_hold_income_criteria(req['house_hold_income'], criteria_list, ad_group_id)
    #add_parental_status_criteria(req['parental_status'], criteria_list, ad_group_id)

    # content targeting criteria
  add_keywords_criteria(req['keywords'], criteria_list, ad_group_id)

    #add_audience_criteria(req['audience'], criteria_list, ad_group_id)
    #add_topic_criteria(req['topics'], criteria_list, ad_group_id)
    #add_placement_criteria(req['placement'], criteria_list, ad_group_id)
  print(len(criteria_list))
  operations = []
  for criterion in criteria_list:
    operations.append({
        'operator': 'ADD',
        'operand': criterion
    })

  #response = ad_group_criterion_service.mutate(operations)
  ad_group_criterion_service.mutate(operations)['value']
  return {'ad_group_id': ad_group_id}


def add_age_criteria(age_data, criteria_list, ad_group_id):

    for i in range(6):
        if (age_data & 1) == 0:
            curr_criteria = {}
            curr_criteria['xsi_type'] = 'NegativeAdGroupCriterion'
            curr_criteria['adGroupId'] = ad_group_id
            curr_criteria['criterion'] = {
              'xsi_type': 'AgeRange',
              'id': START_AGE_RANGE + i
            }
            criteria_list.append(curr_criteria)
        age_data = age_data >> 1

    if (age_data & 1) == 0:
        curr_criteria = {}
        curr_criteria['xsi_type'] = 'NegativeAdGroupCriterion'
        curr_criteria['adGroupId'] = ad_group_id
        curr_criteria['criterion'] = {
              'xsi_type': 'AgeRange',
              'id': UNDETERMINED_AGE
    }

def add_gender_criteria(gender_data, criteria_list, ad_group_id):
    temp_id = GENDER_MALE
    for i in range(2):
        if (gender_data & 1) == 0:
            curr_criteria = {}
            curr_criteria['xsi_type'] = 'NegativeAdGroupCriterion'
            curr_criteria['adGroupId'] = ad_group_id
            curr_criteria['criterion'] = {
              'xsi_type': 'Gender',
              'id': temp_id
            }
            criteria_list.append(curr_criteria)
        temp_id += 1
        gender_data = gender_data >> 1

    if (gender_data & 1) == 0:
        curr_criteria = {}
        curr_criteria['xsi_type'] = 'NegativeAdGroupCriterion'
        curr_criteria['adGroupId'] = ad_group_id
        curr_criteria['criterion'] = {
              'xsi_type': 'Gender',
              'id': UNDETERMINED_GENDER
    }

def add_house_hold_income_criteria(house_hold_income_data, criteria_list, ad_group_id):
    for i in range(7):
        if (house_hold_income_data & 1) == 0:
            curr_criteria = {}
            curr_criteria['xsi_type'] = 'NegativeAdGroupCriterion'
            curr_criteria['adGroupId'] = ad_group_id
            curr_criteria['criterion'] = {
              'xsi_type': 'IncomeRange',
              'id': END_INCOME_RANGE - i
            }
            criteria_list.append(curr_criteria)
        house_hold_income_data = house_hold_income_data >> 1

def add_parental_status_criteria(parental_status_data, criteria_list, ad_group_id):
    for i in range(3):
        if (parental_status_data & 1) == 0:
            curr_criteria = {}
            curr_criteria['xsi_type'] = 'NegativeAdGroupCriterion'
            curr_criteria['adGroupId'] = ad_group_id
            curr_criteria['criterion'] = {
              'xsi_type': 'Parent',
              'id': START_PARENTAL_RANGE + i
            }
            criteria_list.append(curr_criteria)
        parental_status_data = parental_status_data >> 1

def add_keywords_criteria(keywords, criteria_list, ad_group_id):
    for keyword in keywords:
        curr_criteria = {
        'xsi_type': 'BiddableAdGroupCriterion',
        'adGroupId': ad_group_id,
        'criterion': {
            'xsi_type': 'Keyword',
            'matchType': 'EXACT',
            'text': keyword
            }
        }
        criteria_list.append(curr_criteria)


def add_topic_criteria(topics, criteria_list, ad_group_id):
    topics = topics.splitlines()
    for word in topics:
        curr_criteria = {
      'xsi_type': 'BiddableAdGroupCriterion',
      'adGroupId': ad_group_id,
      'criterion': {
          'xsi_type': 'Topic',
          'matchType': 'EXACT',
          'text': word
      }
    }
    criteria_list.append(curr_criteria)

def add_audience_criteria(audiences, criteria_list, ad_group_id):
    audiences = audiences.splitlines()
    for word in audiences:
        curr_criteria = {
      'xsi_type': 'BiddableAdGroupCriterion',
      'adGroupId': ad_group_id,
      'criterion': {
          'xsi_type': 'Audience',
          'matchType': 'EXACT',
          'text': word
      }
    }
    criteria_list.append(curr_criteria)