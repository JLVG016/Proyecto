import socket
import serial
import threading
import sys

# === CONFIGURACIÓN ===
ESP32_IP = '192.168.4.1'  
TCP_PORT = 8080
PUERTO_COM_PYTHON = 'COM9' 
BAUD_RATE = 9600
# =====================

try:
    ser = serial.Serial(PUERTO_COM_PYTHON, BAUD_RATE)
    print(f"✅ Conectado a {PUERTO_COM_PYTHON}")
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ESP32_IP, TCP_PORT))
    print(f"✅ Conectado vía WiFi al ESP32 ({ESP32_IP})")
except Exception as e:
    print(f"❌ Error de conexión: {e}")
    sys.exit()

def recibir_de_tcp_y_enviar_a_serial():
    while True:
        try:
            datos = sock.recv(1024)
            if datos:
                print(f"⬅️ ESP32 RESPONDE: {datos}")
                ser.write(datos)
        except:
            break

def recibir_de_serial_y_enviar_a_tcp():
    while True:
        try:
            if ser.in_waiting > 0:
                datos = ser.read(ser.in_waiting)
                print(f"➡️ DELPHI ENVÍA: {datos}")
                sock.send(datos)
        except:
            break

t1 = threading.Thread(target=recibir_de_tcp_y_enviar_a_serial, daemon=True)
t2 = threading.Thread(target=recibir_de_serial_y_enviar_a_tcp, daemon=True)

t1.start()
t2.start()

print("🔍 Modo espía activado. Esperando datos...")
try:
    while True:
        pass 
except KeyboardInterrupt:
    print("\nCerrando conexiones...")
    ser.close()
    sock.close()