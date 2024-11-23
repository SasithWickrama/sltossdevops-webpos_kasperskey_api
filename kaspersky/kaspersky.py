import random
import sys
import traceback

from log import getLogger
from cryptography.hazmat.primitives.serialization import pkcs12
from cryptography.hazmat.primitives import serialization
from auth import Authentication
import json
import requests

logger = getLogger('kasperskyapi', 'logs/kaspersky')

with open("kaspersky/files/c412341de164496c869b1ee1beb51bc099bb1940f6a44fcb8c44f2b32cec6e77.pfx", "rb") as f:
    private_key, certificate, additional_certificates = pkcs12.load_key_and_certificates(f.read(), b"89)iopJKL")

    key = open("kaspersky/files/key.pem", 'wb')
    cert = open("kaspersky/files/cert.pem", 'wb')
    key.write(
        private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        )
    )
    key.flush()
    cert.write(
        certificate.public_bytes(serialization.Encoding.PEM),
    )
    cert.flush()

headers = {
    'Content-type': 'application/json',
    'Accept': 'application/json'}

cert = ("kaspersky/files/cert.pem", "kaspersky/files/key.pem")


def specific_string(length):
    sample_string = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'  # define the specific string
    # define the condition for random string
    return ''.join((random.choice(sample_string)) for x in range(length))


class Kaspersky:

    # @Authentication.token_required
    def create_sub(self, auth):
        authres = Authentication.login(auth)
        if authres == 'success':
            ref = specific_string(15)
            data = self
            logger.info("Request : %s" % ref + " - " + str(data))
            try:
                createresponse = requests.post(
                    'https://api.demo.korm.kaspersky.com/Subscriptions/v2.0/api/Subscription/create',
                    #cert=cert,
                    data=json.dumps(data),
                    headers=headers)
                # print(createresponse.text)
                # print(createresponse.status_code)
                resmsg = json.loads(createresponse.text)
                if createresponse.status_code == 200:
                    logger.info("Response : %s" % ref + " - " + str(resmsg))
                    return resmsg
                else:
                    logger.info("Response : %s" % ref + " - " + str(resmsg))
                    return resmsg
            except Exception as e:
                # print("Exception : %s" % traceback.format_exc())
                logger.info("Exception : %s" % ref + " - " + traceback.format_exc())
                responsedata = {"ErrorId": ref,
                                "Message": str(e.args[0]),
                                "ErrorCode": str(e.msg)}
                return responsedata
        else:
            responsedata = {"message": authres}
            return responsedata

    # @Authentication.token_required
    def modify_sub(self, auth):
        authres = Authentication.login(auth)
        if authres == 'success':
            ref = specific_string(15)
            data = self
            logger.info("Request : %s" % ref + " - " + str(data))
            try:
                modifyresponse = requests.post(
                    'https://api.demo.korm.kaspersky.com/Subscriptions/v2.0/api/Subscription/modifyexpiration',
                    cert=cert,
                    data=json.dumps(data),
                    headers=headers)

                if modifyresponse.status_code == 200:
                    resmsg = {"message": "success"}
                    logger.info("Response : %s" % ref + " - " + str(resmsg))
                    return resmsg
                else:
                    resmsg = json.loads(modifyresponse.text)
                    logger.info("Response : %s" % ref + " - " + str(resmsg))
                    return resmsg
            except Exception as e:
                # print("Exception : %s" % traceback.format_exc())
                logger.info("Exception : %s" % ref + " - " + traceback.format_exc())
                responsedata = {"ErrorId": ref,
                                "Message": str(e.args[0]),
                                "ErrorCode": str(e.msg)}
                return responsedata
        else:
            responsedata = {"message": authres}
            return responsedata

    # @Authentication.token_required
    def remove_sub(self, auth):
        authres = Authentication.login(auth)
        if authres == 'success':
            ref = specific_string(15)
            data = self
            # app.logger.info("Request :" +str(data))
            logger.info("Request : %s" % ref + " - " + str(data))
            try:
                removeresponse = requests.post(
                    'https://api.demo.korm.kaspersky.com/Subscriptions/v2.0/api/Subscription/hardcancel',
                    cert=cert,
                    data=json.dumps(data),
                    headers=headers)

                if removeresponse.status_code == 200:
                    resmsg = {"message": "success"}
                    logger.info("Response : %s" % ref + " - " + str(resmsg))
                    return resmsg
                else:
                    resmsg = json.loads(removeresponse.text)
                    logger.info("Response : %s" % ref + " - " + str(resmsg))
                    return resmsg
            except Exception as e:
                print("Exception : %s" % traceback.format_exc())
                logger.info("Exception : %s" % ref + " - " + traceback.format_exc())
                responsedata = {"ErrorId": ref,
                                "Message": str(e.args[0]),
                                "ErrorCode": str(e.msg)}
                return responsedata
        else:
            responsedata = {"message": authres}
            return responsedata
