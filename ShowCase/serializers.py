from rest_framework import serializers

class HyperlinkedImageField(serializers.ImageField):
    '''
    Customizing image field to return complete url.
    '''
    def __init__(self,default_url, *args, **kwargs):
	self.default_url = default_url
	super(HyperlinkedImageField, self).__init__(*args, **kwargs)
    
    def to_native(self, value):
	request = self.context.get('request', None)
	try :
	    print value.url
	    return request.build_absolute_uri(value.url)
	except ValueError:
	    if self.default_url:
	        return request.build_absolute_uri(self.default_url) 
	    else:
		raise Exception('HyperlinkedImageField: Default url invalid')

class HyperlinkedFileField(serializers.FileField):
    '''
    Customizing image field to return complete url.
    '''
    def __init__(self,default_url, *args, **kwargs):
	self.default_url = default_url
	super(HyperlinkedFileField, self).__init__(*args, **kwargs)
    
    def to_native(self, value):
	request = self.context.get('request', None)
	try :
	    print value.url
	    return request.build_absolute_uri(value.url)
	except ValueError:
	    if self.default_url:
	        return request.build_absolute_uri(self.default_url)
	    else:
		raise Exception('HyperlinkedFileField: Default url invalid.')
