import threading, time
from KeyboardInput import KeyboardProcessor

class FakeEvent:
    def __init__(self,name):
        self.name=name
        self.event_type="down"

def worker(kp, keys):
    for k in keys:
        kp.process_key(FakeEvent(k))
        # tiny sleep to force context switch
        time.sleep(0.001)

def test_keyboard_processor_thread_safety():
    keymap={"up":"up","down":"down","left":"left","right":"right"}
    kp=KeyboardProcessor(8,8,keymap)
    seq1=["up","up","left","down","right"]*50
    seq2=["down","right","right","up","left"]*50
    t1=threading.Thread(target=worker,args=(kp,seq1))
    t2=threading.Thread(target=worker,args=(kp,seq2))
    t1.start(); t2.start(); t1.join(); t2.join()
    r,c=kp.get_cursor()
    assert 0<=r<8 and 0<=c<8, "Cursor out of bounds after concurrent access" 