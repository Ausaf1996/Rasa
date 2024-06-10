## story_1000
* greet
  - action_greet
  
## story_2000
* Register
    - Registration_form
    - form{"name": "Registration_form"}
    - slot{"requested_slot": "name"}
* form: inform{"name": "chaitanya"}
    - form: Registration_form
    - slot{"name": "chaitanya"}
    - slot{"requested_slot": "email"}
* form: inform{"email": "abc@gmail.com"}
    - form: Registration_form
    - slot{"email": "abc@gmail.com"}
    - slot{"requested_slot": "phone"}
* form: inform{"phone": "9987634567"}
    - form: Registration_form
    - slot{"phone": "99987634567"}
    - slot{"requested_slot": "otp"}
* form: inform{"otp": "111245"}
    - form: Registration_form
    - slot{"otp": "111245"}
    - slot{"requested_slot": "dob"}
* form: inform{"dob": "12-2-1995"}
    - form: Registration_form
    - slot{"dob": "12-2-1995"}
    - slot{"requested_slot": "time"}
* form: inform{"time": "22:30"}
    - form: Registration_form
    - slot{"time": "22:30"}
    - slot{"requested_slot": "gender"}
* form: inform{"gender": "male"}
    - form: Registration_form
    - slot{"gender": "male"}
    - slot{"requested_slot": "age"}
* form: inform{"age": "23"}
    - form: Registration_form
    - slot{"age": "23"}
    - slot{"requested_slot": "payment"}
* form: inform{"payment": "200"}
    - form: Registration_form
    - slot{"payment": "200"}
     - slot{"requested_slot": "paymentid"}
* form: inform{"paymentid": "900500125854"}
    - form: Registration_form
    - slot{"paymentid": "900500158545"}
    - form{"name": null}
    - slot{"requested_slot": null}
* bye
  - utter_bye
  
## story_3000
* images
  - utter_images
  
## story_4000
* delete
  - utter_delete_detail
* inform
  - slot{"nremove": "Ausaf"}
  - action_delete