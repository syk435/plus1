import bluetooth
import time

def init():	
    target_name = "HC-06"
    target_address = None

    nearby_devices = bluetooth.discover_devices()

    for bdaddr in nearby_devices:
        if target_name == bluetooth.lookup_name( bdaddr ):
            target_address = bdaddr
            break
    port = 1

    try:
        sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
        sock.connect((target_address, port))
        sock.send("7Aw9")
        start_time = time.time()
    except:
        pass
    time.sleep(0.25)
    return sock

def plus1(sock):
    sock.send("7Ar1")
    time.sleep(0.8)
    sock.send("1Xb6")
    time.sleep(0.8)
    sock.send("7Ar1")
    time.sleep(0.8)
    sock.send("4Xb6")
    time.sleep(0.8)

def heartbeat(sock):
    try:
        sock.send("8Ag1")
        time.sleep(0.14)
        sock.send("8Ag4")
        time.sleep(0.14)
        sock.send("8Ag5")
        time.sleep(0.14)
        sock.send("8Ag7")
        time.sleep(0.14)
        sock.send("8Ag8")
        time.sleep(0.14)
        sock.send("8Ag9")
        time.sleep(0.14)
        sock.send("8Ag8")
        time.sleep(0.14)
        sock.send("8Ag7")
        time.sleep(0.14)
        sock.send("8Ag5")
        time.sleep(0.14)
        sock.send("8Ag4")
        time.sleep(0.14)
        sock.send("8Ag1")
        time.sleep(0.14)

        sock.send("9Ab1")
        time.sleep(0.14)
        sock.send("9Ab4")
        time.sleep(0.14)
        sock.send("9Ab5")
        time.sleep(0.14)
        sock.send("9Ab7")
        time.sleep(0.14)
        sock.send("9Ab8")
        time.sleep(0.14)
        sock.send("9Ab9")
        time.sleep(0.14)
        sock.send("9Ab8")
        time.sleep(0.14)
        sock.send("9Ab7")
        time.sleep(0.14)
        sock.send("9Ab5")
        time.sleep(0.14)
        sock.send("9Ab4")
        time.sleep(0.14)
        sock.send("9Ab1")
        time.sleep(0.14)
    except:
        pass

def transition(sock,prev,curr):
    try:
        sock.send(prev+"Ar3")
        time.sleep(0.14)
        sock.send(prev+"Aw9")
        time.sleep(0.14)
        sock.send(curr+"Aw3")
        time.sleep(0.14)
        sock.send(curr+"Ar9")
        time.sleep(0.14)
    except:
        pass

sock = init()
prevSect = '3'
currSect = '1'
try:
    # while True:
    #     sock.send(prevSect+"Xb9")
    #     time.sleep(0.14)
    #     sock.send(currSect+"Xr9")
    #     time.sleep(0.14)
    #     sock.send('7Xg9')
    #     time.sleep(1)
    #     # transition(sock,prevSect,currSect)

    # sock.send("8Ag1")
    # time.sleep(0.14)
    # sock.send("9Ab1")
    # time.sleep(0.14)
    # while True:
    #     heartbeat(sock)
    #     heartbeat(sock)
    #     heartbeat(sock)
    #     heartbeat(sock)
    #     heartbeat(sock)

    while True:
        plus1(sock)
except:
    pass
finally:
    sock.close()