import queue
import socketserver
import threading
import struct
import binascii

import constants

class ThreadedMsgProcess(threading.Thread):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.msgQueue = args[0]
        self.counter = 0
        self.msgIndex = 0
        self.msgLabel = []
        self.msgData = []
        self._args, self._kwargs = args, kwargs
        self._stop_event = threading.Event()
    
    def run(self):
        with open('xplane_data.txt', mode='w') as txt_file:
            while not(self._stop_event.is_set()):
                try:
                    record = self.msgQueue.get(block=False)
                except queue.Empty:
                    pass
                else:
                    self.counter += 1
                    print('Data Counter ',self.counter)
                    data = self.parsingData(record)
                    txt_file.write(record)
                    txt_file.write('\n')
                    # txt_file.write(json.dumps(data))
                    # txt_file.write('\n')

    def parsingData(self, record):
        dataArr = []
        for indexStart in range(0, len(record), 2):
            dataArr.append(record[indexStart:indexStart+2])

        dataArr = dataArr[5:]
        results = []
        template = []
        for idx in range(0, len(dataArr), 36):
            currentIdx = idx
            result = {}
            result['msgIndex'] = self.parseUnsignedInteger(dataArr[currentIdx:currentIdx+4])
            if result['msgIndex']==20:
                template = constants.MESSAGE_INDEX20_TEMPLATE
            elif result['msgIndex']==17:
                template = constants.MESSAGE_INDEX17_TEMPLATE
            elif result['msgIndex']==3:
                template = constants.MESSAGE_INDEX03_TEMPLATE
            else:
                template = constants.MESSAGE_OTHER_TEMPLATE
            
            data = {}
            for dataIdx in range(0, 8):
                currentIdx = currentIdx+4
                if template[dataIdx]!=constants.MessageData.SKIP:
                    data[template[dataIdx].msg_label] = self.parseFloat(dataArr[currentIdx:currentIdx+4])
            
            result['data'] = data
            results.append(result)

        print(results)
                    
    def parseUnsignedInteger(self, data: list):
        data_bin = binascii.a2b_hex("".join(data))
        value = struct.unpack('<I',data_bin)
        return value[0] if value and len(value)>0 else 0

    def parseFloat(self, data: list):
        data_bin = binascii.a2b_hex("".join(data))
        value = struct.unpack('<f',data_bin)
        return value[0] if value and len(value)>0 else -999

    def stop(self):
        self._stop_event.set()

    def clone(self):
        return ThreadedMsgProcess(*self._args, **self._kwargs)

class ThreadedUDPRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request[0].strip().hex()
        current_thread = threading.current_thread()
        print("{}: client: {}, wrote: {}".format(current_thread.name, self.client_address, data))

        if data.startswith('44415441'):
            self.server.msgQueue.put(data)

class ThreadedUDPServer(socketserver.ThreadingMixIn, socketserver.UDPServer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.msgQueue = queue.Queue()
        self.threaderMsgProcess = ThreadedMsgProcess(self.msgQueue)
        self.threaderMsgProcess.start()
    
    def shutdown(self):
        self.threaderMsgProcess.stop()
        return super().shutdown()