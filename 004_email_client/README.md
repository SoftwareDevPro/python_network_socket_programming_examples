
# Python Networking Example Creating and Sending E-mail via SMTP

## To Run

1. Open password.txt and enter your password to the e-mail account (NOTE: this  is not the suggested way to store an account password).
2. Open message.txt, and update it to have the text of the e-mail message
3. Open mailing_client.py, and make changes as necessary:
   1. This example assumes a live.com account, other e-mail providers (e.g. Gmail) might require more steps to setup
   2. Change the server login to have the account being logged into to send e-mails.
   3. Update the message parts as necessary (From, To, Subject)
   4. Update the attachment filename as necessary
   5. Update the sendmail call to the desired from address (1st parameter), and recipients (2nd parameter).

```
python mailing_client.py
```
