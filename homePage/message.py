from twilio.rest import TwilioRestClient
from twilio import TwilioRestException
from twilio.rest.lookups import TwilioLookupsClient
import requests
import httplib2
import urllib
from bs4 import BeautifulSoup
from dateutil.relativedelta import relativedelta
import re
import time
import logging

logging.basicConfig(filename="failedMessages.log",level=logging.WARNING)



class MessageApp:

    def __init__(self):
        self.msg = "My name is John"
        # self.auth_token = "9d7843b6b1b3ce23ab0ec4087e88804e"
        # self.sid = "AC3af5445dcb02235b6d4b3ac51c007038"
        # self.twilio_number = "+12052824000"

        self.sid = "ACd277855be797522d8b8a5441444ff3c4"
        self.auth_token = "74a9f5221f1296de26a78d8dfe2c4f21"
        self.twilio_number = "+12016451817 "
        self.client = TwilioRestClient(self.sid,self.auth_token)
        self.lookupClient = TwilioLookupsClient(self.sid,self.auth_token)
        self.smsStatus = 0
        self.validStatus= 0
        self.verifiedStatus = 0
        self.callStatus = 0
        self.validationCode = 0


    def is_verified(self,number):
        try:
            caller_ids = self.client.caller_ids.list(phone_number=number)
            if not caller_ids:
                self.verifiedStatus = 0
                return False

            self.verifiedStatus = 1
            return True

        except TwilioRestException as error:
            # something went wrong with the api
            self.verifiedStatus = -1
            return False

        except httplib2.ServerNotFoundError as serverError:
            self.verifiedStatus = -2
            return False



    def send_sms(self,number,message):

        try:
            msg = self.client.messages.create(
            body=message,
            from_=self.twilio_number,
            to=number
            )
            return True

        except TwilioRestException as error:
            return False

        except httplib2.ServerNotFoundError as serverError:
            return False
            # retry = 1
            # sent = False
            # msgId = ""
            # error_message = ""
            # error_code = ""
            # diff = relativedelta(end, start)
            # runtime = "The application has been running for %d year %d month %d days %d hours %d minutes %d seconds" % (diff.years, diff.months,
            # diff.days, diff.hours, diff.minutes,diff.seconds)
            # msg = "My name is John. " + runtime
            # while(retry <= 5 ):
            #     message = self.client.messages.create(
            #         body=msg,
            #         from_=self.twilio_number,
            #         to=to
            #     )
            #     msgId = message.sid + ".json"
            #     url = "https://api.twilio.com/2010-04-01/Accounts/" + self.sid + "/SMS/Messages/" + msgId
            #     time.sleep(10)
            #     try:
            #         response = requests.get(url,auth=(self.sid,self.auth_token))
            #         jsonObj = response.json()
            #
            #         if(jsonObj['status'] == "failed" or jsonObj['status'] == "undelivered"):
            #             self.smsStatus = jsonObj['status']
            #             error_message = "Message could not be delivered"
            #
            #             retry +=1
            #
            #         if(jsonObj['status']== "delivered" or jsonObj['status'] == "sent"):
            #             self.smsStatus = jsonObj['status']
            #             sent = True
            #             break;
            #
            #     except requests.exceptions.RequestException as error:
            #         # this  is bad because  we don't know the status of the message.
            #         error_message =  str(error)
            #         print "get failed"
            #         print error_message
            #         retry += 1

            #     except httplib2.ServerNotFoundError as serverError:
            #         print serverError
            #         error_message = "Server Not found"
            #         error_code = "404"
            #         break
            #
            #
            #
            # if(sent):
            #     return True

            # else:
            #     # log the failed message
            #     print "tried 5 times"
            #     logging.debug({"Message ID":"%s"%msgID,"Error Message":"%s"%error_message,"Error Code":"%s"%error_code})
            #     return False



        # except TwilioRestException as error:
        #     print error
        #     error_message = str(error)
        #     logging.debug({"Message ID":"","Error Message":"%s"%error_message,"Error Code":""})
        #     return False
        #
        # except httplib2.ServerNotFoundError as serverError:
        #     return False


    def validate(self,number):
        try:
            response = self.lookupClient.phone_numbers.get(number, include_carrier_info=True)
            response.phone_number  # If invalid, throws an exception.
            print "valid number"
            self.validStatus = 1
            return True

        except TwilioRestException as e:
            print "twilio exception"
            self.validStatus = 0
            return False

        except httplib2.ServerNotFoundError as serverError:
            self.validStatus = -1
            return False



    def verifyNewUser(self,number):

        try:
            caller_id = self.client.caller_ids.validate(number,status_callback="http://github.rishabh.ultrahook.com")
            print caller_id['validation_code']
            self.validationCode = caller_id['validation_code']
            print self.validationCode
            self.callStatus = 1
            return True

        except TwilioRestException as error:
            self.callStatus = 0
            return False

        except httplib2.ServerNotFoundError as serverError:
            self.callStatus = -1
            return False
