import argparse
from OpenSSL import crypto
import os
from hashlib import md5
import subprocess
import sys
from termcolor import colored


def convert_and_push_ca_cert_to_android(ca_cert_file,adbip):
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
        print(colored("[+] Unable to find devices", "red"))

    
    if serials:
        print(colored("[+] ADB device is connected", "green"))
    else:
        serial = connect_adb(adbip)
       
    
    output = subprocess.check_output(["adb", "-s", serial, "root"])
    output = subprocess.check_output(["adb", "-s", serial, "remount"])
    output = subprocess.check_output(["adb", "-s", serial, "push", androidfilename, '/sdcard/'])
    output = subprocess.check_output(["adb", "-s", serial, "shell", "mv", pushedpfile, android_cert_dir])
    output = subprocess.check_output(["adb", "-s", serial, "shell", "chmod", "644",filetochangepermission])
    
    # Print a success message
    print(colored("[+] Successfully converted and pushed the Android mobile certificate to the device and set the correct permissions.", "green"))


def connect_adb(adbip):
    print(colored("[+] Device is not connected Tying to connect", "red"))
    output = subprocess.check_output(["adb", "connect", f"{adbip}"])
    if "connected to" in output.decode("utf-8"):
        print(colored("[+] Successfully connected to ADB device", "green"))
        output = subprocess.check_output(["adb", "devices"])
        lines = output.decode("utf-8").strip().split("\n")
        serials = [line.split("\t")[0] for line in lines[1:]]
        try:
            serial = serials[0]
            return serial
        except IndexError:
            print(colored("[+] Unable to find devices", "red"))
            sys.exit(1)
    else:
        print(colored("[+] Failed to connect to ADB device", "red"))
        sys.exit(1)

def android_to_burp(burpip,adbip):
    serial = connect_adb(adbip)
    output = subprocess.check_output(["adb", "-s", serial, "shell", "iptables", "-t", "nat","-A","OUTPUT","-p","tcp","--dport","80","-j","DNAT","--to-destination",burpip])
    output = subprocess.check_output(["adb", "-s", serial, "shell", "iptables", "-t", "nat","-A","OUTPUT","-p","tcp","--dport","443","-j","DNAT","--to-destination",burpip])

    print(colored("[+] Successfully Added Burp IP and PORT in android IP Table.", "green"))


def check_adb_installed():
    output = os.system("adb version")
    if output == 0:
        print(colored("[+] ADB Found.", "green"))
        return True
    else:
        print(colored("[+] ADB is not installed. Please install ADB and try again.", "red"))
        sys.exit(1)



# Parse the user arguments

#parser = argparse.ArgumentParser(description="Convert and push a CA certificate to Android.")
parser = argparse.ArgumentParser(
    usage="%(prog)s cert --cert <cert_file> \n %(prog)s burp --burpip 127.0.0.1:8080",
    description="Convert and push a CA certificate to Android or redirect Android traffic to Burp using IP Table.",
    formatter_class=argparse.RawDescriptionHelpFormatter
)



parser.add_argument("--cert", help="Path to the CA certificate file.", required=True)
parser.add_argument("--adbip", default="127.0.0.1:5555", help="ADB Connect IP and Port. default = 127.0.0.1:5555")
parser.add_argument("--burpip", default="127.0.0.1:8080", help="Redirect Android traffic from port 80 and 443 to Burp using IP Table. default = 127.0.0.1:8080")
#parser.add_argument("--port", default=5555, type=int, help="Port number")
parser.add_argument("command", nargs="?", default=None, help="adb or burp command")

args = parser.parse_args()



if args.command == "cert":
    check_adb_installed()
    convert_and_push_ca_cert_to_android(args.cert, args.adbip)

elif args.command == "burp":
    check_adb_installed()
    android_to_burp(args.burpip,args.adbip)

elif args.command in ["cert", "burp"]:
    if args.command == "adb" and "burp" in parser.parse_known_args()[1]:
        check_adb_installed()
        convert_and_push_ca_cert_to_android(args.cert, args.adbip)
        android_to_burp(args.burpip,args.adbip)
else:
    print(colored("[+] Missing Required Option cert/burp", "red"))