from flask import (
    flash,
    render_template,
    redirect,
    request,
    session,
    url_for,
)
from twilio.twiml.voice_response import VoiceResponse
from twilio.rest import Client

from ivr_phone_tree_python import app
from ivr_phone_tree_python.view_helpers import twiml

# replace with the number you want to use
RECEIVING_NUMBER = "+18324827880"

@app.route("/")
@app.route("/ivr")
def home():
    return render_template("index.html")


@app.route("/ivr/welcome", methods=["POST"])
def welcome():
    """Greets callers, presents a menu and gathers input"""
    response = VoiceResponse()
    with response.gather(
        num_digits=1, action=url_for("menu"), method="POST"
    ) as g:
        g.say(
                message="Thanks for calling Helper Bees Helper Support. " +
                "Please press 1 if you need to cancel an appointment with a client. " +
                "Press 2 if a client is in danger. " +
                "Press 3 for questions about timesheets or payments. " +
                "Press 4 if you are looking for available work or clients. " +
                "Press 5 for all other inquiries. " +
                "Press 6 to hear these options again. ")
        
    return twiml(response)


@app.route("/ivr/menu", methods=["POST"])
def menu():
    """ Directs callers based on their input """
    selected_option = request.form["Digits"]
    option_actions = {
                        "1": _transfer_call,
                        "2": _transfer_call,
                        "3": _record_financial_voicemail,
                        "4": _record_work_search_voicemail,
                        "5": _record_misc_voicemail,
                        "6": _redirect_welcome
                    }

    if selected_option in option_actions:
        response = VoiceResponse()
        if selected_option == "6":
            option_actions[selected_option]()

        else:
            option_actions[selected_option](response)
        return twiml(response)

    return _redirect_welcome()


@app.route("/ivr/finance_voicemail", methods=["POST"])
def finance_voicemail():

    """ Returns TwiML which prompts the caller to record a message"""
    
    response = _record("finance_message")
    
    return str(response)


@app.route("/ivr/finance_message", methods=["POST"])
def finance_message():
    """ Creates a client object and returns the transcription text to an SMS message"""
    
    message_sid = _send_transcription(request.form, "Payment and Timesheets")

    return message_sid


@app.route("/ivr/work_voicemail", methods=["POST"])
def work_voicemail():
    """ Returns TwiML which prompts the caller to record a message"""
    
    response = _record("work_message")

    return str(response)


@app.route("/ivr/work_message", methods=["POST"])
def work_message():
    """ Creates a client object and returns the transcription text to an SMS message"""
    
    message_sid = _send_transcription(request.form, "Work Inquiries")

    return message_sid

@app.route("/ivr/misc_voicemail", methods=["POST"])
def misc_voicemail():
    """ Returns TwiML which prompts the caller to record a message"""
    
    response = _record("misc_message")

    return str(response)


@app.route("/ivr/misc_message", methods=["POST"])
def misc_message():
    """ Creates a client object and returns the transcription text to an SMS message"""
    
    message_sid = _send_transcription(request.form, "Misc. Inquiries")

    return message_sid


def _transfer_call(response):
    response.say("Transferring your call to a Helper Bees team member")
    response.dial(RECEIVING_NUMBER)

    return response


def _record(message_route):
    response = VoiceResponse()
    if "RecordingSid" not in request.form:
        response.say("Please leave your message after the tone.")
        response.record(transcribe_callback="/ivr/{}".format(message_route))
    
    else:
        response.hangup()

    return response


def _record_financial_voicemail(response):
    return _route_to_voicemail(response, "finance_voicemail")


def _record_work_search_voicemail(response):
    return _route_to_voicemail(response, "work_voicemail")


def _record_misc_voicemail(response):
    return _route_to_voicemail(response, "misc_voicemail")


def _route_to_voicemail(response, route_name):
    response.redirect(url_for(route_name))
    return response


def _send_transcription(form, tag):
    client = Client()
    sender = form["From"]
    twilio_number = form["To"]

    transcription = form["TranscriptionText"]
    
    m = client.messages.create(
                                body = "From: {} \n{}: {}".format(sender, tag, transcription),
                                from_=twilio_number,
                                to=RECEIVING_NUMBER
                            )
    return str(m.sid)


def _redirect_welcome():
    response = VoiceResponse()
    response.redirect(url_for("welcome"))

    return twiml(response)
