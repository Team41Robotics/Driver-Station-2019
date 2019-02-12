PARITY_NONE = 1
STOPBITS_ONE = 1
EIGHTBITS = 1

class Serial:
    def __init__(self, port, baudrate, parity, stopbits, bytesize, timeout):
        print('Serial device initialized on port ' + port)
    def write(self, data):
        print('Writing data: ' + str(data))
