from gpiozero import LED, Button
from signal import pause
import time

ledR = LED(17)
ledG = LED(27)
ledB = LED(22)
btn = Button(23)

##============================================================================

State = type("state", (object,),{})

"""
class State(object):
    def __init__(self,FSM):
        self.FSM = FSM

        def Enter(self):
            pass
        def Execute(self):
            pass
        def Exit(self):
            pass
"""    

class RecOn(State):
    def Execute(self):
        print("Recording")
        ledR.on()
        
    #def __inint__(self,FSM):
    #    super(RecOn, self).FSM
    #def Enter(self):
    #    print("Camera enter")
    #def Exit(self):
    #    print("Camera exit")

class RecOff(State):
    def Execute(self):
        print("StopRecording")
        ledG.on()

class PreviewOn(State):
    def Execute(self):
        ledB.on()
        print("preview")

class StandBy(State):
    def Execute(self):
        print("standby")

##============================================================================

class Transition(object):
    def __init__(self, toState):
        self.toState = toState

    def Execute(self):
        print("transitioning")
        ledR.off()
        ledG.off()
        ledB.off()

##============================================================================

class CameraFSM(object):
    def __init__(self, char):
        self.char = char
        self.states = {}
        self.transitions = {}
        self.prevState = None
        self.curState = None
        self.trans = None

    def SetState(self, stateName):
        self.prevState = self.curState
        self.curState = self.states[stateName]

    def Transition(self, transName):
        self.trans = self.transitions[transName]

    def Execute(self):
        if(self.trans):
            self.SetState(self.trans.toState)
            #self.curState.Exit()
            #self.trans.Execute()
            #self.curState.Enter()

            self.trans.Execute()
            self.SetState(self.trans.toState)
            self.trans = None
        self.curState.Execute()

##============================================================================

class Char(object):
    def __init__(self):
        self.FSM = CameraFSM(self)
        self.RecOff = True

##============================================================================

if __name__ == "__main__":
    camera = Char()
    
    camera.FSM.states["Rec"] = RecOn()
    camera.FSM.states["RecOff"] = RecOff()
    camera.FSM.states["Preview"] = PreviewOn()
    camera.FSM.states["Stndb"] = StandBy()
    camera.FSM.transitions["toRec"] = Transition("Rec")
    camera.FSM.transitions["toRecOff"] = Transition("RecOff")
    camera.FSM.transitions["toPreview"] = Transition("Preview")
    camera.FSM.transitions["toStndb"] = Transition("Stndb")
    camera.FSM.SetState("Rec")

##============================================================================

def singlePress():
    if (camera.RecOff):
        camera.FSM.Transition("toRecOff")
        camera.RecOff = False
    else:
        camera.FSM.Transition("toRec")
        camera.RecOff = True
    camera.FSM.Execute()
        
    print("siglePress!")
    camera.FSM.Transition("toRec")

def longPress():
    print("longPress")
    camera.FSM.Transition("toPreview")
    camera.FSM.Execute()

def pressed(btn):
    hold_time = 0.5
    start_time=time.time()
    diff=0

    while btn.is_active and (diff < hold_time) :
        now_time=time.time()
        diff =- start_time+now_time

    if diff < hold_time :
        singlePress()
    else:
        longPress()

btn.when_pressed = pressed

pause()