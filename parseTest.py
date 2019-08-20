from yaml_utils import YAMLUtils
import lxml.etree as etree
from urllib.request import urlopen
import urllib
from io import StringIO
import requests
from lxml import html
import lxml.html as LH

banks = YAMLUtils.readYAML(YAMLUtils.FILE_NAME)

#page = requests.get('file:///C:/Users/waliak/Downloads/Interest%20Rates%20on%20Bank%20Accounts%20_%20Rates%20_%20CIBC.html')
with open(r'C:\Users\waliak\Desktop\Competitive Tracker\competitive-tracker_latest\Interest Rates on Bank Accounts _ Rates _ CIBC.html',"r",encoding="utf8") as f:
 page = f.read()
tree = html.fromstring(page)
context = etree.iterwalk(tree, events=("start", "end"))

for p in tree.xpath('//div[footer] | //div[@class="layoutcontainer base parbase" and contains(text(), "Interest")] | //div[@class="layoutcontainer base parbase"][2]'):
    p.getparent().remove(p)
    print(etree.tostring(p))

fetchData = tree.xpath('//div[@class="layoutcontainer base parbase"]')
print(len(fetchData))
print(fetchData)

#buyers = tree.xpath('//div[@class="layoutcontainer base parbase"]/text()')
bankCIBC = ([p.text_content() for p in tree.xpath('//div[@class="layoutcontainer base parbase"]')],)
#print(bankCIBC)
#([p.text_content()

#print(len(p))
#print (tree.xpath('//div[@class="layoutcontainer base parbase"]/text()', pretty_print=True, xml_declaration=True))

#print(tree, pretty_print=True, xml_declaration=True)
 # ])

#print(buyers)
#print([tr.text_content() for tr in tree.xpath('//tr')])
#bankCIBC = ([p.text_content() for p in tree.xpath("//strong[contains(text(),'CIBC')] | //b[contains(text(),'CIBC')] | //i[contains(text(),'CIBC')] | //*[contains(text(),'CIBC eAdvantage®')]")])
#print(len(bankCIBC))
#print((bankCIBC))
#bankCIBC1 = ([t.text_content() for t in tree.xpath("//*[contains(text(),'CIBC eAdvantage®')]")])
#print(len(bankCIBC1))
#joinCIBCAccount = bankCIBC + bankCIBC1
#print(joinCIBCAccount)

#if (len(bankCIBC))==5:
 #print("No account has been added in CIBC bank")
#elif (len(bankCIBC))<5:
 # print("Account has been removed from CIBC bank")
#else:
  #print("Account has been added in CIBC bank")

#str = etree.tostring(tree, pretty_print=True).decode("utf-8")
#print(str)
#str = ([tr.text_content() for tr in tree.xpath('//p')])
#print(etree.tostring(tree, pretty_print=True).decode("utf-8"))
#if "CIBC Bonus Savings Account" in str:
    #print('working')
#else:
    #print('Not working')


#for bank in banks:

 #for account in bank['accounts']:
#  if account['account_name'] in str:
#print("No changes has been made in"+ " "+ account["account_name"] +" "+bank["name"])
  #elif account['account_name'] is not str:
#print("Changes has been made"+ " "+ account["account_name"]+" "+bank["name"])