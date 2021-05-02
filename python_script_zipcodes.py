#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  1 20:40:58 2021

@author: hantswilliams + kojodanish 

Stonybrook 

Zipcode Verification Script 


1) Register unique ID from USPS: https://registration.shippingapis.com/ 

2) Webtool homepage documentation: https://www.usps.com/business/web-tools-apis/documentation-updates.htm

3) Address information: https://www.usps.com/business/web-tools-apis/address-information-api.pdf



https://smartystreets.com/articles/using-usps-apis-in-python



"""





#### ORIGINAL SCRIPT TAKING FROM   https://smartystreets.com/articles/using-usps-apis-in-python


import requests 
import pandas as pd 
import urllib.request
import xml.etree.ElementTree as ET
import os

from dotenv import dotenv_values


os.chdir('/Users/hantswilliams/Documents/development/python_projects/Zipcode_USPS_Tool/')
config = dotenv_values("./.env") 
usps_username = config["USERNAME"]
usps_password = config["PASSWORD"]



requestXML = """
<?xml version="1.0"?>
<AddressValidateRequest USERID=" """ + usps_username + """ ">
	<Revision>1</Revision>
	<Address ID="0">
		<Address1>2335 S State</Address1>
		<Address2>Suite 300</Address2>
		<City>Provo</City>
		<State>UT</State>
		<Zip5>84604</Zip5>
		<Zip4/>
	</Address>
</AddressValidateRequest>
"""

#prepare xml string doc for query string
docString = requestXML
docString = docString.replace('\n','').replace('\t','')
docString = urllib.parse.quote_plus(docString)

url = "http://production.shippingapis.com/ShippingAPI.dll?API=Verify&XML=" + docString
print(url + "\n\n")

response = urllib.request.urlopen(url)
if response.getcode() != 200:
	print("Error making HTTP call:")
	print(response.info())
	exit()
    
contents = response.read()
print(contents)

root = ET.fromstring(contents)
for address in root.findall('Address'):
	print()
	print("Address1: " + address.find("Address1").text)
	print("Address2: " + address.find("Address2").text)
	print("City:	 " + address.find("City").text)
	print("State:	" + address.find("State").text)
	print("Zip5:	 " + address.find("Zip5").text)












#### MODIFIED THE ORIGINAL SCRIPT TO REFLECT CHANGE TO API CALL TYPE 



requestXML = """
<?xml version="1.0"?>
<ZipCodeLookupRequest USERID=" """ + usps_username + """ ">
	<Revision>1</Revision>
	<Address ID="0">
		<Address1>952 rosewood ave</Address1>
		<Address2></Address2>
		<City>san carlos</City>
		<State>CA</State>
		<Zip5>unknown</Zip5>
		<Zip4/>
	</Address>
</ZipCodeLookupRequest>
"""

#prepare xml string doc for query string
docString = requestXML
docString = docString.replace('\n','').replace('\t','')
docString = urllib.parse.quote_plus(docString)

url = "http://production.shippingapis.com/ShippingAPI.dll?API=ZipCodeLookup&XML=" + docString
print(url + "\n\n")

response = urllib.request.urlopen(url)
if response.getcode() != 200:
	print("Error making HTTP call:")
	print(response.info())
	exit()
    
contents = response.read()
print(contents)


root = ET.fromstring(contents)
for address in root.findall('Address'):
	print()
# 	print("Address1: " + address.find("Address1").text)
	print("Address2: " + address.find("Address2").text)
	print("City:	 " + address.find("City").text)
	print("State:	" + address.find("State").text)
	print("Zip5:	 " + address.find("Zip5").text)














# load up some fake addresses 
fake_address_df = pd.read_csv('fake_addresses.csv', header='infer')


# Now create a function to take in each of the rows: 

def usps_zip_finder(fakeindex, address, city, state):
    
    #testing
    # address = '952 rosewood ave'
    # city = 'san carlos'
    # state = 'CA'
    
    requestXML = """
        <?xml version="1.0"?>
        <ZipCodeLookupRequest USERID=" """ + usps_username + """ ">
        	<Revision>1</Revision>
        	<Address ID="0">
        		<Address1>""" + address + """ </Address1>
        		<Address2></Address2>
        		<City>""" + city + """</City>
        		<State>""" + state + """</State>
        		<Zip5>unknown</Zip5>
        		<Zip4/>
        	</Address>
        </ZipCodeLookupRequest>
        """
    
    #prepare xml string doc for query string
    docString = requestXML
    docString = docString.replace('\n','').replace('\t','')
    docString = urllib.parse.quote_plus(docString)


    url = "http://production.shippingapis.com/ShippingAPI.dll?API=ZipCodeLookup&XML=" + docString
    print(url + "\n\n")
    
    response = urllib.request.urlopen(url)
    if response.getcode() != 200:
    	print("Error making HTTP call:")
    	print(response.info())
    	exit()
        
    contents = response.read()
    print(contents)
    
    
    root = ET.fromstring(contents)
    
    
    for address in root.findall('Address'):
        var1 = address.find("Address2").text
        var2 = address.find("City").text
        var3 = address.find("State").text
        var4 = address.find("Zip5").text
        
    output = {'fakeindex': fakeindex, 'address': var1, 'city' : var2, 'state': var3, 'zip':var4}
    output = pd.DataFrame(data=output, index=[0])
        
    return output
        
        



output_final = []

for i in range(len(fake_address_df)):
    
    df_row = fake_address_df.iloc[i]
    df_index = df_row.index_fake
    df_address = df_row.address_1
    df_city = df_row.city
    df_state = df_row.state 
        
    output_temp2 = usps_zip_finder(df_index, df_address, df_city, df_state)
    output_final.append(output_temp2)


final = pd.concat(output_final)





















# https://github.com/Brobin/usps-api/

from usps import USPSApi, Address

address = Address(
    name='hants williams',
    address_1='952 rosewood ave',
    city='san carlos',
    state='ca',
    zipcode='94070'
)

usps = USPSApi(usps_username, test=True)
validation = usps.validate_address(address)
print(validation.result)











