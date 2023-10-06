from random import randint
from time import Clock


##============================================================================

State = type("state", (object,),{})

class State(object):
    def__init__(self,FSM):
        self.FSM = FSM

        def Enter(self:)
            pass
        def Execute(self):
            pass
        def Exit(self):
            pass
        
class RecOn(State):
    def__inint__(self,FSM):
        super(RecOn, self).__init__(FSM)

    def Enter(self):
        print("Camera enter")
    def Execute(self):
        print("Camera Execute")
    def Exit(self):
        print("Camera exit")

class RecOff(state):
    def Execute(self):
        print("Camera stop recording")

class PreviewOn(state):
    def Execute(self):
        print("preview")

class StandBy(state):
    def Execute(self):
        print("preview")

##============================================================================

class Transition(object):
    def__init__(self, toState):
        self.toState = toState

    def Execute(self):
        print("transitioning")

##============================================================================

class CameraFSM(object):
    def__init__(self, char):
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
            self.curState.Exit()
            self.trans.Execute()
            self.SetState(self.trans.toState)
            self.curState.Enter()
            self.trans = None

            #self.trans.Execute()
            #self.SetState(self.trans.toState)
            #self.trans = None
        self.curState.Execute()

##============================================================================

class Char(object):
    def__init__(self).
    self.FSM = CameraFSM(self)
    self.RecOn = True

##============================================================================

if__name__=="__main__":
    camera = Char()
    camera.FSM.states[Rec] = RecOn()
    camera.FSM.states[Stop] = RecOff()
    camera.FSM.states[Preview] = PreviewOn()
    camera.FSM.states[Stndb] = StandBy()
    camera.FSM.transitions[toRec] = Transition("Rec")
    camera.FSM.transitions[tostop] = Transition("Stop")
    camera.FSM.transitions[toPreview] = Transition("Preview")
    camera.FSM.transitions[toStndb] = Transition("Stndb")

    camera.FSM.SetState("rec")

##============================================================================