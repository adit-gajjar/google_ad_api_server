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

"""This example downloads a criteria performance report.

To get report fields, run get_report_fields.py.

The LoadFromStorage method is pulling credentials and properties from a
"googleads.yaml" file. By default, it looks for this file in your home
directory. For more information, see the "Caching authentication information"
section of our README.

"""


import sys
from googleads import adwords




results = {}
def main(req):
  client = adwords.AdWordsClient.LoadFromStorage()
  report_downloader = client.GetReportDownloader(version='v201809')
  client.client_customer_id = req['customer_id']
  report = {
      'reportName': 'Last 7 days CRITERIA_PERFORMANCE_REPORT',
      'dateRangeType': 'LAST_7_DAYS',
      'reportType': 'ADGROUP_PERFORMANCE_REPORT',
      'downloadFormat': 'CSV',
      'selector': {
          'fields': ['CampaignId', 'AdGroupId', 'Impressions', 'Clicks', 'Cost', 'CampaignName']
      }
  }
  f= open("report.txt","w+")

  # You can provide a file object to write the output to. For this demonstration
  # we use sys.stdout to write the report to the screen.
  report_downloader.DownloadReport(
      report, f, skip_report_header=False, skip_column_header=False,
      skip_report_summary=False, include_zero_impressions=True)

  f.close()
  f = open("report.txt", "r")
  data = f.readlines()
  i = 0
  for entry in data:
    if (i > 1):
        entry = entry.split(',')
        print(entry)
        if (not(entry[0] in results)): # check if campaign is already present.
            results[entry[0]] = {}
        add_report_entry(entry, results[entry[0]])
    i += 1
  return results




    
def add_report_entry(entry, campaign):
        campaign[entry[1]] = {
            'impressions': entry[2],
            'clicks': entry[3],
            'Cost': entry[4]
        }



