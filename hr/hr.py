import traceback
import json
#from auth import Authentication
from log import getLogger
import requests

logger = getLogger('hr', 'logs/hr')

headers = {
    'Content-type': 'application/json',
    'Accept': 'application/json'}


class Hr:
    #@Authentication.token_required
    def requet_token(self):
        data = self
        logger.info("Request : %s" % data)
        try:
            createresponse = requests.post('https://ebsmobileapp.slt.com.lk/API/v1/employee/login',
                                           data=json.dumps(data),
                                           headers=headers)

            logger.info("Response Code: %s" % createresponse.status_code)
            # resmsg = json.loads(createresponse.text)
            # responsedata = {"message": resmsg['Message']}
            # logger.info("Response : %s" % responsedata)
            # return responsedata
            resmsg = createresponse.json()
            responsedata = {"token": resmsg['authtoken'], "person id": resmsg['person_id']}
            logger.info("Response : %s" % resmsg)
            return responsedata
        except Exception as e:
            print("Exception : %s" % traceback.format_exc())
            logger.info("Exception : %s" % traceback.format_exc())

    #@Authentication.token_required
    def requet_leave(self):
        data = self
        logger.info("Request : %s" % data)
        try:

            headers = {
                'username': '012583',
                'personid': str(data['personid']),
                'Authorization': 'Bearer ' + str(data['authtoken'])
            }

            createresponse = requests.get('https://ebsmobileapp.slt.com.lk/API/v1/employee/leavebalance',
                                          headers=headers)

            logger.info("Response Code: %s" % createresponse.status_code)
            resmsg = createresponse.json()
            responsedata = {"data": resmsg['data']}
            logger.info("Response : %s" % resmsg)

            print(type(resmsg['data']))
            for data in resmsg['data']:
                print(data)
                print('Leave_Plan :'+data['Leave_Plan'])
                print('Entitlement :'+str(data['Entitlement']))
                print('Current_Balance :'+str(data['Current_Balance']))
                print('No_Pay :'+str(data['No_Pay']))



            return responsedata
        except Exception as e:
            print("Exception : %s" % traceback.format_exc())
            logger.info("Exception : %s" % traceback.format_exc())
