# HelperBees_IVR_Project
A Flask API written with Python 3.5 intended to receive incoming calls to a Twilio phone number, determine if the call is an emergency, and route it either to a representative or to leave a message.

## Local Development

1. First clone this repository and `cd` into it.

   ```bash
   $ git clone git@github.com:TwilioDevEd/ivr-phone-tree-python.git
   $ cd ivr-phone-tree-python
   ```

1. Create a new virtual environment.

    - If using vanilla [virtualenv](https://virtualenv.pypa.io/en/latest/):

        ```bash
        virtualenv venv
        source venv/bin/activate
        ```

    - If using [virtualenvwrapper](https://virtualenvwrapper.readthedocs.org/en/latest/):

        ```bash
        mkvirtualenv ivr-phone-tree-python
        ```

1. Install the dependencies.

    ```bash
    pip install -r requirements.txt
    ```

1. Make sure the tests succeed.

    ```bash
    $ coverage run manage.py test
    ```

1. Start the server.

    ```bash
    python manage.py runserver
    ```

1. Expose the application to the wider Internet using [ngrok](https://ngrok.com/).

    ```bash
    ngrok http 5000 -host-header="localhost:5000"
    ```

1. Configure Twilio to call your webhooks

  You will also need to configure Twilio to call your application when calls are
  received in your [*Twilio Number*](https://www.twilio.com/user/account/messaging/phone-numbers).
  The voice url should look something like this:

  ```
  http://<your-ngrok-subdomain>.ngrok.io/ivr/welcome
  ```
