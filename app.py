import os

from flask import Flask, request, redirect
import threading
from firebase_admin import credentials, firestore, initialize_app
import email_util

app = Flask(__name__)

email_util.init()

# Initialize Firestore DB
cred = credentials.Certificate('key.json')
default_app = initialize_app(cred)
db = firestore.client()


@app.route('/message_send', methods=('POST',))
def message_send():
    msg = request.form['msg']
    to_id = request.form['to_id']
    from_id = request.form['from_id']
    from_email = request.form['from_email']

    def inner():
        # TODO: use ML to check sentiment of `msg`
        ml_approved = False

        # TODO: DB lookup names of `to_id` and `from_id`
        to_name = 'Albert'
        from_name = 'Tony'
        if ml_approved:
            send(msg, to_id, from_id, from_email)
        else:
            # TODO: DB lookup recipient's squad's emails using `to_id`
            squad_emails = ['squaddtalk@gmail.com']
            for a in squad_emails:
                email_util.send_email(a, f'Approval for Message from {from_name} to {to_name}', msg,
                                      '<p>msg</p>')

    threading.Thread(target=inner, daemon=True).start()

    return {}


@app.route('/approve')
def approve():
    msg = request.args['msg']
    to_id = request.args['to_id']
    from_id = request.args['from_id']
    from_email = request.args['from_email']

    send(msg, to_id, from_id, from_email)

    # TODO: redirect to page on frontend
    return redirect('https://google.com')


def send(msg, to_id, from_id, from_email):
    # TODO: DB lookup recipient's email using `to_id`
    email = 'squaddtalk@gmail.com'

    # TODO: DB lookup names of `to_id` and `from_id`
    to_name = 'Albert'
    from_name = 'Tony'

    email_util.send_email(email, f'Message from {from_name}', msg, f'<p>{msg}</p>')


@app.route('/reject')
def reject():
    # TODO: redirect to page on frontend
    return redirect('https://google.com')


port = int(os.environ.get('PORT', 8080))
if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0', port=port)
