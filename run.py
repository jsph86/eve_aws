import os
from eve import Eve
from flask import abort

def pre_POST_callback(resource, request):
    # retrieve mongodb collection using eve connection
    docs = app.data.driver.db['people']
    if docs.find_one({'firstname': 'joe'}):
        abort(422, description='Document is a duplicate and already in database.')

  
# AWS lambda, sensible DB connection settings are stored in environment variables.
MONGO_HOST= os.environ.get('MONGO_HOST')
MONGO_PORT = int(os.environ.get('MONGO_PORT'))
MONGO_USERNAME = os.environ.get('MONGO_USERNAME')
MONGO_PASSWORD = os.environ.get('MONGO_PASSWORD')
MONGO_DBNAME = os.environ.get('MONGO_DBNAME')
  
# AWS 
api_settings = {
      'MONGO_URI': MONGO_HOST,
      'MONGO_PORT': MONGO_PORT,
     # 'MONGO_USERNAME' : MONGO_USERNAME,
     # 'MONGO_PASSWORD' : MONGO_PASSWORD,
      'MONGO_DBNAME': MONGO_DBNAME,
      'RESOURCE_METHODS' : ['GET', 'POST', 'DELETE'],
      'ITEM_METHODS' : ['GET', 'PATCH', 'DELETE', 'PUT'],
      'EXTENDED_MEDIA_INFO' : ['content_type', 'name', 'length'],
      'RETURN_MEDIA_AS_BASE64_STRING' : False,
      'RETURN_MEDIA_AS_URL': True,
      'CACHE_CONTROL' : 'max-age=20',
      'CACHE_EXPIRES' : 20,
      'DOMAIN' : {'people': {
                  'item_title': 'person',
                  'additional_lookup':
                      {
                          'url': 'regex("[\w]+")',
                          'field': 'lastname'
                      },
                  'schema':
                      {
                          'firstname': {
                              'type': 'string',
                              'minlength': 1,
                              'maxlength': 10,
                          },
                          'lastname': {
                              'type': 'string',
                              'minlength': 1,
                              'maxlength': 15,
                              'required': True,
                              'unique': True,
                          },
                      }
                  }
              }
}
app = Eve(settings=api_settings)  
app.on_pre_POST += pre_POST_callback