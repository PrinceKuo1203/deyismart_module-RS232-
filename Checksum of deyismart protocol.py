##################
# deyismart protocol tester
# Author : Prince Kuo
# Development history :
#     - 20220505 : Calculate checksum
import serial
import struct
from time import sleep

##################
# deyismart protocol content 
preamble_HB = 0x55
preamble_LB = 0xAA
#Length = 0x05
Address_and_data_of_01_sned_2_mdule = {
    'addr_01H_Module_status':0x01, 
        'len_01H_shade_motor_control' : 5,
        'data_01H_shade_motor_control':
            {'01H_Open':0x01, '02H_Close': 0x02, '03H_Stop': 0x03},
    
    'addr_02H_percentage_and_Angle_control':0x02,
        'len_02H_percentage_and_angle' : 6,
        'data_02H_percentage_and_angle': 
            {'Percentage_00':0x00, 'Percentage_25':0x19,  'Percentage_50':0x32, 'Percentage_75':0x4B, 'Percentage_100':0x64,
                'Angle_00': 0x00, 'Angle_45': 0x2D, 'Angle_90': 0x5A, 'Angle_135': 0x87, 'Angle_180': 0xB4},          

    'addr_10H_Change_device_type':0x10, 
        'len_10H_Change_device_type' : 5,
        'data_10H_Change_device_type':
            {'20H_Curtain':0x20, '30H_Venetian_blinds': 0x30},
    }

Address_and_data_of_02H_Read_from_module = {
    'addr_00H_read_usually_info':0x00, 
        'len_00H_read_usually_info': 4,

    'addr_01H_shade_motor_status':0x01, 
        'len_01H_shade_motor_status': 4,    

    'addr_02H_shade_motor_location_percentage':0x02, 
        'len_02H_shade_motor_location_percentage': 4,   

    'addr_03H_shade_motor_angle':0x03, 
        'len_03H_shade_motor_angle': 4,                

    'addr_04H_has_main_process_or_not':0x04, 
        'len_04H_has_main_process_or_not': 4,     

    'addr_05H_manual_pull_enable_or_not':0x05, 
        'len_05H_manual_pull_enable_or_not': 4,     

    'addr_06H_shade_motor_direction':0x06, 
        'len_06H_shade_motor_direction': 4,     

    'addr_07H_weak_electric_switch_type':0x07, 
        'len_07H_weak_electric_switch_type': 4,          
    
    'addr_08H_strong_electric_switch_type':0x08, 
        'len_08H_strong_electric_switch_type': 4,    

    'addr_09H_enable_edge_status':0x09, 
        'len_09H_Enable_edge_status': 4,    

    'addr_0AH_disable_edge_status':0x0A, 
        'len_0AH_Disable_edge_status': 4,            

    'addr_0BH_3rd_thread_point_set_or_not':0x0B, 
        'len_0BH_3rd_thread_point_set_or_not': 4,   

    'addr_0CH_angle_value':0x0C, 
        'len_0CH_Angle_value': 4,    

    'addr_0DH_angle_direction':0x0D, 
        'len_0DH_Angle_direction': 4,            

    'addr_0FH_shade_motor_jamming_or_not':0x0F, 
        'len_0FH_shade_motor_jamming_or_not': 4,             

    'addr_25H_battery_capacity':0x25, 
        'len_25H_battery_capacity': 4,  

    'addr_F0H_shade_motor_type':0xF0, 
        'len_F0H_shade_motor_type': 4, 

    'addr_F1H_shade_motor_model':0xF1, 
        'len_F1H_shade_motor_model': 4,  

    'addr_F2H_shade_motor_FW_VER':0xF2, 
        'len_F2H_shade_motor_FW_VER': 4,          
    }

deyi_protocol = {'01H_send_2_module':0x01, '01H_send_2_module_Address_and_Data' : Address_and_data_of_01_sned_2_mdule, 
                         
                 '02H_Read_from_module':0x02, '02H_Read_from_module_Address_and_Data' : Address_and_data_of_02H_Read_from_module,
                               
                 '03H_Module_auto_notify': 0x03}   

command_list = {
##############################
# 01_XXH_SEND_COMMAND         
##############################
    '01_01H_open_shade':
            [preamble_HB, 
            preamble_LB, 
            deyi_protocol['01H_send_2_module_Address_and_Data']['len_01H_shade_motor_control'], 
            deyi_protocol['01H_send_2_module'], 
            deyi_protocol['01H_send_2_module_Address_and_Data']['addr_01H_Module_status'],
            deyi_protocol['01H_send_2_module_Address_and_Data']['data_01H_shade_motor_control']['01H_Open']],
    '01_02H_close_shade':
            [preamble_HB, 
            preamble_LB, 
            deyi_protocol['01H_send_2_module_Address_and_Data']['len_01H_shade_motor_control'], 
            deyi_protocol['01H_send_2_module'], 
            deyi_protocol['01H_send_2_module_Address_and_Data']['addr_01H_Module_status'],
            deyi_protocol['01H_send_2_module_Address_and_Data']['data_01H_shade_motor_control']['02H_Close']],
    '01_03H_stop_shade':
            [preamble_HB, 
            preamble_LB, 
            deyi_protocol['01H_send_2_module_Address_and_Data']['len_01H_shade_motor_control'], 
            deyi_protocol['01H_send_2_module'], 
            deyi_protocol['01H_send_2_module_Address_and_Data']['addr_01H_Module_status'],
            deyi_protocol['01H_send_2_module_Address_and_Data']['data_01H_shade_motor_control']['03H_Stop']],
    '01_04H_Percentage_50_Angle_90':
            [preamble_HB, 
            preamble_LB, 
            deyi_protocol['01H_send_2_module_Address_and_Data']['len_02H_percentage_and_angle'], 
            deyi_protocol['01H_send_2_module'], 
            deyi_protocol['01H_send_2_module_Address_and_Data']['addr_02H_percentage_and_Angle_control'],
            deyi_protocol['01H_send_2_module_Address_and_Data']['data_02H_percentage_and_angle']['Percentage_50'], 
            deyi_protocol['01H_send_2_module_Address_and_Data']['data_02H_percentage_and_angle']['Angle_90']], 
    # '01_05H_Percentage_50_Angle_180':

    # '01_06H_Percentage_100_Angle_90':
 
    # '01_07H_Percentage_100_Angle_180':

    '01_10H_Change_device_type':
            [preamble_HB, 
            preamble_LB, 
            deyi_protocol['01H_send_2_module_Address_and_Data']['len_10H_Change_device_type'], # len
            deyi_protocol['01H_send_2_module'],                                                 # function code
            deyi_protocol['01H_send_2_module_Address_and_Data']['addr_10H_Change_device_type'],      # address
            deyi_protocol['01H_send_2_module_Address_and_Data']['data_10H_Change_device_type']['20H_Curtain']],   # data

##############################
# 02_XXH_READ_COMMAND         
##############################     
    '02_00H_Read_usually_info':     
            [preamble_HB, 
            preamble_LB, 
            deyi_protocol['02H_Read_from_module_Address_and_Data']['len_00H_read_usually_info'],    # len
            deyi_protocol['02H_Read_from_module'],                                                  # function code
            deyi_protocol['02H_Read_from_module_Address_and_Data']['addr_00H_read_usually_info']],  # address

    '02_01H_shade_motor_status':     
            [preamble_HB, 
            preamble_LB, 
            deyi_protocol['02H_Read_from_module_Address_and_Data']['len_01H_shade_motor_status'],
            deyi_protocol['02H_Read_from_module'], 
            deyi_protocol['02H_Read_from_module_Address_and_Data']['addr_01H_shade_motor_status']],   

    '02_02H_shade_motor_location_percentage':     
            [preamble_HB, 
            preamble_LB, 
            deyi_protocol['02H_Read_from_module_Address_and_Data']['len_02H_shade_motor_location_percentage'],
            deyi_protocol['02H_Read_from_module'], 
            deyi_protocol['02H_Read_from_module_Address_and_Data']['addr_02H_shade_motor_location_percentage']],            

    '02_03H_shade_motor_angle':     
            [preamble_HB, 
            preamble_LB, 
            deyi_protocol['02H_Read_from_module_Address_and_Data']['len_03H_shade_motor_angle'],
            deyi_protocol['02H_Read_from_module'], 
            deyi_protocol['02H_Read_from_module_Address_and_Data']['addr_03H_shade_motor_angle']],            

    '02_04H_has_main_process_or_not':     
            [preamble_HB, 
            preamble_LB, 
            deyi_protocol['02H_Read_from_module_Address_and_Data']['len_04H_has_main_process_or_not'],
            deyi_protocol['02H_Read_from_module'], 
            deyi_protocol['02H_Read_from_module_Address_and_Data']['addr_04H_has_main_process_or_not']],            

    '02_05H_manual_pull_enable_or_not':     
            [preamble_HB, 
            preamble_LB, 
            deyi_protocol['02H_Read_from_module_Address_and_Data']['len_05H_manual_pull_enable_or_not'],
            deyi_protocol['02H_Read_from_module'], 
            deyi_protocol['02H_Read_from_module_Address_and_Data']['addr_05H_manual_pull_enable_or_not']],            

    '02_06H_shade_motor_direction':     
            [preamble_HB, 
            preamble_LB, 
            deyi_protocol['02H_Read_from_module_Address_and_Data']['len_06H_shade_motor_direction'],
            deyi_protocol['02H_Read_from_module'], 
            deyi_protocol['02H_Read_from_module_Address_and_Data']['addr_06H_shade_motor_direction']],            

    '02_07H_weak_electric_switch_type':     
            [preamble_HB, 
            preamble_LB, 
            deyi_protocol['02H_Read_from_module_Address_and_Data']['len_07H_weak_electric_switch_type'],
            deyi_protocol['02H_Read_from_module'], 
            deyi_protocol['02H_Read_from_module_Address_and_Data']['addr_07H_weak_electric_switch_type']],            

    '02_08H_strong_electric_switch_type':     
            [preamble_HB, 
            preamble_LB, 
            deyi_protocol['02H_Read_from_module_Address_and_Data']['len_08H_strong_electric_switch_type'],
            deyi_protocol['02H_Read_from_module'], 
            deyi_protocol['02H_Read_from_module_Address_and_Data']['addr_08H_strong_electric_switch_type']],            

    '02_09H_enable_edge_status':     
            [preamble_HB, 
            preamble_LB, 
            deyi_protocol['02H_Read_from_module_Address_and_Data']['len_09H_Enable_edge_status'],
            deyi_protocol['02H_Read_from_module'], 
            deyi_protocol['02H_Read_from_module_Address_and_Data']['addr_09H_enable_edge_status']],            

    '02_0AH_disable_edge_status':     
            [preamble_HB, 
            preamble_LB, 
            deyi_protocol['02H_Read_from_module_Address_and_Data']['len_0AH_Disable_edge_status'],
            deyi_protocol['02H_Read_from_module'], 
            deyi_protocol['02H_Read_from_module_Address_and_Data']['addr_0AH_disable_edge_status']],            

    '02_0BH_3rd_thread_point_set_or_not':     
            [preamble_HB, 
            preamble_LB, 
            deyi_protocol['02H_Read_from_module_Address_and_Data']['len_0BH_3rd_thread_point_set_or_not'],
            deyi_protocol['02H_Read_from_module'], 
            deyi_protocol['02H_Read_from_module_Address_and_Data']['addr_0BH_3rd_thread_point_set_or_not']],            

    '02_0CH_angle_value':     
            [preamble_HB, 
            preamble_LB, 
            deyi_protocol['02H_Read_from_module_Address_and_Data']['len_0CH_Angle_value'],
            deyi_protocol['02H_Read_from_module'], 
            deyi_protocol['02H_Read_from_module_Address_and_Data']['addr_0CH_angle_value']],            

    '02_0DH_angle_direction':     
            [preamble_HB, 
            preamble_LB, 
            deyi_protocol['02H_Read_from_module_Address_and_Data']['len_0DH_Angle_direction'],
            deyi_protocol['02H_Read_from_module'], 
            deyi_protocol['02H_Read_from_module_Address_and_Data']['addr_0DH_angle_direction']],            

    '02_0FH_shade_motor_jamming_or_not':     
            [preamble_HB, 
            preamble_LB, 
            deyi_protocol['02H_Read_from_module_Address_and_Data']['len_0FH_shade_motor_jamming_or_not'],
            deyi_protocol['02H_Read_from_module'], 
            deyi_protocol['02H_Read_from_module_Address_and_Data']['addr_0FH_shade_motor_jamming_or_not']],            

    '02_25H_battery_capacity':     
            [preamble_HB, 
            preamble_LB, 
            deyi_protocol['02H_Read_from_module_Address_and_Data']['len_25H_battery_capacity'],
            deyi_protocol['02H_Read_from_module'], 
            deyi_protocol['02H_Read_from_module_Address_and_Data']['addr_25H_battery_capacity']],            

    '02_F0H_shade_motor_type':     
            [preamble_HB, 
            preamble_LB, 
            deyi_protocol['02H_Read_from_module_Address_and_Data']['len_F0H_shade_motor_type'],
            deyi_protocol['02H_Read_from_module'], 
            deyi_protocol['02H_Read_from_module_Address_and_Data']['addr_F0H_shade_motor_type']],            

    '02_F1H_shade_motor_model':     
            [preamble_HB, 
            preamble_LB, 
            deyi_protocol['02H_Read_from_module_Address_and_Data']['len_F1H_shade_motor_model'],
            deyi_protocol['02H_Read_from_module'], 
            deyi_protocol['02H_Read_from_module_Address_and_Data']['addr_F1H_shade_motor_model']],            

    '02_F2H_shade_motor_FW_VER':     
            [preamble_HB, 
            preamble_LB, 
            deyi_protocol['02H_Read_from_module_Address_and_Data']['len_F2H_shade_motor_FW_VER'],
            deyi_protocol['02H_Read_from_module'], 
            deyi_protocol['02H_Read_from_module_Address_and_Data']['addr_F2H_shade_motor_FW_VER']],            

}

return_len = {
##############################
# 01_XXH_SEND_COMMAND         
##############################
    '01_10H_Change_device_type': 15,    # 0x20????????? ?? ??0x30???????????? ?? ??0xFF?????????

##############################
# 02_XXH_READ_COMMAND         
##############################    
    '02_00H_Read_usually_info' : 23,    # 1st data : ?????????????????????0x01???????????? 0x02???????????? 0x03?????????
                                        # 2nd data : ????????????????????????0----100??? ??0xFF??????????????????????????????
                                        # 3rd data : ???????????????0----180??? ??0xFF???????????????????????????
                                        # 4th data : ??????????????????????????????0x00????????????????????????0x01????????????????????????
                                        # 5th data : ???????????????0x00?????????????????? 0x01
                                        # 6th data : ???????????????0x01???????????????0x02????????????
                                        # 7th data : ????????????????????????0x00 ?? ?? ??????????????????:0x01
                                        # 8th data : ???????????????0----100??????????????????????????????
                                        # 9th data : 0x00?????????????????????????????????
 
    '02_01H_shade_motor_status' : 15,   # byte[0] : 0x01???????????? 0x02???????????? 0x03?????????

    '02_02H_shade_motor_location_percentage' : 15,   # byte[0] : 0----100??? 0xFF??????????????????????????????
     
    '02_03H_shade_motor_angle' : 15,   # byte[0] :??0----180??? 0xFF???????????????????????????

    '02_04H_has_main_process_or_not' : 15,   # byte[0] : 0x00????????????????????????0x01????????????????????????

    '02_05H_manual_pull_enable_or_not' : 14,   # byte[0] : 0x01???????????????????????? 0x00????????????????????????

    '02_06H_shade_motor_direction' : 15,   # byte[0] : 0x01????????????????????????0x02?????????????????????
     
    '02_07H_weak_electric_switch_type' : 14,   # byte[0] : 0x01??????????????????????????? ?? 0x02??????????????????????????????   0x03???DC246???????????????????????? 0x04?????????????????????

    '02_08H_strong_electric_switch_type' : 14,   # byte[0] : 0x01??????????????????????????????   0x02???????????????????????????????????????   0x03???????????????????????????

    '02_09H_enable_edge_status' : 14,   # byte[0] : 0x01????????????????????????????????? ?? ??0x00?????????????????????????????????

    '02_0AH_disable_edge_status' : 14,   # byte[0] : 0x01????????????????????????????????? ?? ??0x00?????????????????????????????????
     
    '02_0BH_3rd_thread_point_set_or_not' : 14,   # byte[0] : 0x00??????????????? ?? ??0x01????????????

    '02_0CH_angle_value' : 14,   # byte[0] : 0x00----0xFF

    '02_0DH_angle_direction' : 14,   # byte[0] : 0x01????????????????????????0x02????????????????????????

    '02_0FH_shade_motor_jamming_or_not' : 15,   # byte[0] : 0x00:??????????????? ?? ?? ??0x01:????????????
     
    '02_25H_battery_capacity' : 16,   # byte[0] : 0x00?????????????????????????????????  0x01????????????????????????  
                                      # Byte[1]???0----100??????????????????????????????

    '02_F0H_shade_motor_type' : 14,   # byte[0] : 0x10????????????  0x20?????????  0x30????????????

    '02_F1H_shade_motor_model' : 22,   

    '02_F2H_shade_motor_FW_VER' : 16,   
}
##############################################
# 0x01 DK board -> deyismart module
##############################################
# command_str='01_01H_open_shade'
# command_str='01_02H_close_shade'
# command_str='01_03H_stop_shade'
# command_str='01_04H_Percentage_50_Angle_90'
# command_str='01_05H_Percentage_50_Angle_180'
# command_str='01_06H_Percentage_100_Angle_90'
# command_str='01_07H_Percentage_100_Angle_180'
# command_str='01_10H_Change_device_type'


##############################################
# 0x02 DK board <- deyismart module
##############################################
command_str='02_00H_Read_usually_info'            # 03 ?????????????????????0x01???????????? 0x02???????????? 0x03?????????
                                                    # ff ????????????????????????0----100??? ??0xFF??????????????????????????????
                                                    # 00 ???????????????0----180??? ??0xFF???????????????????????????
                                                    # 00 ??????????????????????????????0x00????????????????????????0x01????????????????????????
                                                    # 00 ???????????????0x00?????????????????? 0x01
                                                    # 01 ???????????????0x01???????????????0x02????????????
                                                    # 00 ????????????????????????0x00 ?? ?? ??????????????????:0x01
                                                    # 50 ???????????????0----100???????????????????????????
                                                    # 00 0x00?????????????????????????????????
                                                     
# command_str='02_01H_shade_motor_status'           # 03 0x01???????????? 0x02???????????? 0x03????????? 
# command_str='02_02H_shade_motor_location_percentage'    # FF 0----100??? 0xFF??????????????????????????????
# command_str='02_03H_shade_motor_angle'            # 00 0----180??? 0xFF???????????????????????????
# command_str='02_04H_has_main_process_or_not'      # 00 0x00????????????????????????0x01????????????????????????
# command_str='02_05H_manual_pull_enable_or_not'    # !!!!!! no data in response field  ...PK 20220505+ !!!!!!
# command_str='02_06H_shade_motor_direction'        # 01 0x01?????????????????????  ...PK 20220505+
# command_str='02_07H_weak_electric_switch_type'    # !!!!!! no data in response field  ...PK 20220505+ !!!!!!
# command_str='02_08H_strong_electric_switch_type'  # !!!!!! no data in response field  ...PK 20220505+ !!!!!!
# command_str='02_09H_enable_edge_status'           # !!!!!! no data in response field  ...PK 20220505+ !!!!!!
# command_str='02_0AH_disable_edge_status'          # !!!!!! no data in response field  ...PK 20220505+ !!!!!!
# command_str='02_0BH_3rd_thread_point_set_or_not'  # !!!!!! no data in response field  ...PK 20220505+ !!!!!!
# command_str='02_0CH_angle_value'                  # !!!!!! no data in response field  ...PK 20220505+ !!!!!!
# command_str='02_0DH_angle_direction'              # !!!!!! no data in response field  ...PK 20220505+ !!!!!!
# command_str='02_0FH_shade_motor_jamming_or_not'   # 00 0x00:??????????????? ?? ?? ??0x01:????????????
# command_str='02_25H_battery_capacity'             # 00 0x00?????????????????????????????????0x01????????????????????????
                                                    # 50 0----100??????????????????????????????
# command_str='02_F0H_shade_motor_type'             # !!!!!! no data in response field  ...PK 20220505+ !!!!!!
# command_str='02_F1H_shade_motor_model'            # 00 
                                                    # 00 
                                                    # 00 
                                                    # 00 
                                                    # 50 'P'
                                                    # 0b 
                                                    # 57 'W'
                                                    # 4d 'M'
# command_str='02_F2H_shade_motor_FW_VER'           # 01 
                                                    # 00 

command = command_list[command_str]
read_len = return_len[command_str]


# Calculate checksum by command list
def Calculate_Checksum(temp_command):
    wCRCin=0xFFFF
    wCPoly=0x8005
    wChar=0
    
    for data in temp_command:
        wChar = data
        temp = (wChar<<8)
        # print('wChar : 0x{:08b}'.format(wChar))
        # print('temp : 0x{:08b}'.format(temp))
        # print('wChar : b{:08b}'.format(wChar) + '(0x{:02x})'.format(wChar) + ', ' + 'temp(wChar << 8) : b{:016b}'.format(temp) + '(0x{:04x})'.format(temp))
        # print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> wCRCin : b{:016b}'.format(wCRCin) + '(0x{:04x})'.format(wCRCin))
        wCRCin = wCRCin ^ temp
        # print('>>>>>>>>>>>>>>>>>>>>>>>>>>> do XOR wCRCin : b{:08b}'.format(wCRCin) + '(0x{:04x})'.format(wCRCin))
        for idx in range(8):
            if(wCRCin & 0x8000):
                # print('wCRCin & 0x8000 == true')
                wCRCin = (wCRCin << 1) & 0xFFFF
                # print('>>>>>>>>>>>>>>> wCRCin << 1: b{:016b}'.format(wCRCin) + '(0x{:04X})'.format(wCRCin))
                # print('>>>>>>>>>>>>>>> wCPoly << 1: b{:016b}'.format(wCPoly) + '(0x{:04X})'.format(wCPoly))
                wCRCin = wCRCin ^ wCPoly
                # print('>> wCRCin = wCRCin ^ wCPoly: b{:016b}'.format(wCRCin) + '(0x{:04X})'.format(wCRCin))
            else:
                # print('wCRCin & 0x8000 == false')
                wCRCin = (wCRCin << 1) & 0xFFFF
                # print('>>>>>>>>>>>>>>> wCRCin << 1: b{:016b}'.format(wCRCin) + '(0x{:04X})'.format(wCRCin))
    print('0x{:04X}'.format(wCRCin)) 
    return wCRCin        
    


command_content='Command = '    
send_cmd=''

# generate comand(command_content) and send command data(send_cmd)
for data in command:
    command_content = command_content + '{:02x} '.format(data)
    send_cmd = send_cmd + '{:02x}'.format(data)

# print command
print(command_content)

## Calculate checksum...PK20220505+
checksum = Calculate_Checksum(command)

# add checksum to send command data(send_cmd)
send_cmd = send_cmd + '{:04x}'.format(checksum)

from serial.tools import list_ports
port = list(list_ports.comports())
for p in port:
    print(p.device)

ser = serial.Serial(
    port='/dev/cu.usbserial-0001',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)

print(ser.isOpen())
message_bytes = bytes.fromhex(send_cmd)

ser.write(message_bytes)
s = ser.read(read_len)
print(s.hex(' '))
ser.close()