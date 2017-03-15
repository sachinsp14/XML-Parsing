
#Format: python xmlParsing.py [--gunzip/gzip] [file-path]

import sys,zlib,base64,requests
import xml.sax.saxutils as saxutils
import xml.etree.ElementTree as ET

try:
    
    file = sys.argv[2]    
    tree = ET.parse(file)    
    root = tree.getroot()

    #Zipping the xml content
    if sys.argv[1]=="--gzip":    
        for elements in root.findall(".//*[@test='1']"):                    
            elementstring = ET.tostring(elements).split('>', 1)[1].rsplit('<', 1)[0]            
            elementstring=base64.b64encode(zlib.compress(elementstring))            
            for child in list(elements):
                elements.remove(child)            
            elements.text=elementstring            
            f=open(file,"w")
            tree.write(f)
            f.close()
            
    #Unzipping the zipped content
    elif sys.argv[1]=="--gunzip":
        for elements in root.findall(".//*[@test='1']"):            
            elementstring=zlib.decompress(base64.b64decode(elements.text))            
            elements.text=elementstring            
            f=open(file,"w")
            f.write(saxutils.unescape(ET.tostring(root)))
            f.close()
    else:
         raise NameError
        
    #Bonus:Sending post request to the server
    
    tree = ET.parse(file)
    xml=ET.tostring(tree.getroot())
    print("sending request to http://posttestserver.com/post.php")
    print (requests.post('http://posttestserver.com/post.php', data=xml, headers={'Content-Type': 'application/xml'}).text)

except NameError:
    print("Unknown Command")
    print("Format: python xmlParsing.py [--gunzip/gzip] [file-path]")       
