__author__ = 'www.yoelsher.com'

# Grab all data from xml
#import xml.etree.ElementTree as etree
from lxml import etree
import csv,re

inputFileName = 'funk120415.xml'
outputFileName = 'funk120415.txt'
dbFileName = 'funkierb_1C.csv'
brand = 'Funkier Bike'
sellerName = 'Funkier Bike USA'
websiteURL = 'https://www.funkierbikeusa.com'
uploadURL = websiteURL + '/wp-content/uploads/'


oFile = open(outputFileName,'w',newline='') 
feedWriter = csv.writer(oFile,delimiter='\t')
feedWriter.writerow(['id','title','brand','link','price','description','image_link'])
    
tree = etree.parse(inputFileName)

root = tree.getroot()

channel = root.find('channel')


# Prase items and save
counter = 1
for item in channel.findall('item'):
    counter = counter + 1
    # Check if Published, else skip
    status = item.find(etree.QName(item.nsmap['wp'],'status')).text
    if (status != 'publish'):
        continue
    

    # Get Title
    title = item.find('title').text
    title= re.sub('\u2019','\'',title)
    title = title.encode("ascii")
    
 
    # Get URL to Item
    link = item.find('link').text
    
    # Change to https if http
    link = re.sub('http://','https://',link)    
    
    # Get ID
    postID = item.find(etree.QName(item.nsmap['wp'],'post_id')).text
    
    # Get Description    
    description = item.find(etree.QName(item.nsmap['excerpt'] , 'encoded')).text.strip()
    
    # Remove HTML tags 
    description = re.sub('<[^<]+?>', '', description)   
    description = re.sub('\n','. ',description)
    description = re.sub('\t','',description)
    description = re.sub('\xa0','',description)
    description = re.sub('-','',description)
    description = re.sub('\u2022','',description)    
    description = description.strip().encode("ascii").decode("utf-8")
    

    # If description starts with ' ' remove it
    description = description.strip();
    
    if not (len(description)):
        description = 'No description available.';


    # Get Price
    for postmeta in item.findall(etree.QName(item.nsmap['wp'],'postmeta')):
        for metakey in postmeta.findall(etree.QName(item.nsmap['wp'],'meta_key')):
            if (metakey.text=='_price'):
                
                for element in postmeta.iter():
                    if (element.tag == etree.QName(item.nsmap['wp'],'meta_value')):
                        price = element.text
                        
    
    # Get Thumbnail ID
    for postmeta in item.findall(etree.QName(item.nsmap['wp'],'postmeta')):
        for metakey in postmeta.findall(etree.QName(item.nsmap['wp'],'meta_key')):
            if (metakey.text=='_thumbnail_id'): 
                
                for element in postmeta.iter():
                    if (element.tag == etree.QName(item.nsmap['wp'],'meta_value')):
                        imageIDs = element.text.split(',')


    # Generate image url
    imageURL = ''
    with open(dbFileName) as dbFile:
        
        r = csv.reader(dbFile, delimiter=";") 
        for row in r:
           # print(row[1])
            for imageID in imageIDs:
                if (row[1] == imageID) and (row[2]=='_wp_attached_file'):
                    imageURL = uploadURL + row[3] 
                    break
    
    
    
    # Generate the CSV
        
    feedWriter = csv.writer(oFile,delimiter='\t')

    # Make sure no duplicates
    postIDWithB = ' ('+postID+')'
    postIDWithB = postIDWithB.encode("utf8") 
    title = title + postIDWithB
    title = title.decode("utf-8")
    
    data = [postID,title,brand,link,price,description,imageURL]
    feedWriter.writerow(data)
        
                    
    

oFile.close()    
print('Done')