from multiprocessing.connection import Connection
import sys
import socket
import logging
import json
from time import sleep
import os
import ssl
import threading

player_data = dict()
player_data['1']=dict(nomor=1, nama="dean henderson", posisi="kiper")
player_data['2']=dict(nomor=2, nama="luke shaw", posisi="bek kiri")
player_data['3']=dict(nomor=3, nama="aaron wan-bissaka", posisi="bek kanan")
player_data['4']=dict(nomor=4, nama="victor lindelof", posisi="bek tengah kanan")
player_data['5']=dict(nomor=5, nama="harry kane", posisi="penyerang")
player_data['6']=dict(nomor=6, nama="heung min son", posisi="sayap kiri")
player_data['7']=dict(nomor=7, nama="mohammed salah", posisi="sayap kanan")
player_data['8']=dict(nomor=8, nama="kevin de bruyne", posisi="gelandang serang")
player_data['9']=dict(nomor=9, nama="bernardo silva", posisi="gelandang serang")
player_data['10']=dict(nomor=10, nama="ngolo kante", posisi="gelandang bertahan")
player_data['11']=dict(nomor=11, nama="jorginho", posisi="gelandang bertahan cadangan")
player_data['12']=dict(nomor=12, nama="dejan kulusevski", posisi="sayap kanan cadangan")
player_data['13']=dict(nomor=13, nama="ruben dias", posisi="bek tengah kiri")
player_data['14']=dict(nomor=14, nama="joao cancelo", posisi="bek kiri cadangan")
player_data['15']=dict(nomor=15, nama="trent alexander arnold", posisi="bek kanan cadangan")
player_data['16']=dict(nomor=16, nama="antonio rudiger", posisi="bek cadangan")
player_data['17']=dict(nomor=17, nama="reece james", posisi="bek kiri cadangan")
player_data['18']=dict(nomor=18, nama="bruno fernandes", posisi="gelandang serang cadangan")
player_data['19']=dict(nomor=19, nama="cristiano ronaldo", posisi="penyerang cadangan")
player_data['20']=dict(nomor=20, nama="antonio conte", posisi="pelatih") 

def versi():
    return "versi 0.0.1"


def process_request(request_string):
    result = None
    try:
        player_number = request_string.strip()

        # logging.warning(f'Found data for {player_number}')
        result = player_data[player_number]
    except Exception:
        result = None

    return result




def serialized(data):
    serialized = json.dumps(data)

    # logging.warning('serializing data')
    # logging.warning(serialized)

    return serialized

def terimarequest(connection,socket_context):
    # print(type(connection))
    # print("Masuk terima request")
    connection = socket_context.wrap_socket(connection, server_side=True)
    data_received = ''
    while True:
        data = connection.recv(32)
        logging.warning(f'received {data}')
        if data:
            data_received += data.decode()
            if '\r\n\r\n' in data_received:
                result = process_request(data_received)
                # logging.warning(f'Result: {result}')
                sleep(0.1)

                result = serialized(result)
                result += '\r\n\r\n'
                connection.sendall(result.encode())
                break              

        else:
            # logging.warning(f'no more data from {client_address}')
            break

def jalankan_server(server_address):
    cert_location = os.getcwd() + '/certs/'
    socket_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    socket_context.load_cert_chain(
        certfile=cert_location + 'domain.crt',
        keyfile=cert_location + 'domain.key'
    )
    tugas = []
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    logging.warning(f'starting up on {server_address}')
    sock.bind(server_address)

    sock.listen(1000)

    while True:
        logging.warning('waiting for a connection')
        connection, client_address = sock.accept()
        logging.warning(f'Incoming connection from {client_address}')

        thread_sementara = threading.Thread(target=terimarequest, args=(connection,socket_context))
        thread_sementara.start()

        tugas.append(thread_sementara)
    

        
if __name__ == '__main__':
    try:
        jalankan_server(('0.0.0.0', 12000))
    except KeyboardInterrupt:
        logging.warning("Control-C: Program berhenti")
        exit(0)
    finally:
        logging.warning("seelsai")
