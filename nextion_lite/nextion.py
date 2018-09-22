from machine import UART
from micropython import const
import ustruct

COMMAND_PAGE_ID = 'page'
COMMAND_COMPONENT = 'ref'
COMMAND_CLICK = 'click'
COMMAND_STOP_REFRESH = 'ref_stop'
COMMAND_REFRESH_START = 'ref_star'
COMMAND_GET = 'get'
COMMAND_GET_PAGE = 'sendme'
COMMAND_VISIBLE = 'vis'
COMMAND_TOUCH_ENABLED = 'tsw'
COMMAND_ADD_DATA = 'add'
COMMAND_ADD_DATA_BULK = 'addt'
COMMAND_CLEAR = 'cle'
COMMAND_RESET = 'rest'

R_COMMAND_TOUCH_EVENT = const(0x65)
R_COMMAND_PAGE_ID = const(0x66)
R_COMMAND_TOUCH_COORDINATE = const(0x67)
R_COMMAND_TOUCH_COORDINATE_SLEEP_MODE = const(0x68)
R_COMMAND_STRING_DATA = const(0x70)
R_COMMAND_NUMERIC_DATA = const(0x71)
R_COMMAND_AUTO_SLEEP = const(0x86)
R_COMMAND_AUTO_WAKE_UP = const(0x87)
R_COMMAND_SYSTEM_STARTUP = const(0x88)
R_COMMAND_SD_UPGRADE = const(0x89)
R_COMMAND_TRANSPARENT_TRANSMIT_FINISHED = const(0xFD)
R_COMMAND_TRANSPARENT_TRANSMIT_READY = const(0xFE)


class Nextion(UART):

    read_buffer = bytearray(100)

    command = None
    page = None
    id = None
    touch_event = None
    x = None
    y = None
    data = None

    def __init__(self, port=1, baud=9200):
        super(Nextion, self).__init__(port, baud)

    def send(self, command, *args):
        length = len(args)
        for arg in args:
            length += len(str(arg))
        write_buffer = bytearray(len(command) + length + 3)
        write_buffer[0: len(command)] = bytes(command, 'ASCII')
        index = 0
        for arg in args:
            if index > 0:
                write_buffer[len(command) + index:len(command) + index + 1] = b','
            else:
                write_buffer[len(command) + index:len(command) + index + 1] = b' '
            #write_buffer[len(command) + index:len(command) + index + 1] = b' '
            write_buffer[len(command) + index + 1:len(command) + index + 1 + len(str(arg))] = bytes(str(arg), 'ASCII')
            index += 1 + len(str(arg))
        write_buffer[-3:] = b'\xff\xff\xff'
        print(write_buffer)
        self.write(write_buffer)

    def check_data(self, callback):
        if self.any():
            chars = self.readinto(self.read_buffer, 100)
            index = 0
            while index < chars:
                self.command = self.read_buffer[index]
                index += 1
                if self.command in [R_COMMAND_TOUCH_EVENT, R_COMMAND_PAGE_ID]:
                    self.page = self.read_buffer[index]
                    index += 1
                if self.command == R_COMMAND_TOUCH_EVENT:
                    self.id = self.read_buffer[index]
                    index += 1
                if self.command in [R_COMMAND_TOUCH_COORDINATE, R_COMMAND_TOUCH_COORDINATE_SLEEP_MODE]:
                    self.x = self.read_buffer[index:index + 2]
                    self.y = self.read_buffer[index + 2:index + 4]
                    index += 4
                if self.command in [R_COMMAND_TOUCH_EVENT, R_COMMAND_TOUCH_COORDINATE, R_COMMAND_TOUCH_COORDINATE_SLEEP_MODE]:
                    self.touch_event = self.read_buffer[index]
                    index += 1
                if self.command == R_COMMAND_STRING_DATA:
                    length = 0
                    while self.read_buffer[index + length:index + length + 3] != b'\xff\xff\xff':
                        length += 1
                    self.data = self.read_buffer[index:index + length]
                    index += length
                if self.command == R_COMMAND_NUMERIC_DATA:
                    self.data = ustruct.unpack('<i', self.read_buffer[index:index + 4])[0]
                    index += 4
                if self.read_buffer[index: index + 3] == b'\xff\xff\xff':
                    index += 3
                    callback(command=self.command, page=self.page, id=self.id, touch_event=self.touch_event)

                    # Reset
                    self.command = None
                    self.page = None
                    self.id = None
                    self.touch_event = None
                    self.x = None
                    self.y = None
                    self.data = None
                else:
                    print('invalid command')
                    return



