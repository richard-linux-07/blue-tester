import asyncio
from bleak import BleakScanner, BleakClient
from colorama import init, Fore

init(autoreset=True)

def banner():
    print(Fore.CYAN + r"""
  ____  _             _   _____         _             
 | __ )| |_   _  __ _| | |_   _|__  ___| |_ ___  _ __ 
 |  _ \| | | | |/ _` | |   | |/ _ \/ __| __/ _ \| '__|
 | |_) | | |_| | (_| | |   | |  __/\__ \ || (_) | |   
 |____/|_|\__,_|\__,_|_|   |_|\___||___/\__\___/|_|   

         Educational Bluetooth Test Tool
""")

async def scan_devices():
    print(Fore.GREEN + "[*] Scanning for Bluetooth devices...\n")
    devices = await BleakScanner.discover(timeout=5)
    for idx, d in enumerate(devices):
        print(f"{Fore.YELLOW}{idx + 1}. {d.name or 'Unknown'} - {d.address}")
    return devices

async def stress_connect(address):
    print(Fore.CYAN + f"[*] Attempting multiple connections to {address}...\n")
    for i in range(10):
        try:
            async with BleakClient(address) as client:
                print(Fore.GREEN + f"[{i+1}] Connected: {client.is_connected}")
        except Exception as e:
            print(Fore.RED + f"[!] Failed to connect: {e}")

async def main():
    banner()
    print("1. Scan Devices")
    print("2. Stress Test Device")
    choice = input("Choose option: ")

    if choice == "1":
        await scan_devices()
    elif choice == "2":
        addr = input("Enter device MAC/UUID: ")
        await stress_connect(addr)
    else:
        print(Fore.RED + "Invalid option.")

if __name__ == "__main__":
    asyncio.run(main())
