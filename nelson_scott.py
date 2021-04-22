#!/usr/bin/env python
# coding: utf-8

# Make a small program that makes a GET request to the specified URL,
# parses the response, and creates a certificate chain using the certs
# supplied from the API response. You may use any programming style
# that are comfortable with; the program may use classes and methods
# (OOP) or it may use regular functions.
# 
# 
# 
# 1. The program should make an API call to the following URL:
# 
# (GET request)
# 
# http://test-api-app-apptest.k-apps.osh.massopen.cloud/api/v1/get-example-certificates
# 
# When making the request, ensure the following username:password is
# base64 encoded and then included within the Basic Authentication
# header of your GET request:
# 
# testuser:T3st9paS$w0rd!
# 
# Note: It's okay to hardcode those credentials in your script as this is
# just for example only.
# 
# 
# 
# 
# 2. The response from the API call in the above step should return
# valid JSON containing three dummy certificates that were generated
# and self-signed with openssl. Each certificate is returned as a
# fairly long string inside of a list. The list is contained within a
# dictionary at the key named 'Certificates' as shown:
# 
# {
#     "Certificates": [
#         "MIIDYjCCAkoCCQD12xSERbXFI... (omitted for brevity)",
#         "MIIDkDCCAngCCQDb0/k1Oex1O... (omitted for brevity)",
#         "MIIDYDCCAkgCCQDOPnykxHJNO... (omitted for brevity)"
#     ]
# }
# 
#  Your job is to parse and properly format the text for each of the
#  three certificates found in the API response.
# 
# 
# 
# 
# 3. Your code should ultimately produce a certificate chain within a
# plain-text file in the same working directory as your script. The
# file should be IDENTICAL to the included file:
# 
# example_cert_chain.crt
# 
# 
#  Assume that each certificate will need to begin with the text:
#  
#  -----BEGIN CERTIFICATE-----
#  
#  Assume that each certificate should also end with the text:
#  
#  -----END CERTIFICATE-----
# 
# 
# Check the attached example_cert_chain.crt for an example.
# 
# 
# With the exception of the -----BEGIN CERTIFICATE----- and the
# corresponding -----END CERTIFICATE----- parts, each line of text
# should be 64 characters long plus a newline (total 65 chars). The
# LAST line of each certificate may be up to 64 characters or less
# (usually less). This will require you to create an algorithm that
# creates/formats each certificate properly. Three certificates were
# given to you in the API response, but your code should work for
# one:many certificates.
# 
# 
# 
# 
# 4. Finally, using your personal Github account (if you do not
# have one you will have to create a free account), create a repository
# using this naming convention:
# 
# ssc_test_application
# 
# Then create a branch named Develop (taken off of your main/master
# branch).
# 
# Then create a 2nd branch. This branch should be take off of the
# newly created Develop branch. Use your first name concatenated with
# 'feature_branch' using underscores when creating/naming the branch:
# 
# firstname_feature_branch
# 
# 
# Add, commit, and push your solution to the above problem into
# this feature branch.
# 
# Then merge the feature branch into the Develop branch. Finally,
# merge the Develop branch into the main (or master) branch.
# 
# Please email the link to jcolley1@statestreet.com and be sure
# to CC Ata Turk at aturk@statestreet.com
# 
# 
# 
# 
# 5. Other Stipulations:
# 
# Your code must pass a pycodestyle validation. No warnings should be
# present in the output. Use the below command to check your script:
# 
# pycodestyle </path/to/program_name.py>
# 
# Only the Python3 standard-library packages may be used and imported
# into your script: No third-party libs should be imported into the
# program (the requests library MAY NOT be used -> use Python3's
# built-in urllib.request instead).
# 
# Use comments and/or Google-Style docstrings to explain what is
# happening in your code.
# 
# Use your last and first names as the program name separated with
# an underscore:  last_first.py
# 
# Ensure the name of the certificate chain that is created by your
# script uses your last and first name: last_first.crt
# 
# 
# 
# 
# Thanks,
# 
# James
# 

# In[117]:


import urllib.request as urllibr
import base64

def formatCerts(user, password, url):
    """ function to retrieve the certifactes from the url using
    the username and password provided to the function. Then format 
    the retrieved certificates into a .txt file
    
    Args: 
        user (str): the string user name used for authentication
        password (str): string representing the password for authentication
        url (str): string representing the url to retrieve the data from
        
    Returns:
    """

    #encodes the user name and pass for the auth
    userpass = base64.b64encode(bytes('%s:%s' % (user, password), 'ascii'))

    #makes the header for the request
    headers = { 'Authorization' : 'Basic %s' %  userpass.decode('utf-8')}

    #makes the request object using url and header
    r = urllibr.Request(url, headers=headers)

    #gets the meta data using the request obj
    with urllibr.urlopen(r) as response:
        certs = response.read()

    #cleans the response data
    certs = certs.decode('utf-8')[18:].split(',')
    certs[0] = certs[0][:-1]
    certs[1] = certs[1][1:-1]
    certs[2] = certs[2][1:-4]

    #set variable to control the format of the output
    outfile = open('nelson_scott.crt','w')  
    cnt = 0

    #loop through all recieved certifcates
    for cert in certs:
        #append start of cert
        outfile.write('----Begin Certificate---- \n')
        #loop through cert ensuring line does exceed 64 chars
        while len(cert) > 0:
            if(len(cert) == 1):
                #outfile write character of the cert and new line for end of curr cert
                outfile.write(cert[0])
                outfile.write(' \n')
                cert = cert[1:]
                
                #reset counter
                cnt = 0
            elif(cnt < 63):
                #outfile write character of the certificate
                outfile.write(cert[0])
                cert = cert[1:]
                
                #increment the counter
                cnt += 1
            else:
                #outfile write character of the certificate and new line
                outfile.write(cert[0])
                outfile.write('\n')
                cert = cert[1:]
                
                #reset the counter
                cnt = 0
                
        #append end of cert to outfile
        outfile.write('----End Certificate----')
        outfile.write(' \n')

    #close the outfile
    outfile.close()
        
#establish the user name and password to acess data
user = 'testuser'
password = 'T3st9paS$w0rd!'

#establish url to retrieve the data from
url = 'http://test-api-app-apptest.k-apps.osh.massopen.cloud/api/v1/get-example-certificates'

#call the function using our params we just set
formatCerts(user, password, url)

