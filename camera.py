from signal import pause
import time
from gpiozero import LED, Button

from picamera2 import Picamera2, Preview
import digitalio
import board
from PIL import Image, ImageDraw
from adafruit_rgb_display import st7735


ledR = LED(17)
ledG = LED(27)
ledB = LED(22)
btn = Button(23)

#display
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = digitalio.DigitalInOut(board.D24)

#start camera
picam = Picamera2()
config = picam.create_preview_configuration()
picam.configure(config)

picTaken = False
picShown = True

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 24000000

# Setup SPI bus using hardware SPI:
spi = board.SPI()

# Create the display:
# Turn on the Backlight
#backlight = DigitalInOut(board.D18)
#backlight.switch_to_output()
#backlight.value = True

disp = st7735.ST7735R(
    spi,
    rotation=90,
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
)

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
        for i in range(1):
            startTime = time.time()
            timeInterval = 1
            while (startTime + timeInterval > time.time()):
                #===============
                picam.start()
                picam.capture_file("test.jpg")
                #time.sleep(2)
                #picam.start_and_capture_file("test.jpg")
                #picam.close()
                print("pictaken")
                
                # Create blank image for drawing.
                if disp.rotation % 180 == 90:
                    height = disp.width  # we swap height/width to rotate it to landscape!
                    width = disp.height
                else:
                    width = disp.width  # we swap height/width to rotate it to landscape!
                    height = disp.height
                image = Image.new("RGB", (width, height))

                # Get drawing object to draw on image.
                draw = ImageDraw.Draw(image)

                # Draw a black filled box to clear the image.
                draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
                disp.image(image)
                
                #show image in display
                image = Image.open("test.jpg")

                # Scale the image to the smaller screen dimension
                image_ratio = image.width / image.height
                screen_ratio = width / height
                if screen_ratio < image_ratio:
                    scaled_width = image.width * height // image.height
                    scaled_height = height
                else:
                    scaled_width = width
                    scaled_height = image.height * width // image.width
                image = image.resize((scaled_width, scaled_height), Image.BICUBIC)

                # Crop and center the image
                x = scaled_width // 2 - width // 2
                y = scaled_height // 2 - height // 2
                image = image.crop((x, y, x + width, y + height))

                # Display image.
                disp.image(image)
                print("preview")
                
            #back to off state
            camera.FSM.Transition("toRecOff")
            camera.FSM.Execute()

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
    
    camera.FSM.Transition("toPreview")
    camera.FSM.Execute()

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
    #print("{}".format(camera.FSM.curState))
    #if (camera.FSM.curState == "RecOff"):
    #    camera.FSM.Transition("toPreview")
    #else:
    #    camera.FSM.Transition("toRecOff")
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