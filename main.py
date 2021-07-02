from threadedUDPServer import ThreadedUDPServer, ThreadedUDPRequestHandler
import threading
from signal import signal, SIGINT
from time import sleep

APP_IP_ADDRESS = "172.16.2.121"
APP_PORT = 49000

isRunning = True

def stop():
    global isRunning
    isRunning = False

def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    stop()

def Main():
    server = ThreadedUDPServer(server_address=(APP_IP_ADDRESS, APP_PORT), RequestHandlerClass=ThreadedUDPRequestHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()

    while isRunning:
        sleep(2)

    server.shutdown()
    server.server_close()

if __name__ == '__main__':
    signal(SIGINT, signal_handler)
    Main()