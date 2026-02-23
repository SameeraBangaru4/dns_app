import socket
import os

DNS_DB_File = "dns_records.txt"

UDP_PORT = 53533
def save_record(name, value, record_type, ttl):
    with open(DNS_DB_File, "a") as f:
        f.write(f"{record_type},{name},{value},{ttl}\n")

def lookup_record(name, record_type):

    if not os.path.exists(DNS_DB_File):
        return None
    
    with open(DNS_DB_File, "r") as f:
        for line in f:
            r_type, r_name, r_value, r_ttl = line.strip().split(',')
            print(f"r_type: {r_type}, r_name: {r_name}, r_value: {r_value}, r_ttl: {r_ttl}")
            if r_type == record_type and r_name == name:
                return r_value, r_ttl
    return None

def parse_message(message):
    lines = message.strip().split("\n")
    data = {}
    for l in lines:
        key, value = l.split("=")
        data[key.strip()] = value.strip()
    return data
def start_as():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("", UDP_PORT))

    print(f"Authoritative Server running on UDP Port {UDP_PORT}")

    while True:
        message, addr = sock.recvfrom(1024)
        message = message.decode()
        print("\nReceived")
        print(message)

        data = parse_message(message)

        if "VALUE" in data:
            save_record(
                name= data["NAME"],
                value= data["VALUE"],
                record_type= data["TYPE"],
                ttl= data["TTL"]
                )
            print("Record Registered")

        else:
            result = lookup_record(name= data["NAME"], record_type=data["TYPE"])
            
            if result:
                value, ttl = result
                response = f"TYPE={data['TYPE']}\nNAME={data['NAME']}\nVALUE={value}\nTTL={ttl}"
                sock.sendto(response.encode(), addr)
                print("Response Sent")
            else:
                print("Record not found")

if __name__ == "__main__":
    start_as()