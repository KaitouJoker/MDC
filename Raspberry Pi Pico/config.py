from machine import Pin, PWM, UART

hc06:UART = UART(
    0,
    baudrate = 9600,
    bits = 8,
    parity = None,
    stop = 1,
    tx = Pin(0),
    rx = Pin(1))

pixy:UART = UART(
    1,
    baudrate = 9600,
    bits = 8,
    parity = None,
    stop = 1,
    tx = Pin(4),
    rx = Pin(5))

pico_LED:Pin = Pin("LED", Pin.OUT)

_motor1_a:Pin = Pin(13, Pin.OUT)
_motor1_b:Pin = Pin(12, Pin.OUT)
_motor2_a:Pin = Pin(11, Pin.OUT)
_motor2_b:Pin = Pin(10, Pin.OUT)
_motor3_a:Pin = Pin(9, Pin.OUT)
_motor3_b:Pin = Pin(8, Pin.OUT)
_motor4_a:Pin = Pin(7, Pin.OUT)
_motor4_b:Pin = Pin(6, Pin.OUT)

_motor1_pwm:PWM = PWM(Pin(14))
_motor2_pwm:PWM = PWM(Pin(15))
_motor3_pwm:PWM = PWM(Pin(16))
_motor4_pwm:PWM = PWM(Pin(17))

_motor1_pwm.freq(1000)
_motor2_pwm.freq(1000)
_motor3_pwm.freq(1000)
_motor4_pwm.freq(1000)

modes:dict[str, str] = {
    '4' : '4WD',
    '1' : 'Single',
    '5' : 'Auto'}

motor_commands:dict[str, int] = {
    'j' : 1,
    'k' : 2,
    'n' : 3,
    'm' : 4}

commands_1:dict[str, str] = {
    'f' : 'forward',
    'b' : 'backward',
    's' : 'stop'}

commands_4:dict[str, str] = {
    'f' : 'forward',
    'l' : 'move_left',
    'b' : 'backward',
    'r' : 'move_right',
    'o' : 'turn_left',
    'p' : 'turn_right',
    's' : 'stop'}

manual_direction:dict[str, list[bool]] = {
    'forward'  : [True, False],
    'backward' : [False, True],
    'stop'     : [False, False]}

direction_list:dict[str, list[bool]] = {
    'forward'   :[True, False,
                  True, False,
                  True, False,
                  True, False],

    'backward'  :[False, True,
                  False, True,
                  False, True,
                  False, True],

    'turn_right':[True, False,
                  False, True,
                  True, False,
                  False, True,],

    'turn_left' :[False, True,
                  True, False,
                  False, True,
                  True, False],

    'move_left':[True, False,
                  False, True,
                  False, True,
                  True, False],

    'move_right':[False, True,
                  True, False,
                  True, False,
                  False, True],

    'stop'      :[False, False,
                  False, False,
                  False, False,
                  False, False]}

pwm_speed:dict[str, list[int]] = {
    'forward'    : [100, 100, 100, 100],
    'backward'   : [100, 100, 100, 100],
    'turn_right' : [100, 100, 100, 100],
    'turn_left'  : [100, 100, 100, 100],
    'move_right' : [100, 100, 100, 100],
    'move_left'  : [100, 100, 100, 100],
    'stop'       : [  0,   0,   0,   0]}

motor_box:list[Pin] = [
    _motor1_a, _motor1_b,
    _motor2_a, _motor2_b,
    _motor3_a, _motor3_b,
    _motor4_a, _motor4_b]

pwm_box:list[PWM] = [
    _motor1_pwm,
    _motor2_pwm,
    _motor3_pwm,
    _motor4_pwm]

mapping:dict[str, int] = {
    'left_over'     : 80,
    'left_margine'  : 120,
    'right_margine' : 200,
    'right_over'    : 240}

distances:dict[str, int] = {
    'close'         : 30000,
    'close_margine' : 20000,
    'far_margine'   : 10000,
    'far'           : 8000}