from __future__ import absolute_import, division, unicode_literals
from rasa_sdk import Action
from rasa_sdk.events import SlotSet, FollowupAction, AllSlotsReset, Restarted, Form

import logging
import re
import json
import pymongo
import datetime
from random import randint
from rasa_sdk.forms import FormAction, REQUESTED_SLOT
from twilio.rest import Client
from pymongo import MongoClient

logger = logging.getLogger(__name__)

class ActionGreet(Action):

    def name(self):
        uniqId = randint(1, 1000000)
        return "action_greet"

    def run(self, dispatcher, tracker, domain):
        gt = {
            "attachment": {
                "type": "carousel",
                "payload": {
                    "template_type": "generic",
                    "elements": [
                        {
                            "title": "Book Appointment",
                            "image_url": "https://www.vertical-leap.uk/wp-content/uploads/2017/09/robot-blue-background-1400x800.jpg",
                            "buttons": [
                                {
                                    "title": "Book",
                                    "payload": "Register"
                                }
                            ]
                        },
                        {
                            "title": "Book Appointment",
                            "image_url": "https://www.vertical-leap.uk/wp-content/uploads/2017/10/robot-touchscreen-1400x800.jpg",
                            "buttons": [
                                {
                                    "title": "Book",
                                    "payload": "Register"
                                }
                            ]
                        }
                    ]
                }
            }
        }
        dispatcher.utter_custom_json(gt)
        return []

class ActionRestarted(Action):
    def name(self):
        return "action_restarted"

    def run(self, dispatcher, tracker, domain):
        return [Restarted(), FollowupAction('action_greet')]

class RegistrationForm(FormAction, ActionGreet):
    otp = 0

    def name(self):
        return 'Registration_form'

    @staticmethod
    def required_slots(tracker):
        return ["name", "email", "phone", "otp", "dob", "time", "gender", "age", "payment", "paymentid"]

    def validate(self, dispatcher, tracker, domain):
        slot_values = self.extract_other_slots(dispatcher, tracker, domain)
        slot_to_fill = tracker.get_slot(REQUESTED_SLOT)
        if slot_to_fill:
            slot_values.update(self.extract_requested_slot(dispatcher, tracker, domain))
        for slot, value in slot_values.items():
            if value == "hi" or "restart" in value.lower():
                return [Form(None), Restarted(), FollowupAction('action_restarted')]

            if slot == 'name':
                print(value)
                if value.replace(" ", "").isalpha() == False:
                    dispatcher.utter_template('utter_wrong_name', tracker)
                    slot_values[slot] = None
                else:
                    dispatcher.utter_message("Hi {}".format(value))
            elif slot == 'email':
                email = re.compile(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)')
                mo = email.search(value)
                if mo == None:
                    dispatcher.utter_template('utter_wrong_email', tracker)
                    slot_values[slot] = None

            elif slot == 'phone':
                number = re.compile(r'^(?:(?:\+|0{0,2})91(\s*[\-]\s*)?|[0]?)?[789]\d{9}$')
                v = number.search(value)
                if v == None:
                    dispatcher.utter_template('utter_wrong_phone_number', tracker)
                    return [SlotSet('phone', None)]

            elif slot == 'dob':
                print(value)
                print(type(value))
                myclient = pymongo.MongoClient("mongodb://localhost:27017/")
                mydb = myclient["rasa"]
                mycol = mydb["Time"]
                x = {}
                date1 = ["26-01-2020", "11-01-2020", "12-01-2020", "13-01-2020", "14-01-2020", "15-01-2020"
                         "16-01-2020", "17-01-2020", "18-01-2020", "19-01-2020", "20-01-2020"
                         "21-01-2020", "22-01-2020", "23-01-2020", "24-01-2020", "25-01-2020"]
                if value == value:
                    print("Success")
                    x = mycol.find_one({}, {"sender_id": 1})
                    print(x)
                    print(type(x))
                    if value not in x.values():
                        mydict = {"sender_id": value, "9-10am": "", "10-11am": "", "2-3pm": "", "3-4pm": ""}
                        y = mycol.insert_one(mydict)
                        print(y)
                        print("If done")
                    else:
                        print("value is DB")
                else:
                    print("Over")

                myquery = {"sender_id": value}
                mydoc = mycol.find(myquery)
                print("else done")
                for x in mydoc:
                    print(x)
                    print(type(x))
                    res = []
                    res = [key for key, value in x.items() if not value]
                    print(res)
                    print("res done")
                    print(type(res))
                    for i in res:
                        print("for done")
                        gt = {
                            "attachment": {
                                "type": "timeslots",
                                "payload": {
                                    "template_type": "generic",
                                    "elements": [
                                        {
                                            "title": res,
                                            "payload": res,
                                        }
                                    ]
                                }
                            }
                        }
                        print(gt)
                        dispatcher.utter_custom_json(gt)

            elif slot == 'time':
                date = tracker.get_slot("dob")
                print(value)
                time = ["9-10am", "10-11am", "2-3pm", "3-4pm"]
                myclient = pymongo.MongoClient("mongodb://localhost:27017/")
                mydb = myclient["rasa"]
                mycol = mydb["Time"]
                x = {}
                if value in time:
                    mycol.update({"sender_id": date}, {"$set": {"11-12": value}})

            elif slot == 'payment':
                print(value)
                print(type(value))
                if value == "Pay Now":
                    dispatcher.utter_message("Scan BHIM UPI Code and pay")
                    pay = {
                        "attachment": {
                            "type": "payment",
                            "payload": {
                                "template_type": "generic",
                                "elements": [
                                    {
                                        "image_url": "https://i.postimg.cc/nrMDfFzB/1578799559433.jpg",
                                        "title": "Done",
                                    }
                                ]
                            }
                        }
                    }
                    dispatcher.utter_custom_json(pay)

                elif value == "Pay Later":
                    dispatcher.utter_message("Session end. Your appointment is not booked. Please try again with restart")
                    print("tq")

            elif slot == 'paymentid':
                id = len(value)
                if id == 12:
                    print(id)
                else:
                    dispatcher.utter_template('utter_wrong_Id', tracker)
                    return [SlotSet('paymentid', None)]

        return [SlotSet(slot, value) for slot, value in slot_values.items()]

    def submit(self, dispatcher, tracker, domain):
        name = tracker.get_slot("name")
        email = tracker.get_slot("email")
        phone = tracker.get_slot("phone")
        otp = tracker.get_slot("otp")
        dob = tracker.get_slot("dob")
        time = tracker.get_slot("time")
        gender = tracker.get_slot("gender")
        age = tracker.get_slot("age")
        payment = tracker.get_slot("payment")
        paymentid = tracker.get_slot("paymentid")
        dispatcher.utter_message("Hi" + " " + name + ". Your Appointment is booked on" + " " + dob + "," + time + ". Payment Success Rs.200/. PaymentID:" + paymentid + ". Thank you")
        message = {
            "attachment": {
                "type": "webvieww",
                "payload": {
                    "template_type": "buttons",
                    "elements": [
                        {
                            "text1": "Name:" + name,
                            "text2": "Email:" + email,
                            "text8": "phone:" + phone,
                            "text3": "Appointment Date:" + dob,
                            "text4": "Time:" + time,
                            "text5": "Fee:" + payment,
                            "text9": "Payment Success Rs.200/. PaymentId:" + paymentid,
                            "text6": "Gender:" + gender,
                            "text7": "Age:" + age,
                        },
                    ]
                }
            }
        }
        dispatcher.utter_custom_json(message)
        uniqId = randint(1, 1000000)
        most_recent_state = tracker.current_state()
        sender_id = most_recent_state['sender_id']
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["rasa"]
        mycol = mydb["person"]
        mydict = {"sender_id": uniqId, "Name": name, "Phone": phone, "dob": dob,
                  "Time": time, "Email": email, "gender": gender, "age": age, "Payment": payment}
        x = mycol.insert_one(mydict)

        return [SlotSet("name", None), SlotSet("email", None), SlotSet("phone", None), SlotSet("otp", None), SlotSet("dob", None), SlotSet("time", None),
                SlotSet("gender", None), SlotSet("age", None), SlotSet("payment", None), SlotSet("payment", None),
                Form(None), Restarted(), FollowupAction('action_thank')]

    def slot_mappings(self):
        return {"name": self.from_text(),
                "email": self.from_text(),
                "phone": self.from_text(),
                "otp": self.from_text(),
                "dob": self.from_text(),
                "time": self.from_text(),
                "payment": self.from_text(),
                "paymentid": self.from_text(),
                "gender": self.from_text(),
                "age": self.from_text(),
                }


class ActionThank(Action):
    def name(self):
        return "action_thank"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message("Please give Rate us")


class ActionDelete(Action):
    def name(self):
        return "action_delete"

    def run(self, dispatcher, tracker, domain):
        dname = tracker.get_slot("nremove")
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        db = myclient.rasa.person
        db.delete_one({'Name': dname})
        dispatcher.utter_message("Your appointment with the name {} has been cancelled".format(dname))

        
        
        