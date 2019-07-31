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
"""This example illustrates how to create a new customer under a given
manager account.

Note: this example must be run using the credentials of a Google Ads manager
account. By default, the new account will only be accessible via the manager
account.
"""
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

"""This example illustrates how to create an account.

Note by default this account will only be accessible via its parent AdWords
manager account..

The LoadFromStorage method is pulling credentials and properties from a
"googleads.yaml" file. By default, it looks for this file in your home
directory. For more information, see the "Caching authentication information"
section of our README.

"""


from datetime import datetime
from googleads import adwords


def main(req):
  # Initialize appropriate service.
  adwords_client = adwords.AdWordsClient.LoadFromStorage()
  managed_customer_service = client.GetService(
      'ManagedCustomerService', version='v201809')

  today = datetime.today().strftime('%Y%m%d %H:%M:%S')
  # Construct operations and add campaign.
  operations = [{
      'operator': 'ADD',
      'operand': {
          'name': req['account_name'],
          'currencyCode': req['currency_code'],
          'dateTimeZone': req['time_zone'],
      }
  }]

  # Create the account. It is possible to create multiple accounts with one
  # request by sending an array of operations.
  accounts = managed_customer_service.mutate(operations)

  # Display results.
  for account in accounts['value']:
    print ('Account with customer ID "%s" was successfully created.'
           % account['customerId'])
  return account['customerId']
