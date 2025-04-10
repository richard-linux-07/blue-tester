import os
import platform
import asyncio
from bleak import BleakScanner, BleakClient
from colorama import Fore, Style, init
from datetime import datetime
import getpass

init(autoreset=True)

LOG_FOLDER = "logs"
os.makedirs(LOG_FOLDER, exist_ok=True)

def get_own_mac():
    if platform.system() == "Linux":
        try:
            with os.popen("hciconfig") as f:
                data = f.read()
            for line in data.splitlines():
                if "BD Address" in line:
                    return line.strip().split()[-1]
        except:
            return None
    elif platform.system() == "Windows":
        try:
            with os.popen("getmac /v /fo list") as f:
                data = f.read()
            for section in data.split('\n\n'):
                if "Bluetooth Network Connection" in section:
                    for line in section.splitlines():
                        if "Physical Address" in line:
                            return line.split(":")[1].strip().replace("-", ":")
        except:
            return None
    return None

def log_output(text):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    with open(f"{LOG_FOLDER}/bluetooth_log_{timestamp}.txt", "a") as f:
        f.write(text + "\n")

async def scan_devices(skip_mac=None):
    print(Fore.CYAN + "\n[*] Scanning for Bluetooth devices...\n")
    devices = await BleakScanner.discover()
    result = []
    for i, device in enumerate(devices):
        if skip_mac and device.address.lower() == skip_mac.lower():
            continue
        name = device.name or "Unknown"
        print(f"{Fore.YELLOW}{i+1}. {name} - {device.address}")
        result.append((i + 1, name, device.address))
        log_output(f"Scanned: {name} - {device.address}")
    return result

async def stress_test(address, attempts):
    print(Fore.MAGENTA + f"\n[*] Starting stress test on {address} with {attempts} attempts...\n")
    for i in range(attempts):
        try:
            print(Fore.WHITE + f"[{i+1}] Connecting to {address}...")
            async with BleakClient(address) as client:
                await asyncio.sleep(0.5)
                if client.is_connected:
                    print(Fore.GREEN + f"+ Connected [{i+1}]")  # Changed ✔ to +
                    log_output(f"+ Connected [{i+1}] to {address}")
        except Exception as e:
            print(Fore.RED + f"- Failed [{i+1}] - {e}")
            log_output(f"- Failed [{i+1}] - {e}")
        await asyncio.sleep(0.5)

def banner():
    print(Fore.LIGHTBLUE_EX + r"""
    
______ _              _____         _            
| ___ \ |            |_   _|       | |           
| |_/ / |_   _  ___    | | ___  ___| |_ ___ _ __ 
| ___ \ | | | |/ _ \   | |/ _ \/ __| __/ _ \ '__|
| |_/ / | |_| |  __/   | |  __/\__ \ ||  __/ |   
\____/|_|\__,_|\___|   \_/\___||___/\__\___|_|   
                                                 
                                                 

     💻 Educational Bluetooth Test Tool 💻
    """)

async def main_menu():
    banner()
    skip_mac = get_own_mac()
    if skip_mac:
        print(Fore.LIGHTBLACK_EX + f"[*] Skipping own MAC address: {skip_mac}\n")

    while True:
        print(Fore.CYAN + "\n1. Scan Devices")
        print("2. Stress Test Device")
        print("3. Exit")
        choice = input(Fore.GREEN + "\nChoose option: ").strip()

        if choice == "1":
            await scan_devices(skip_mac)
        elif choice == "2":
            addr = input("Enter MAC address of device to test: ").strip()
            try:
                attempts = int(input("Enter number of attempts: ").strip())
                await stress_test(addr, attempts)
            except ValueError:
                print(Fore.RED + "Invalid input. Try again.")
        elif choice == "3":
            print(Fore.LIGHTBLUE_EX + "\nExiting... Stay ethical 👋")
            break
        else:
            print(Fore.RED + "Invalid option. Try again.")

if __name__ == "__main__":
    asyncio.run(main_menu())
