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

import google.ads.google_ads.client

def main(req):
   
    client = (google.ads.google_ads.client.GoogleAdsClient.load_from_storage())
    customer_service = client.get_service('CustomerService', version='v1')
    customer = client.get_type('Customer', version='v1')
    today = datetime.today().strftime('%Y%m%d %H:%M:%S')
    customer.descriptive_name.value = ('Account created with '
                                       'CustomerService on %s' % today)
    # For a list of valid currency codes and time zones see this documentation:
    # https://developers.google.com/adwords/api/docs/appendix/codes-formats
    customer.currency_code.value = 'CAD'
    customer.time_zone.value = 'America/New_York'
    # The below values are optional. For more information about URL
    # options see: https://support.google.com/google-ads/answer/6305348
    customer.tracking_url_template.value = '{lpurl}?device={device}'
    customer.final_url_suffix.value = ('keyword={keyword}&matchtype={matchtype}'
                                       '&adgroupid={adgroupid}')
    customer.has_partners_badge.value = False

    try:
        response = customer_service.create_customer_client(
           req['manager_customer_id'] , customer)
        print(('Customer created with resource name "%s" under manager account '
               'with customer ID "%s"') %
               (response.resource_name, req['manager_customer_id']))
        result = {}
        result['customer_id'] = (response.resource_name)[10:]
        return result
    except google.ads.google_ads.errors.GoogleAdsException as ex:
        print('Request with ID "%s" failed with status "%s" and includes the '
              'following errors:' % (ex.request_id, ex.error.code().name))
        for error in ex.failure.errors:
            print('\tError with message "%s".' % error.message)
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print('\t\tOn field: %s' % field_path_element.field_name)
        sys.exit(1)















  
