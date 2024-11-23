import traceback

from auth import Authentication
from log import getLogger
import xml.etree.ElementTree as ET
import requests
import random
import string

logger = getLogger('etpos', 'logs/etpos')

userid, locationid, storeid = '', '', ''
url = "https://vendorapi.etpos.lk/soap/merchant/server"
headers = {
    'Content-Type': 'application/xml'
}


def specific_string(length):
    sample_string = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'  # define the specific string
    # define the condition for random string
    return ''.join((random.choice(sample_string)) for x in range(length))


class Etpos:
    #@Authentication.token_required
    def register_merchant(self, auth):
        authres= Authentication.login(auth)
        if authres == 'success':
            ref = specific_string(15)
            data = self
            print(data['category']['category_1'])
            logger.info("Request : %s" % ref + " - " + str(data))
            xmlfile = open('etpos/files/register.xml', 'r')
            body = xmlfile.read()

            # POST request
            try:
                response = requests.request("POST", url, headers=headers,
                                            data=body.format(name=data['name'], email=data['email'], company=data['email'],
                                                             telephone=int(data['telephone']),
                                                             mobile=data['mobile'], username=data['username'],
                                                             password=data['password'],
                                                             confirmedPassword=data['confirmedPassword'],
                                                             registrantName=data['registrantName'],
                                                             registrantRelation=data['registrantRelation'],
                                                             registrantMobile=data['registrantMobile'],
                                                             id=data['id'], address=data['address'],
                                                             no_of_stores=data['no_of_stores'],
                                                             plan=data['plan']))

                # prints the response
                print(response.text)
                logger.info("Response User : %s" % ref + " - " + response.text)

                root = ET.fromstring(response.content)
                for child in root.iter('ok'):
                    outCode = child.text
                    for child in root.iter('verificationCode'):
                        verificationCode = child.text
                        print("verificationCode " + verificationCode)

                    print(outCode)
                    if outCode == "true":
                        for child in root.iter('userId'):
                            userid = child.text
                            print('userId ' + userid)

                            xmlfiletype = open('etpos/files/type.xml', 'r')
                            bodytype = xmlfiletype.read()

                            responsetype = requests.request("POST", url, headers=headers,
                                                            data=bodytype.format(type=data['locationtype'], userid=userid))

                            print(responsetype.text)
                            logger.info("Response Location : %s" % ref + " - " + responsetype.text)

                            roottype = ET.fromstring(responsetype.content)

                            for child in roottype.iter('ok'):
                                outCodetype = child.text
                                for child in roottype.iter('id'):
                                    locationid = child.text
                                    print('id ' + locationid)

                                print(outCodetype)
                                if outCodetype == "true":
                                    xmlfilestore = open('etpos/files/store.xml', 'r')
                                    bodystore = xmlfilestore.read()

                                    responsestore = requests.request("POST", url, headers=headers,
                                                                     data=bodystore.format(name=data['storename'],
                                                                                           contactno=data['storemobile'],
                                                                                           email=data['storeemail'],
                                                                                           fax=data['fax'],
                                                                                           locationType=locationid,
                                                                                           userid=userid,
                                                                                           category1=data['category']['category_1'],
                                                                                           category2=data['category']['category_2'],
                                                                                           addressLine1=data['addressLine1'],
                                                                                           city=data['city'],
                                                                                           country=data['country'],
                                                                                           addressLine2=data['addressLine2'],
                                                                                           state=data['state'],
                                                                                           postalCode=data['postalCode']))

                                    print(responsestore.text)
                                    logger.info("Response Store : %s" % ref + " - " + responsestore.text)

                                    rootstore = ET.fromstring(responsestore.content)

                                    for child in rootstore.iter('ok'):
                                        outCodestore = child.text
                                        for child in rootstore.iter('locationId'):
                                            storeid = child.text
                                            print('locationId ' + storeid)

                                        print(outCodetype)
                                        if outCodestore == "true":
                                            responsedata = {"userid": userid, "verificationCode": verificationCode,
                                                            "locationid": locationid, "storeid": storeid}
                                            return responsedata

                                    else:
                                        for child in rootstore.iter('faultstring'):
                                            print('faultstring ' + child.text)
                                            logger.info("faultstring : %s" % ref + " - " + child.text)

                                            responsedata = {"message": child.text}
                                            return responsedata

                            else:
                                for child in roottype.iter('faultstring'):
                                    print('faultstring ' + child.text)
                                    logger.info("faultstring : %s" % ref + " - " + child.text)

                                    responsedata = {"message": child.text}
                                    return responsedata

                else:
                    for child in root.iter('faultstring'):
                        print('faultstring ' + child.text)
                        logger.info("faultstring : %s" % ref + " - " + child.text)

                        responsedata = {"message": child.text}
                        return responsedata
            except Exception as e:
                print("Exception : %s" % traceback.format_exc())
                logger.info("Exception : %s" % traceback.format_exc())
                responsedata = {"message": e}
                return responsedata
        else:
            responsedata = {"message": authres}
            return responsedata

    #@Authentication.token_required
    def create_store(self,auth):
        authres= Authentication.login(auth)
        if authres == 'success':
            ref = specific_string(15)
            data = self
            logger.info("Request : %s" % ref + " - " + str(data))

            xmlfiletype = open('etpos/files/type.xml', 'r')
            bodytype = xmlfiletype.read()

            try:
                responsetype = requests.request("POST", url, headers=headers,
                                                data=bodytype.format(type=data['locationtype'], userid=data['userid']))

                print(responsetype.text)
                logger.info("Response Location : %s" % ref + " - " + responsetype.text)

                roottype = ET.fromstring(responsetype.content)

                for child in roottype.iter('ok'):
                    outCodetype = child.text
                    for child in roottype.iter('id'):
                        locationid = child.text
                        print('id ' + locationid)

                    print(outCodetype)
                    if outCodetype == "true":
                        xmlfilestore = open('etpos/files/store.xml', 'r')
                        bodystore = xmlfilestore.read()

                        responsestore = requests.request("POST", url, headers=headers,
                                                         data=bodystore.format(name=data['storename'],
                                                                               contactno=data['storemobile'],
                                                                               email=data['storeemail'],
                                                                               fax=data['fax'],
                                                                               locationType=locationid,
                                                                               userid=data['userid'],
                                                                               category1=data['category']['category_1'],
                                                                               category2=data['category']['category_2'],
                                                                               addressLine1=data['addressLine1'],
                                                                               city=data['city'],
                                                                               country=data['country'],
                                                                               addressLine2=data['addressLine2'],
                                                                               state=data['state'],
                                                                               postalCode=data['postalCode']))

                        print(responsestore.text)
                        logger.info("Response Store : %s" % ref + " - " + responsestore.text)

                        rootstore = ET.fromstring(responsestore.content)

                        for child in rootstore.iter('ok'):
                            outCodestore = child.text
                            for child in rootstore.iter('locationId'):
                                storeid = child.text
                                print('locationId ' + storeid)

                            print(outCodetype)
                            if outCodestore == "true":
                                responsedata = {"userid": data['userid'], "locationid": locationid, "storeid": storeid}
                                return responsedata

                        else:
                            for child in rootstore.iter('faultstring'):
                                print('faultstring ' + child.text)
                                logger.info("faultstring : %s" % ref + " - " + child.text)

                                responsedata = {"message": child.text}
                                return responsedata

                else:
                    for child in roottype.iter('faultstring'):
                        print('faultstring ' + child.text)
                        logger.info("faultstring : %s" % ref + " - " + child.text)

                        responsedata = {"message": child.text}
                        return responsedata
            except Exception as e:
                print("Exception : %s" % traceback.format_exc())
                logger.info("Exception : %s" % traceback.format_exc())
                responsedata = {"message": e}
                return responsedata
        else:
            responsedata = {"message": authres}
            return responsedata
