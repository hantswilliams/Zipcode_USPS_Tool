#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  1 20:40:58 2021

@author: hantswilliams + kojodanish 

Stonybrook 

Zipcode Verification Script 


"""





#### ORIGINAL SCRIPT TAKING FROM   https://smartystreets.com/articles/using-usps-apis-in-python



import urllib.request
import xml.etree.ElementTree as ET

import os
from dotenv import dotenv_values
import pandas as pd 



os.chdir('/Users/hantswilliams/Documents/development/python_projects/Zipcode_USPS_Tool/')
config = dotenv_values("./.env") 
usps_username = config["USERNAME"]
usps_password = config["PASSWORD"]



# LOAD ADDRESSES
fake_address_df = pd.read_csv('fake_addresses.csv', header='infer')


# FUNCTION TO HIT USPS API 

def usps_zip_finder(fakeindex, address, city, state):    
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
        
    output = {'fakeindex': fakeindex, 'address': var1, 'city' : var2, 'state': var3, 'zip_estimated':var4}
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
    
    del(df_row, df_index, df_address, df_city, df_state, output_temp2)




final = pd.concat(output_final)



final.to_csv('fake_addresses_output.csv', index=False)


















