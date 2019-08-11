#!/usr/bin/env python
#
# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""This example adds a responsive display ad to an ad group.

Image assets are uploaded using AssetService. To get ad groups, run
get_ad_groups.py.

The LoadFromStorage method is pulling credentials and properties from a
"googleads.yaml" file. By default, it looks for this file in your home
directory. For more information, see the "Caching authentication information"
section of our README.

"""


from googleads import adwords
import requests



AD_GROUP_ID = 'INSERT_AD_GROUP_ID_HERE'


def UploadImageAsset(client, url):
  """Uploads the image from the specified url.

  Args:
    client: An AdWordsClient instance.
    url: The image URL.

  Returns:
    The ID of the uploaded image.
  """
  # Initialize appropriate service.
  asset_service = client.GetService('AssetService', version='v201809')

  # Download the image.
  image_request = requests.get(url)

  # Create the image asset.
  image_asset = {
      'xsi_type': 'ImageAsset',
      'imageData': image_request.content
      # This field is optional, and if provided should be unique.
      # 'assetName': 'Image asset ' + str(uuid.uuid4()),
  }
  
  # Create the operation.
  operation = {
      'operator': 'ADD',
      'operand': image_asset
  }

  # Create the asset and return the ID.
  result = asset_service.mutate([operation])
  
  print(result['value'][0]['assetId'])
  asset = result['value'][0]
  asset['fullSizeInfo']['imageUrl']
  return [result['value'][0]['assetId'],   asset['fullSizeInfo']['imageUrl']]


def main(req):
  # Initialize appropriate service.
  client = adwords.AdWordsClient.LoadFromStorage()
  client.client_customer_id = int(req['customer_id']) 
  ad_group_ad_service = client.GetService('AdGroupAdService', version='v201809')
  image = "http://0.0.0.0:3000/" + req['image']
  square_image = "http://0.0.0.0:3000/" + req['square_image']
  logo_image = "http://0.0.0.0:3000/" + req['logo_image']
  #landscape_image = "http://0.0.0.0:3000/" + req['landscape_image']
  main_image_id = UploadImageAsset(client, image)
  square_image_id = UploadImageAsset(client, square_image)
  logo_image_id = UploadImageAsset(client, logo_image)[0],
  #landscape_image_id = UploadImageAsset(client, landscape_image)
  print(main_image_id)
  print(square_image_id)
  print(logo_image_id)
  # Create the ad.
  multi_asset_responsive_display_ad = {
      'xsi_type': 'MultiAssetResponsiveDisplayAd',
      'headlines': [{
          'asset': {
              'xsi_type': 'TextAsset',
              'assetText': 'Travel to Mars'
          }
      }, {
          'asset': {
              'xsi_type': 'TextAsset',
              'assetText': 'Travel to Jupiter',
          }
      }, {
          'asset': {
              'xsi_type': 'TextAsset',
              'assetText': 'Travel to Pluto'
          }
      }],
      'descriptions': [{
          'asset': {
              'xsi_type': 'TextAsset',
              'assetText': 'Visit the planet in a luxury spaceship.',
          }
      }, {
          'asset': {
              'xsi_type': 'TextAsset',
              'assetText': 'See the planet in style.',
          }
      }],
      'businessName': 'Galactic Luxury Cruises',
      'longHeadline': {
          'asset': {
              'xsi_type': 'TextAsset',
              'assetText': 'Visit the planet in a luxury spaceship.',
          }
      },
      # This ad format does not allow the creation of an image asset by setting
      # the asset.imageData field. An image asset must first be created using
      # the AssetService, and asset.assetId must be populated when creating
      # the ad.
      'marketingImages': [{
          'asset': {
              'xsi_type': 'ImageAsset',
              'assetId': main_image_id[0]
          }
      }],
      'squareMarketingImages': [{
          'asset': {
              'xsi_type': 'ImageAsset',
              'assetId': square_image_id[0]
          }
      }],
      # Optional values
      'finalUrls': ['http://www.example.com'],
      'callToActionText': 'Shop Now',
      # Set color settings using hexadecimal values. Set allowFlexibleColor to
      # false if you want your ads to render by always using your colors
      # strictly.
      'mainColor': '#0000ff',
      'accentColor': '#ffff00',
      'allowFlexibleColor': False,
      'formatSetting': 'NON_NATIVE',
      # Set dynamic display ad settings, composed of landscape logo image,
      # promotion text, and price prefix.
      'dynamicSettingsPricePrefix': 'as low as',
      'dynamicSettingsPromoText': 'Free shipping!',
      'logoImages': [{
          'asset': {
              'xsi_type': 'ImageAsset',
              'assetId': logo_image_id[0]
          }
      }]
  }

  # Create ad group ad.
  ad_group_ad = {
      'adGroupId': req['ad_group_id'],
      'ad': multi_asset_responsive_display_ad,
      # Optional.
      'status': 'PAUSED'
  }

  # Add ad.
  ads = ad_group_ad_service.mutate([
      {'operator': 'ADD', 'operand': ad_group_ad}
  ])

  result = {}
  # Display results.
  if 'value' in ads:
    for ad in ads['value']:
        result['ad_id'] = ad['ad']['id']
        result['image_id'] = main_image_id[0]
        result['image_url'] = main_image_id[1]
  else:
    print('No ads were added.')
  return result
