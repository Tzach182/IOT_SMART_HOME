import sys
import json
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import paho.mqtt.client as mqtt
from data import *

# Creating Client name - should be unique
global clientname
clientname = "IOT_client-Id-305152969"
relay_topic = 'healthUpdate/person/id/status'
global ON
ON = False


class Mqtt_client():

    def __init__(self):
        # broker IP address:
        self.broker = ''
        self.topic = ''
        self.port = ''
        self.clientname = ''
        self.username = ''
        self.password = ''
        self.subscribeTopic = ''
        self.publishTopic = ''
        self.publishMessage = ''
        self.on_connected_to_form = ''

    # Setters and getters
    def set_on_connected_to_form(self, on_connected_to_form):
        self.on_connected_to_form = on_connected_to_form

    def get_broker(self):
        return self.broker

    def set_broker(self, value):
        self.broker = value

    def get_port(self):
        return self.port

    def set_port(self, value):
        self.port = value

    def get_clientName(self):
        return self.clientName

    def set_clientName(self, value):
        self.clientName = value

    def get_username(self):
        return self.username

    def set_username(self, value):
        self.username = value

    def get_password(self):
        return self.password

    def set_password(self, value):
        self.password = value

    def get_subscribeTopic(self):
        return self.subscribeTopic

    def set_subscribeTopic(self, value):
        self.subscribeTopic = value

    def get_publishTopic(self):
        return self.publishTopic

    def set_publishTopic(self, value):
        self.publishTopic = value

    def get_publishMessage(self):
        return self.publishMessage

    def set_publishMessage(self, value):
        self.publishMessage = value

    def on_log(self, client, userdata, level, buf):
        print("log: " + buf)

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("connected OK")
            self.on_connected_to_form()
        else:
            print("Bad connection Returned code=", rc)

    def on_disconnect(self, client, userdata, flags, rc=0):
        print("DisConnected result code " + str(rc))

    def on_message(self, client, userdata, msg):
        topic = msg.topic
        m_decode = str(msg.payload.decode("utf-8", "ignore"))
        print("message from:" + topic, m_decode)
        mainwin.connectionDock.update_btn_state(m_decode)

    def connect_to(self):
        # Init paho mqtt client class
        self.client = mqtt.Client(self.clientname, clean_session=True)  # create new client instance
        self.client.on_connect = self.on_connect  # bind call back function
        self.client.on_disconnect = self.on_disconnect
        self.client.on_log = self.on_log
        self.client.on_message = self.on_message
        self.client.username_pw_set(self.username, self.password)
        print("Connecting to broker ", self.broker)
        self.client.connect(self.broker, self.port)  # connect to broker

    def disconnect_from(self):
        self.client.disconnect()

    def start_listening(self):
        self.client.loop_start()

    def stop_listening(self):
        self.client.loop_stop()

    def subscribe_to(self, topic):
        self.client.subscribe(topic)

    def publish_to(self, topic, message):
        self.client.publish(topic, message)


class ConnectionDock(QDockWidget):
    """Main """

    def __init__(self, mc):
        QDockWidget.__init__(self)

        self.mc = mc
        self.mc.set_on_connected_to_form(self.on_connected)
        self.eHostInput = QLineEdit()
        self.eHostInput.setInputMask('999.999.999.999')
        self.eHostInput.setText(broker_ip)

        self.ePort = QLineEdit()
        self.ePort.setValidator(QIntValidator())
        self.ePort.setMaxLength(4)
        self.ePort.setText(broker_port)

        self.eClientID = QLineEdit()
        global clientname
        self.eClientID.setText(clientname)

        self.eUserName = QLineEdit()
        self.eUserName.setText(username)

        self.ePassword = QLineEdit()
        self.ePassword.setEchoMode(QLineEdit.Password)
        self.ePassword.setText(password)

        self.eKeepAlive = QLineEdit()
        self.eKeepAlive.setValidator(QIntValidator())
        self.eKeepAlive.setText("60")

        self.eSSL = QCheckBox()

        self.eCleanSession = QCheckBox()
        self.eCleanSession.setChecked(True)

        self.eConnectbtn = QPushButton("Enable/Connect", self)
        self.eConnectbtn.setToolTip("click me to connect")
        self.eConnectbtn.clicked.connect(self.on_button_connect_click)
        self.eConnectbtn.setStyleSheet("background-color: gray")

        self.eSubscribeTopic = QLineEdit()
        self.eSubscribeTopic.setText(relay_topic)

        self.bodyTemperature = QPushButton("", self)
        self.bodyTemperature.setText('36')
        self.bodyTemperature.setStyleSheet("background-color: white")

        self.pulseRate = QPushButton("", self)
        self.pulseRate.setText('70')
        self.pulseRate.setStyleSheet("background-color: white")

        self.respirationRate = QPushButton("", self)
        self.respirationRate.setText('15')
        self.respirationRate.setStyleSheet("background-color: white")

        self.bloodPressure = QPushButton("", self)
        self.bloodPressure.setText('75')
        self.bloodPressure.setStyleSheet("background-color: white")

        self.notification = QTextEdit()

        formLayout = QFormLayout()
        formLayout.addRow("Turn On/Off", self.eConnectbtn)
        formLayout.addRow("Sub topic", self.eSubscribeTopic)
        formLayout.addRow("Body Temperature", self.bodyTemperature)
        formLayout.addRow("Pulse Rate", self.pulseRate)
        formLayout.addRow("Respiration Rate", self.respirationRate)
        formLayout.addRow("Blood Pressure", self.bloodPressure)
        formLayout.addRow("Notifications", self.notification)

        widget = QWidget(self)
        widget.setLayout(formLayout)
        self.setTitleBarWidget(widget)
        self.setWidget(widget)
        self.setWindowTitle("Connect")

    def on_connected(self):
        self.eConnectbtn.setStyleSheet("background-color: green")

    def on_button_connect_click(self):
        self.mc.set_broker(self.eHostInput.text())
        self.mc.set_port(int(self.ePort.text()))
        self.mc.set_clientName(self.eClientID.text())
        self.mc.set_username(self.eUserName.text())
        self.mc.set_password(self.ePassword.text())
        self.mc.connect_to()
        self.mc.start_listening()
        self.mc.subscribe_to(self.eSubscribeTopic.text())
        init_db(db_name)


    def doesHaveIrregularBodySigns(self, measurements):
        state = False
        if(34.0 > float(measurements["bodyTemperature"]) or float(measurements["bodyTemperature"]) > 38.0):
            state = True
        elif (60.0 > float(measurements["pulseRate"]) or float(measurements["pulseRate"]) > 100.0):
            state = True
        elif (12.0 > float(measurements["respirationRate"]) or float(measurements["respirationRate"]) > 16.0):
            state = True
        elif (80.0 > float(measurements["bloodPressure"]) or float(measurements["bloodPressure"]) > 120.0):
            state = True

        return state

    def irregularBodyVitalSignActions(self, measurements):
        self.notification.append('<span style=\"color: red\">Alert: Some body vitals show unusual sign. please contact a medical expert<span>')
        self.notification.append('<span style=\"color: red\">Body Vitals: Body Temperature: ' + measurements["bodyTemperature"] + "\nPulse Rate: " + measurements["pulseRate"] + "\nRespiration Rate: " + measurements["respirationRate"] + "\nBlood Pressure: " + measurements["bloodPressure"]+ "<span>")

    def update_btn_state(self, text):
        measurements = json.loads(text)
        if (measurements["type"]=="1"):
            self.bodyTemperature.setText(measurements["bodyTemperature"])
            self.pulseRate.setText(measurements["pulseRate"])
            self.respirationRate.setText(measurements["respirationRate"])
            self.bloodPressure.setText(measurements["bloodPressure"])
            insert_health_check(db_name, measurements)

            if(self.doesHaveIrregularBodySigns(measurements)):
                self.irregularBodyVitalSignActions(measurements)
            else:
                self.notification.append("Valid body signs. Keep your health in check")
                self.notification.setStyleSheet("color: green")
        else:
            print(get_health_update(db_name))
            self.notification.append('<span style=\"color: red\">Doctor has been notified about your condition, and all current readings sent to him<span>')

class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)

        # Init of Mqtt_client class
        self.mc = Mqtt_client()

        # general GUI settings
        self.setUnifiedTitleAndToolBarOnMac(True)

        # set up main window
        self.setGeometry(300, 300, 700, 700)
        self.setWindowTitle('Body Status')

        # Init QDockWidget objects
        self.connectionDock = ConnectionDock(self.mc)

        self.addDockWidget(Qt.TopDockWidgetArea, self.connectionDock)


app = QApplication(sys.argv)
mainwin = MainWindow()
mainwin.show()
app.exec_()

