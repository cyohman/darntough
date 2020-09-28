import flask
from flask import request
from flask_mail import Mail
from flask_mail import Message
import re

#Setup for Flask & Mail
mail = Mail()
app = flask.Flask(__name__)

#Flask Settings
app.config["DEBUG"] = True

#Mail Settings
###Mailtrap.io settings - stmp server that does not actually send mail - mailtrap.io ###
#Settings for mailtrap.io
app.config['MAIL_SERVER']='smtp.mailtrap.io'
app.config['MAIL_PORT'] = 2525
app.config['MAIL_USERNAME'] = 'eb54122858d0fe'
app.config['MAIL_PASSWORD'] = 'bde8ba00acf449'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
#Default Sender for Emails
app.config['MAIL_DEFAULT_SENDER'] = 'noreply@darntough.com'
###End of Mailtrap.io settings###

#Initialize Mail app
mail.init_app(app)

#This did not necessarily work- Tripped up on email address with two dots in the prefix- chance.yohman.ae@gmail.com
regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

def isValidEmail(email):  
  
    # pass the regular expression 
    # and the string in search() method 
    if(re.search(regex,email)):  
    #    print("Valid Email")
        return True  
    else:  
    #    print("Invalid Email")
        return False

#Parameters
#recipient(Required) - Need to send the email somewhere
#file(Optional) - Attachment related to notification
@app.route('/email', methods=['POST'])
def email():
    
    try:
    
       recipient = request.form.get('recipient')
       
       #Debugging Output
       #print(recipient)

       #If no recipient, return a Bad Request
       if (recipient == None):
          return flask.Response(status=400)   
 
       #Validate the email- This is not working exactly right. See note for the regex above
       if isValidEmail(recipient)==False:
          return flask.Response(status=400)

       #Debugging Output
       #print(request.form)
       #print(request)
       #print(request.files)
       #print(len(request.files))

       #Debugging Output
       #print(request.files['file'].content_type)
       
       msg = Message("Darn Tough Email Notification",
                  recipients=[recipient])
       #print(msg)


       #Check if there is an attaachment and act appropriately
       #Debugging Output
       #print('file' in request.files)     

       if('file' in request.files):
          #print("Attachment")
          msg.body="There is an attachment."
          msg.attach(request.files['file'].filename, request.files['file'].content_type,  request.files['file'].read())
       else:
          #print("No Attachment") 
          msg.body="There is no attachment."
       
       mail.send(msg)
       
       #print ("Successfully sent email")
       return flask.Response(status=200)
    except:
       #print ("Error sending email")
       return flask.Response(status=500)

if __name__=='__main__':
    app.run(debug=True)
