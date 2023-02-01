import time
import os
import databaseAttuatori
import uuid
import random
import json
import asyncio
import subprocess

class HomeAssistant():
    def __init__(self) -> None:
        self.dbm = databaseAttuatori.configurazione_database()

        

    def GeneraConfig(self) -> dict:
        
        initconfig = """
# Loads default set of integrations. Do not remove.
default_config:

# Text to speech
tts:
- platform: google_translate

automation: !include automations.yaml
script: !include scripts.yaml
scene: !include scenes.yaml\n\n\n\n\n\n


"""
        
        initconfig = """
mqtt:
"""
        
        orderquery = list()
        switchorderquery = list()
        totord = list()

        #ordina swich e gruppi insieme
        query = self.dbm.RICHIESTA_TUTTI_ATTUATORI()
        for q in query:
            if(q['tipo_attuatore'] == 'on_off'):
                switchorderquery.append(q)
            elif(q['tipo_attuatore'] == 'gruppi'):
                pass
            else:
                orderquery.append(q)

        query = self.dbm.RICHIESTA_TUTTI_ATTUATORI()
        for q in query:
            if(q['tipo_attuatore'] == 'gruppi'):
                switchorderquery.append(q)

        totord = switchorderquery + orderquery




        deviceconfig = ""
        deviceconfig = deviceconfig + initconfig

        devicetipo = ""
        switch_start = False
        dimmer_start = False
        sensori_temperatura_start = False
        termostati_start = False
        serrande_start = False
        gruppi_start = False
        serrature_start = False



        query = totord #self.dbm.RICHIESTA_TUTTI_ATTUATORI()
        for q in query:
            if(q['tipo_attuatore'] == 'on_off'):
                nome = q['nome_attuatore']

                if(switch_start==False):
                    switch_start=True
                    devicetipo = "  switch:\n"
                else:
                    devicetipo = ""

                devicetemp = '\
  - unique_id: ' + nome.replace(" ","")  + '\n\
    name: "' + nome + '"\n\
    command_topic: "/scsshield/device/'+ nome +'/switch"\n\
    state_topic: "/scsshield/device/'+ nome +'/status"\n\
    payload_on: "on"\n\
    payload_off: "off"\n\
    state_on: "on"\n\
    state_off: "off"\n\n\
' 

                deviceconfig = deviceconfig + devicetipo + devicetemp
                
            elif(q['tipo_attuatore'] == 'dimmer'):
                nome = q['nome_attuatore']

                if(dimmer_start==False):
                    dimmer_start=True
                    devicetipo = "  #Dimmer\n  light: \n"
                else:
                    devicetipo = ""


                devicetemp = '\
  - unique_id: ' + nome.replace(" ","")  + '\n\
    name: "' + nome + '" \n\
    payload_on: "on" \n\
    payload_off: "off" \n\
    brightness_scale: "99" \n\
    brightness_state_topic: "/scsshield/device/'+ nome +'/status/percentuale" \n\
    brightness_command_topic: "/scsshield/device/'+ nome +'/dimmer" \n\
    state_topic: "/scsshield/device/' + nome + '/status" \n\
    command_topic: "/scsshield/device/'+ nome + '/dimmer" \n\
    optimistic: false \n\
    retain: true \n\n\
' 
                deviceconfig = deviceconfig + devicetipo + devicetemp


            elif(q['tipo_attuatore'] == 'sensori_temperatura'):
                nome = q['nome_attuatore']

                if(sensori_temperatura_start==False):
                    sensori_temperatura_start=True
                    devicetipo = "  #Sensore Temperatura\n  sensor: \n"
                else:
                    devicetipo = ""


                devicetemp = '\
  - unique_id: ' + nome.replace(" ","")  + '\n\
    name: "' + nome +'" \n\
    state_topic: "/scsshield/device/' + nome + '/status" \n\
    unit_of_measurement: "°C" \n\n\n\
' 
                deviceconfig = deviceconfig + devicetipo + devicetemp


            elif(q['tipo_attuatore'] == 'termostati'):
                nome = q['nome_attuatore']

                if(termostati_start==False):
                    termostati_start=True
                    devicetipo = "  #Termostato\n  climate: \n"
                else:
                    devicetipo = ""



                devicetemp = '\
  - unique_id: ' + nome.replace(" ","")  + '\n\
    name: "'+ nome +'" \n\
    modes: \n\
      - "off" \n\
      - "cool" \n\
      - "heat" \n\
    swing_modes: \n\
      - "on" \n\
      - "off" \n\
    mode_command_topic: "/scsshield/device/'+ nome +'/set_modalita_termostato" \n\
    mode_command_template: >- \n\
     {% set values = { "auto":"0", "heat":"estate",  "cool":"inverno", "off":"off"} %} \n\
     {{ values[value] if value in values.keys() else "4" }} \n\
    temperature_command_topic: "/scsshield/device/'+ nome +'/set_temp_termostato" \n\
    mode_state_topic: "/scsshield/device/'+ nome +'/modalita_termostato_impostata" \n\
    mode_state_template: >- \n\
     {% set values = { "auto":"0", "ESTATE":"cool",  "INVERNO":"heat", "OFF":"off"} %} \n\
     {{ values[value] if value in values.keys() else "4" }} \n\
    temperature_state_topic: "/scsshield/device/'+ nome +'/temperatura_termostato_impostata" \n\
    precision: 1.0 \n\n\n\
'
                deviceconfig = deviceconfig + devicetipo + devicetemp


            elif(q['tipo_attuatore'] == 'serrande_tapparelle'):
                nome = q['nome_attuatore']

                if(serrande_start==False):
                    serrande_start=True
                    devicetipo = "  #Serrande\n  cover: \n"
                else:
                    devicetipo = ""


                devicetemp = '\
  - unique_id: ' + nome.replace(" ","")  + '\n\
    device_class: shutter \n\
    name: "'+ nome +'" \n\
    command_topic: "/scsshield/device/'+ nome +'/percentuale" \n\
    state_topic:  "/scsshield/device/'+ nome +'/status" \n\
    position_topic: "/scsshield/device/'+ nome +'/status" \n\
    set_position_topic: "/scsshield/device/'+ nome +'/percentuale" \n\
    value_template: "{{ value_json.position }}" \n\
    position_closed: 0 \n\
    position_open: 100 \n\
    payload_open: 100 \n\
    payload_close: 0 \n\
    #payload_stop: (0) \n\n\n\
'

                deviceconfig = deviceconfig + devicetipo + devicetemp


            elif(q['tipo_attuatore'] == 'gruppi'):
                nome = q['nome_attuatore']

                if(switch_start==False):
                    switch_start=True
                    devicetipo = "  switch: \n"
                else:
                    devicetipo = ""



                devicetemp = '\
  - unique_id: ' + nome.replace(" ","")  + '\n\
    name: "' + nome + '" \n\
    command_topic: "/scsshield/device/'+ nome +'/switch" \n\
    state_topic: "/scsshield/device/'+ nome +'/status" \n\
    payload_on: "on" \n\
    payload_off: "off" \n\
    state_on: "on" \n\
    state_off: "off" \n\n\n\
' 
                deviceconfig = deviceconfig + devicetipo + devicetemp
        


            elif(q['tipo_attuatore'] == 'serrature'):
                nome = q['nome_attuatore']

                if(serrature_start==False):
                    serrature_start=True
                    devicetipo = "  #portone\n  lock: \n"
                else:
                    devicetipo = ""



                devicetemp = '\
  - unique_id: ' + nome.replace(" ","")  + '\n\
    name: "' + nome + '" \n\
    command_topic: "/scsshield/device/' + nome + '/sblocca/" \n\
    payload_unlock: "sblocca" \n\
    payload_open: "sblocca" \n\
    optimistic: false \n\
    qos: 1 \n\
    retain: true \n\n\n\
' 
                deviceconfig = deviceconfig + devicetipo + devicetemp
        





        return deviceconfig
  







    def main(self):
        print("main Home Assistant")
        node = HomeAssistant()
        js = node.GeneraConfig()

        print(js)
    


if __name__ == "__main__":    
    print("*****Home Assistant Config*****")
    
    node = HomeAssistant()
    js = node.GeneraConfig()
    print(js)
    