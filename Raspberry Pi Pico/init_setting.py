from config import *

def _pwm_control(pwm_pin:PWM, speed:int) -> None:
    u16_pwm = round(speed / 100 * 65535)
    pwm_pin.duty_u16(u16_pwm)
    
def controler_4WD(motor_box:list[Pin], direction:str, pwm_box:list[PWM], manual_pwm:list[int] = []) -> None:
    if manual_pwm == []: manual_pwm = pwm_speed[direction]
    dl:list[bool] = direction_list[direction]
    
    # print(f'direction = {direction}')
    # for address_count in range(4):
    #     x2 = address_count * 2
    #     print(f'motor{address_count + 1} {dl[x2:x2 + 2]}')
    
    for motor_pin, dir in zip(motor_box, dl):
        motor_pin.value(dir)
    
    for pwm, speed in zip(enumerate(pwm_box, 1), manual_pwm):
        # number = pwm[0]
        # print(f'motor{number} {speed}% PWM duty')
        _pwm_control(pwm[1], speed)
    
def controler_Single(motor_number:int, direction:str, speed:int = 100) -> None:
    # print(f'motor {motor_number}, direction = {direction}, speed = {speed}% PWM duty')
    motor_index = motor_number * 2 - 2
    manual_box  = motor_box[motor_index:motor_index + 2]
    
    for motor_pin, dir in zip(manual_box, manual_direction[direction]): motor_pin.value(dir)
    
    _pwm_control(pwm_box[motor_number - 1], speed)

def read_hc06(hc06:UART) -> str: # type: ignore
    if hc06.any():
        encode_command = hc06.read(1)
        command        = encode_command.decode() # type: ignore
        
        return command

def write_hc06(uart:UART, command:str) -> None:
    # print(f"send data {command}")
    uart.write(command) # type: ignore

# pixy camera output resolution 320 px x 200 px
def direction_check(xy:list[int], distance:int, bstate:str) -> str:
    x    :int = xy[0]
    state:str = bstate
    
    if mapping['left_margine'] < x < mapping['right_margine'] and distances['far_margine'] < distance < distances['close_margine']: state = commands_4['s']
    elif x < mapping['left_over']                                                                                                 : state = commands_4['p']
    elif x > mapping['right_over']                                                                                                : state = commands_4['o']
    elif distance < distances['far']                                                                                              : state = commands_4['f']
    elif distance > distances['close']                                                                                            : state = commands_4['b']

    return state

def auto_drive(bstate:str, xywh:list[int]) -> str:
    center  :list[int] = xywh[1:3]
    distance:int       = xywh[3] * xywh[4]
    state   :str       = direction_check(center, distance, bstate)
    
    print(f'xywh = [{xywh[0]:>3d}, {xywh[1]:>3d}, {xywh[2]:>3d}, {xywh[3]:>3d}, {xywh[4]:>3d}], center = [{center[0]:>3d}, {center[1]:>3d}], distance = {distance:>5d}, state = {state:10s}')
    write_hc06(hc06, f'xywh = [{xywh[0]:>3d}, {xywh[1]:>3d}, {xywh[2]:>3d}, {xywh[3]:>3d}, {xywh[4]:>3d}], center = [{center[0]:>3d}, {center[1]:>3d}], distance = {distance:>5d}, state = {state:10s}')

    controler_4WD(motor_box, state, pwm_box)
    return state