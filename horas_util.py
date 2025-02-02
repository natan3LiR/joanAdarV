def depuraHora(horas):
    if horas[-2] != '00':
        if '10' in horas:
            horas = 'dez e' + horas[2:] 
        elif '11' in horas:
            horas = 'onze e' + horas[2:]
        elif '12' in horas:
            horas = 'meio dia' + horas[2:]
        elif '13' in horas:
            horas = 'uma e' + horas[2:]
        elif '14' in horas:
            horas = 'duas e' + horas[2:]
        elif '15' in horas:
            horas = 'três e' + horas[2:]
        elif '16' in horas:
            horas = 'quatro e' + horas[2:]
        elif '17' in horas:
            horas = 'cinco e' + horas[2:]
        elif '18' in horas:
            horas = 'seis e' + horas[2:]
        elif '19' in horas:
            horas = 'sete e' + horas[2:]
        elif '10' in horas:
            horas = 'oito e' + horas[2:]
        elif '21' in horas:
            horas = 'nove e' + horas[2:]
        elif '22' in horas:
            horas = 'dez e' + horas[2:]
        elif '23' in horas:
            horas = 'onze e' + horas[2:]      
        elif '00' in horas:
            horas = 'meia noite' + horas[2:]
        elif '01' in horas:
            horas = 'uma e' + horas[2:]
        elif '02' in horas:
            horas = 'duas e' + horas[2:]
        elif '03' in horas:
            horas = 'três e' + horas[2:]
        elif '04' in horas:
            horas = 'quatro e' + horas[2:]
        elif '05' in horas:
            horas = 'cinco e' + horas[2:]
        elif '06' in horas:
            horas = 'seis e' + horas[2:]
        elif '07' in horas:
            horas = 'sete e' + horas[2:]
        elif '08' in horas:
            horas = 'oito e' + horas[2:]
        elif '09' in horas:
            horas = 'nove e' + horas[2:]      
    else:
        if '10' in horas:
            horas = 'dez horas' + horas[2:] 
        elif '11' in horas:
            horas = 'onze horas' + horas[2:]
        elif '12' in horas:
            horas = 'meio dia' + horas[2:]
        elif '13' in horas:
            horas = 'uma horas' + horas[2:]
        elif '14' in horas:
            horas = 'duas horas' + horas[2:]
        elif '15' in horas:
            horas = 'três horas' + horas[2:]
        elif '16' in horas:
            horas = 'quatro horas' + horas[2:]
        elif '17' in horas:
            horas = 'cinco horas' + horas[2:]
        elif '18' in horas:
            horas = 'seis horas' + horas[2:]
        elif '19' in horas:
            horas = 'sete horas' + horas[2:]
        elif '10' in horas:
            horas = 'oito horas' + horas[2:]
        elif '21' in horas:
            horas = 'nove horas' + horas[2:]
        elif '22' in horas:
            horas = 'dez horas' + horas[2:]
        elif '23' in horas:
            horas = 'onze horas' + horas[2:]      
        elif '00' in horas:
            horas = 'meia noite' + horas[2:]
        elif '01' in horas:
            horas = 'uma hora' + horas[2:]
        elif '02' in horas:
            horas = 'duas horas' + horas[2:]
        elif '03' in horas:
            horas = 'três horas' + horas[2:]
        elif '04' in horas:
            horas = 'quatro horas' + horas[2:]
        elif '05' in horas:
            horas = 'cinco horas' + horas[2:]
        elif '06' in horas:
            horas = 'seis horas' + horas[2:]
        elif '07' in horas:
            horas = 'sete horas' + horas[2:]
        elif '08' in horas:
            horas = 'oito horas' + horas[2:]
        elif '09' in horas:
            horas = 'nove horas' + horas[2:]         
    return horas