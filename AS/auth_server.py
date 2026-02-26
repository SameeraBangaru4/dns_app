import socket
import os

DNS_DB_File = "/AS/dns_records.txt"

UDP_PORT = 53533
def save_record(name, value, record_type, ttl):
    records = []
    record_exists = False

    # Create file if it doesn't exist
    if not os.path.exists(DNS_DB_File):
        open(DNS_DB_File, "w").close()

    # Read existing records
    with open(DNS_DB_File, "r") as f:
        for line in f:
            r_type, r_name, r_value, r_ttl = line.strip().split(",")

            if r_type == record_type and r_name == name:
                # Update existing record
                records.append(f"{record_type},{name},{value},{ttl}\n")
                record_exists = True
            else:
                records.append(line)

    # If record was not found, add it
    if not record_exists:
        records.append(f"{record_type},{name},{value},{ttl}\n")

    # Write back to file
    with open(DNS_DB_File, "w") as f:
        f.writelines(records)

    if record_exists:
        print("Record updated")
    else:
        print("Record added")

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
    sock.bind(("0.0.0.0", UDP_PORT))

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