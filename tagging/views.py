from .models import Tag

# Create your views here.

def tag_exists(tagname):
    try:
        tag = Tag.objects.get(tag_name=tagname)
    except Tag.DoesNotExist:
        tag = None
    retval = 0 if (tag==None) else 1
    return retval
        

def get_tag(tagname):
    #Assumes tag exists
    return Tag.objects.get(tag_name=tagname)

    
def taglist_exists(tag_list):
    for tag in tag_list:
        if(tag_exists(tag)==0):
            return 0
    return 1    

