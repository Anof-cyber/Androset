import argparse
from OpenSSL import crypto
import os
from hashlib import md5
import subprocess
import sys


def convert_and_push_ca_cert_to_android(ca_cert_file,ip,port):
    # Set the Android mobile certificate file path
    android_cert_file = "android.pem"
    

    # Read the CA certificate file and convert it to PEM format using pyOpenSSL
    with open(ca_cert_file, "rb") as f:
        ca_cert_data = f.read()
    ca_cert = crypto.load_certificate(crypto.FILETYPE_ASN1, ca_cert_data)
    
    with open(android_cert_file, "wb") as f:
        f.write(crypto.dump_certificate(crypto.FILETYPE_PEM, ca_cert))
        
        
        
    with open(android_cert_file, "rb") as f:
        pemdata = f.read()  


    cert = crypto.load_certificate(crypto.FILETYPE_PEM, pemdata)
    
    ca_obj = crypto.load_certificate(crypto.FILETYPE_PEM, pemdata)
    md = md5(ca_obj.get_subject().der()).digest()
    ret = (md[0] | (md[1] << 8) | (md[2] << 16) | md[3] << 24)
    ca_file_hash = hex(ret).lstrip('0x')

    
    
    androidfilename = str(ca_file_hash) + ".0"
    try:
        os.remove(androidfilename)
    except OSError:
        pass
    os.rename(android_cert_file, str(ca_file_hash) + ".0")
    android_cert_dir = "/system/etc/security/cacerts/"
    pushedpfile = "/sdcard/" + androidfilename
    filetochangepermission = android_cert_dir + androidfilename
    
    output = subprocess.check_output(["adb", "devices"])
    
    
    lines = output.decode("utf-8").strip().split("\n")
    serials = [line.split("\t")[0] for line in lines[1:]]
    try:
        serial = serials[0]
    except IndexError:
        print("Unable to find devices")
    
    
    if serials:
        print("ADB device is connected")
    else:
        print("Device is not connected Tying to connect")
        output = subprocess.check_output(["adb", "connect", f"{ip}:{port}"])
        if "connected to" in output.decode("utf-8"):
            print("Successfully connected to ADB device")
            output = subprocess.check_output(["adb", "devices"])
            lines = output.decode("utf-8").strip().split("\n")
            serials = [line.split("\t")[0] for line in lines[1:]]
            try:
                serial = serials[0]
            except IndexError:
                print("Unable to find devices")
                sys.exit(1)
        else:
            print("Failed to connect to ADB device")
            sys.exit(1)
    
    
    
    output = subprocess.check_output(["adb", "-s", serial, "root"])
    output = subprocess.check_output(["adb", "-s", serial, "remount"])
    output = subprocess.check_output(["adb", "-s", serial, "push", androidfilename, '/sdcard/'])
    output = subprocess.check_output(["adb", "-s", serial, "shell", "mv", pushedpfile, android_cert_dir])
    output = subprocess.check_output(["adb", "-s", serial, "shell", "chmod", "644",filetochangepermission])
    
    # Print a success message
    print("Successfully converted and pushed the Android mobile certificate to the device and set the correct permissions.")

# Parse the user arguments
parser = argparse.ArgumentParser(description="Convert and push a CA certificate to Android.")
parser.add_argument("--cert", help="Path to the CA certificate file.", required=True)
parser.add_argument("--ip", default="127.0.0.1", help="IP address")
parser.add_argument("--port", default=5555, type=int, help="Port number")
args = parser.parse_args()

# Use the script to convert and push the Android mobile certificate to the device
convert_and_push_ca_cert_to_android(args.cert,args.ip,args.port)
