from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import  pytz
import json
import logging
from django.core import serializers
from  message import MessageApp

logging.basicConfig(filename="failedMessages.log",level=logging.DEBUG)
msgapp = MessageApp()
# Create your views here.
VerificationStatus = ""

def index(request):
	return render(request,'homePage/home.html')


def checkValidity(request):
	number = request.GET['number']
	countryCode = request.GET["countryCode"]
	number = countryCode + number
	if(number.startswith("+") == False):
		number = "+" + number

	is_valid = msgapp.validate(number)


	if(is_valid):
		return JsonResponse({"status":1,"result":"Valid Number"})

	else:
		if(msgapp.validStatus == 0):
			return JsonResponse({"status":0,"result":"Invalid Number"})

		if(msgapp.validStatus == -1):
			return JsonResponse({"status":-1,"result": "Server Down"})


def is_verified(request):

	number = request.GET['number']
	countryCode = request.GET['countryCode']
	number = countryCode+number

	if(number.startswith("+") == False):
		number = "+" + number

	if(msgapp.is_verified(number)):

		return JsonResponse({"status":1,"result":"Already verified"})

	else:

		if(msgapp.verifiedStatus == 0):
			return JsonResponse({"status":0,"result":"Since you are not verified we will be making a call to veriy your number"})

		if(msgapp.verifiedStatus == -1):
			return JsonResponse({"status": -1,"result":"Try again.Something's wrong with the API.We could not check whether you were verified or not"})

		if(msgapp.verifiedStatus == -2):
			return JsonResponse({"status":-2, "result":"Try again.Server is down"})



def callUser(request):
	number = request.GET['number']
	countryCode = request.GET["countryCode"]
	number = countryCode + number

	if(number.startswith("+") == False):
		number = "+" + number

	callPlaced  = msgapp.verifyNewUser(number)
	if(callPlaced):

		return JsonResponse({"status":1,"result":msgapp.validationCode})
	else:
		if(msgapp.callStatus == 0):
			return JsonResponse({"status":0,"result":"Sorry We Couldn't call you,something went wrong with the api"})
		if(msgapp.callStatus ==  -1):
			return JsonResponse({"status":-1, "result":"Server Down. Please comeback later"})




def verificationCheck(request):
	number = request.GET['number']
	countryCode = request.GET['countryCode']
	number = countryCode+number
	if(number.startswith("+") == False):
		number = "+" + number

	if not VerificationStatus:
		return JsonResponse({"status":-1,"result":""})


	if(VerificationStatus == "success"):

		return JsonResponse({"status":1, "result": "Successfully verified"})

	return JsonResponse({"status":0,"result":"Try again. You did not get verfied"})

@csrf_exempt
def webHook(request):
	global VerificationStatus
	# print request.POST['VerificationStatus',None]
	VerificationStatus = request.POST['VerificationStatus']

	return JsonResponse({"status":VerificationStatus})



def sendSms(request):

	number = request.GET['number']
	cCode = request.GET['cCode']
	message = request.GET['message']
	number = cCode + number
	if(number.startswith("+") == False):
		number = "+" + number

	status = msgapp.send_sms(number,message)
	if(status):
		return JsonResponse({"result":"Sent"})

	return JsonResponse({"result":"Failed to send the message"})
