# A dummy class for testing the GUI on a desktop without PySerial

class Serial:
    def __init__(self, port, baudrate):
        print('Serial device initialized on port ' + port)
    def write(self, data):
        print('Writing data: ' + str(data))
