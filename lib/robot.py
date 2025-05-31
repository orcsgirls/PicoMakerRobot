import time
import board
import pwmio
import neopixel
import simpleio
from adafruit_motor import servo, motor
from digitalio import DigitalInOut, Direction, Pull
from pulseio import PulseIn

#-------------------------------------------------------------------
# Motor: Class for driving the robot
#-------------------------------------------------------------------
class Motors:
    def __init__(self):
        m1a = pwmio.PWMOut(board.GP8, frequency=50)
        m1b = pwmio.PWMOut(board.GP9, frequency=50)
        m2a = pwmio.PWMOut(board.GP10, frequency=50)
        m2b = pwmio.PWMOut(board.GP11, frequency=50)
        self.motor1 = motor.DCMotor(m1a, m1b)
        self.motor2 = motor.DCMotor(m2a, m2b)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
            self.stop()

    def stop(self):
        self.motor1.throttle = 0.0
        self.motor2.throttle = 0.0

    def forward(self, speed=0.5, duration=None):
        self.motor1.throttle = speed
        self.motor2.throttle = speed
        if(duration):
            time.sleep(duration)
            self.stop()

    def backward(self, speed=0.5, duration=None):
        self.forward(speed=-speed, duration=duration)

    def right(self, speed=0.5, duration=None, tankmode=True):
        self.motor1.throttle = speed
        self.motor2.throttle = -speed if tankmode else 0.0
        if(duration):
            time.sleep(duration)
            self.stop()

    def left(self, speed=0.5, duration=None, tankmode=True):
        self.right(speed=-speed, duration=duration, tankmode=tankmode)

#-------------------------------------------------------------------
# Sonar: Class for ultrasonic sensor
#-------------------------------------------------------------------
class Sonar:
    def __init__(self, trigger_pin, echo_pin, timeout=0.1):
        self._timeout = timeout
        self._trig = DigitalInOut(trigger_pin)
        self._trig.direction = Direction.OUTPUT
        self._echo = PulseIn(echo_pin)
        self._echo.pause()
        self._echo.clear()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.deinit()

    def deinit(self):
        self._trig.deinit()
        self._echo.deinit()

    @property
    def distance(self):
        self._echo.clear()  # Discard any previous pulse values
        self._trig.value = True  # Set trig high
        time.sleep(0.00001)  # 10 micro seconds 10/1000/1000
        self._trig.value = False  # Set trig low

        pulselen = None
        timestamp = time.monotonic()

        self._echo.resume()
        while not self._echo:
            # Wait for a pulse
            if (time.monotonic() - timestamp) > self._timeout:
                self._echo.pause()
                raise RuntimeError("Timed out")
        self._echo.pause()
        pulselen = self._echo[0]

        # positive pulse time, in seconds, times 340 meters/sec, then
        # divided by 2 gives meters. Multiply by 100 for cm
        # 1/1000000 s/us * 340 m/s * 100 cm/m * 2 = 0.017
        return pulselen * 0.017

#-------------------------------------------------------------------
# Leds: Class for the Neopixels
#-------------------------------------------------------------------
class Leds:
    def __init__(self):
        self.pixels = neopixel.NeoPixel(board.GP18, 2)
        self.pixels.fill((0,0,0))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.pixels.deinit()

    def _wheel(self, pos):
        pos = pos % 255
        if pos < 0:
            pos = pos + 255
        if pos < 85:
            r = int(pos * 3)
            g = int(255 - pos * 3)
            b = 0
        elif pos < 170:
            pos -= 85
            r = int(255 - pos * 3)
            g = 0
            b = int(pos * 3)
        else:
            pos -= 170
            r = 0
            g = int(pos * 3)
            b = int(255 - pos * 3)
        return (r, g, b)

    def _clamp(self, n, min_value, max_value):
        return max(min_value, min(n, max_value))

    def left_color(self, color):
        self.pixels[1] = color
        self.pixels.show()

    def right_color(self, color):
        self.pixels[0] = color
        self.pixels.show()

    def color(self, color):
        self.pixels.fill(color)

    def left_color_hue(self, hue):
        self.left_color(self._wheel(hue))

    def right_color_hue(self, hue):
        self.right_color(self._wheel(hue))

    def color_hue(self, hue):
        self.pixels.fill(self._wheel(hue))

    def off(self):
        self.pixels.fill((0,0,0))

    @property
    def brightness(self):
        return self.pixels.brightness

    @brightness.setter
    def brightness(self, value):
        self.pixels.brightness = self._clamp(value, 0.0, 1.0)

#-------------------------------------------------------------------
# Linesensor: Class for the  linesensor
#-------------------------------------------------------------------
class Linesensor():
    def __init__(self, sensor_pin):
        self.sensor = DigitalInOut(sensor_pin)
        self.sensor.direction = Direction.INPUT
        self.sensor.pull = Pull.UP

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.sensor.deinit()

    @property
    def line_detected(self):
        return self.sensor.value

#-------------------------------------------------------------------
# Button: Class for the  on board buttons
#-------------------------------------------------------------------
class Button():
    def __init__(self, pin):
        self.btn = DigitalInOut(pin)
        self.btn.direction = Direction.INPUT
        self.btn.pull = Pull.UP
        self.lastState = self.btn.value

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.btn.deinit()

    def clicked(self):
        currentState = self.btn.value
        if currentState != self.lastState:
            self.lastState=currentState
            return currentState
        else:
            return False

    @property
    def pressed(self):
        return not self.btn.value

#-------------------------------------------------------------------
# Buzzer: Class for the on board piezo buzzer
#-------------------------------------------------------------------
class Buzzer():
    def __init__(self):
        self._PIEZO_PIN = board.GP22

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def beep(self, tone=500, duration=0.2):
        simpleio.tone(self._PIEZO_PIN, tone, duration=duration)

    def alert(self):
        MELODY_NOTE = [659,520,659,520]
        MELODY_DURATION = [0.2,0.2,0.2,0.2]
        self.play(MELODY_NOTE, MELODY_DURATION)

    def siren(self, repeat=1):
        sound = list(range(400,700,10)) + list(range(700,400,-10))
        time = [0.02]*len(sound)
        for r in range(repeat):
            self.play(sound, time)

    def play(self, melody, duration):
        for i in range(len(melody)):
            simpleio.tone(self._PIEZO_PIN, melody[i], duration=duration[i])
