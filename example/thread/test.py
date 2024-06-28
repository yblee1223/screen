import threading
import time


def takes_long(event: threading.Event):
    time.sleep(5)
    print("[Long ] Started!")
    event.set()


def takes_short(event: threading.Event):
    print("[Short] Waiting for other thread!")
    event.wait()
    print("[Short] Started!")


event_ = threading.Event()
threading.Thread(target=takes_long, args=[event_]).start()
threading.Thread(target=takes_short, args=[event_]).start()