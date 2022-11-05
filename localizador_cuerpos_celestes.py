from tokenize import Double
import requests
from datetime import timedelta, datetime
import serial
import time
while True:
    try:
        arduino = serial.Serial('COM7', 9600)
        break
    except:
        print("esperando arduino...")
        time.sleep(3)
def write_read(x):
    arduino.write(bytes(x, 'utf-8'))
    time.sleep(0.05)
    print("datos enviados")


planetas_ids = {'10':'Sol', '199':'Mercurio', '299':'Venus', '301':'Luna', '499':'Marte', '599': 'Jupiter', '699': 'Saturno', '799': 'Urano', '899': 'Neptuno' }
menu = ""
for i in planetas_ids.keys():
    menu += i+") " + planetas_ids[i] + "\n"
#planetas_ids[i].append(requests.get(url).text.split("$$SOE")[1].split("$$EOE")[0].split("\n"))

menu += "01) Ajustar error\n02) Modo Manual\nElige un cuerpo celeste: "
error_x = 0
error_y = 0

while True:
    cuerpo_seleccionado = input(menu)
    if cuerpo_seleccionado == "01":
        error_x = int(input("Error horizontal: "))
        error_y = int(input("Error vertical: "))
        continue
    elif cuerpo_seleccionado == "02":
        grados_x = int(input("Grados x: ")) 
        grados_y = int(input("Grados y: "))
        grados_x = str((180 - int(float(grados_x)))+90+error_x)
        grados_y = str(-int(float(grados_y))+90+error_y) 
        write_read("x\n")
        time.sleep(2)
        write_read(grados_x)
        time.sleep(2)
        write_read("y\n")
        time.sleep(1)
        write_read(grados_y)
        continue

    fecha = str(datetime.now() - timedelta(hours=2)).split('.')[0].split(':')[0:2]
    fecha = ":".join(fecha) + ":00"
    print(fecha)
    try:
        url = "https://ssd.jpl.nasa.gov/api/horizons.api?format=text&MAKE_EPHEM=YES&COMMAND="+str(cuerpo_seleccionado)+"&EPHEM_TYPE=OBSERVER&CENTER=%27coord@399%27&COORD_TYPE=GEODETIC&SITE_COORD=%27-0.425360,39.654756,200%27&TLIST_TYPE=JD&TIME_TYPE=UT&TLIST=%27"+fecha+"%27&QUANTITIES=%274,5,9%27&REF_SYSTEM=%27ICRF%27&CAL_FORMAT=%27CAL%27&TIME_DIGITS=%27MINUTES%27&ANG_FORMAT=%27HMS%27&APPARENT=%27AIRLESS%27&RANGE_UNITS=%27AU%27&SUPPRESS_RANGE_RATE=%27NO%27&SKIP_DAYLT=%27NO%27&SOLAR_ELONG=%270,180%27&EXTRA_PREC=%27NO%27&CSV_FORMAT=%27NO%27&OBJ_DATA=%27YES%27"
        datos = requests.get(url).text.split("$$SOE")[1].split("$$EOE")[0].split("\n")[1].replace("  ", " ").replace("  ", " ")
        grados_x = datos.split(" ")[4]
        grados_y = datos.split(" ")[5]
        print(grados_x + " " + grados_y)
        if float(grados_y) < 0:
            print("No esta a la vista")
        else:
            grados_x = str((180 - int(float(grados_x)))+90+error_x)
            grados_y = str(-int(float(grados_y))+90+error_y)
            print(grados_x + ", "+ grados_y)
            write_read("x\n")
            time.sleep(2)
            write_read(grados_x)
            time.sleep(2)
            write_read("y\n")
            time.sleep(1)
            write_read(grados_y)
        
        
        
    except Exception as e:
        print(e)
        print("Valor incorrecto")
