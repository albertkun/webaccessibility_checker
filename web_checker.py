import urllib, json, csv,time,requests
from lxml import html,etree
from collections import defaultdict

target_list = "2018_priority_list.csv"
output_json_file = target_list.split('.')[0]+".json"

the_data =[]
unique_link = []
count = 1

ignorelist = ["blog","programming-language","enterprise","open-source","fonts","bookmarking","social-sharing","wordpress-plugins","translation"]
        

def link_checker(item,keyword,target_array):
    if keyword in item and item not in target_array:
        # print item
        cleaned_item = item.replace("https://trends.builtwith.com"+keyword,"")
        if cleaned_item not in ignorelist and cleaned_item not in target_array:
            print cleaned_item
            target_array.append(cleaned_item)


def set_object(object_name,key,value):
    object_name.update({key:value})


def set_defaults(target_array,value):
    if len(target_array)==0:
        msg = value+" not found"
        target_array.append(msg)
        print msg


with open(target_list) as f:
    reader = csv.reader(f)
    for ucla_url in reader:
        # print ucla_url
        url_data = {}
        the_url = ucla_url[0]
        clean_url = the_url.replace(" ","")
        print "working on: "+clean_url
        print str(count)+" out of 82"
        complete_percent = round(float(count)/500 * 100,2)
        the_target = "https://builtwith.com/?"+clean_url
        # the_target = "http://builtwith.com/twins.ucla.edu"

        # print page.content
        frameworks =[]
        cms = []
        widgets = []
        webserver = []
        enfold = 0
        try:
            page = requests.get(the_target)
            tree = html.fromstring(page.content)       
            urls = tree.xpath('//a/@href')
            # print urls 
            for link in urls:
                link_checker(link,"/framework/",frameworks)
                link_checker(link,"/cms/",cms)
                link_checker(link,"/widgets/",widgets)
                link_checker(link,"/Web-Server/",webserver)
            
            if "Enfold" in frameworks:
                print "found ENFOLDDDDDwDDDDDDDDDD"
                set_object(url_data,"enfold",1)
                enfold = 1
                
            
                # print link
            # uni = [node.text_content() for node in subtree.xpath('//*[contains(text(), "Frameworks")')]
            # print uni
        except:
            print "Error occured on"+clean_url
        # print the_target
        # print "here are the frameworks"
        # if item 

        set_defaults(frameworks,"frameworks")
        set_defaults(cms,"cms")
        set_defaults(widgets,"widgets")
        set_defaults(webserver,"webserver")
        
        set_object(url_data,"frameworks",frameworks)
        set_object(url_data,"cms",cms)
        set_object(url_data,"widgets",widgets)
        set_object(url_data,"webserver",webserver)
        set_object(url_data,"enfold",enfold)
        set_object(url_data,"site_url",clean_url)
        # print frameworks
        # print cms
        # print widgets
        print url_data
        the_data.append(url_data)
        print "This much completed: "+str(complete_percent)+"%"
        count+=1
        time.sleep(10)

        if complete_percent >= 1:
            with open(output_json_file, 'w') as fp:
                json.dump(the_data, fp,sort_keys=True, indent=4)     

with open(output_json_file, 'w') as fp:
    json.dump(the_data, fp,sort_keys=True, indent=4)    
