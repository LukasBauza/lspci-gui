'''
Data and commands that will be used for the GUI
'''

import subprocess

def command(command:str, input:str = None):
    command = command.split()
    
    data = subprocess.run(command, capture_output = True, text = True, input = input) 
    
    return data.stdout

def pipe(command1:str, command2:str):
    command1 = command1.split()
    command2 = command2.split()

    command = subprocess.run(command1, capture_output = True, text = True)
    command = command.stdout
    command = subprocess.run(command2, capture_output = True, text = True, input = command)

    return command.stdout

def index_get_paragragh(data:str, select:int):
    command = ['awk', '-v', 'RS=', '-v', 'ORS=', 'NR==' + str(select + 1)]

    paragraph = subprocess.run(command, capture_output = True, text = True, input = data)

    return paragraph.stdout

def word_get_paragraph(data:str, word:str):
    command = ['awk', '-v', 'RS=', f'/\\y{word}\\y/']
    paragraph = subprocess.run(command, capture_output = True, text = True, input = data)

    return paragraph.stdout

def word_get_line(data:str, word:str):
    command = ['grep', '-w', f'{word}']
    line = subprocess.run(command, capture_output = True, text = True, input = data)

    return line.stdout

devices = pipe('lspci -vmm', 'grep -w Device')
devices = devices.replace('Device:\t', '')
devices_list = devices.split('\n')
devices_list = list(filter(None, devices_list))    #Removes empty items in list.

slot = pipe('lspci -vvv', 'awk -v RS= {print$1}')
slot_list = slot.split('\n')
slot_list = list(filter(None, slot_list))

#Device specific commands
lspci_opd_name = ['lspci -v', 'lspci -vvv', 'lspci -nvmm', 'lspci -xxx']
#lspici_opd_device = list(map(lambda item: item + main.devices_selected, lspci_opd_name))
lspci_opd_out = [command(option) for option in lspci_opd_name]

#Non device specific commands
lspic_op_name  = ['lspci -tv']
lspic_op_out = [command(option) for option in lspic_op_name]

setpci_op_name = ['setpci --dumpregs']
