from init_setting import *
from time import sleep_ms

print('meca_while.py is running...')
print('pico LED is ON')

pico_LED.on()

mode  :str = '4WD'
state :str = 'stop'
bstate:str = 'stop'
delay :int = 20

def read_pixy(pixy:UART) -> list[int]: # type: ignore
    global delay
    
    byte_data:bytes = pixy.read(19) # type: ignore
    if byte_data:
        try:
            str_data :str       = byte_data.decode()
            xywh_list:list[str] = str_data[1:-1].split(',')
            xywh     :list[int] = [int(data) for data in xywh_list]
            
            if xywh[0] == 1: return xywh
            else           : return [2]
        except UnicodeError: return [3]
        except ValueError  : return [4]
    else:
        delay += 1
        return [0]

while True:
    command = read_hc06(hc06)
    
    if command in modes:
        mode = modes[command]
        continue
    
    elif command in motor_commands:
        motor = motor_commands[command]
        continue
    
    if mode == '4WD':
        if command in commands_4:
            state = commands_4[command]
            
        controler_4WD(motor_box, state, pwm_box)
        sleep_ms(1)
    
    elif mode == 'Auto':
        output = read_pixy(pixy)
        
        if   len(output) == 5: bstate = auto_drive(bstate, output)
        elif output == [2]   : 
            print('No object')
            controler_4WD(motor_box, 'stop', pwm_box)
        elif output == [3]   :
            print('Exception Data')
            write_hc06(hc06, 'Exception Data')
        elif output == [0]   :
            print('No data')
            write_hc06(hc06, 'No data')
        elif output == [4]   :
            print('Value error')
            write_hc06(hc06, 'Value Error')
        
        sleep_ms(delay)