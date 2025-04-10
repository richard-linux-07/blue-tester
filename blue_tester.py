import subprocess

def scan_devices():
    print("[*] Scanning for Bluetooth devices...\n")
    result = subprocess.run(["bluetoothctl", "scan", "on"], capture_output=True, text=True, timeout=10)
    print(result.stdout)

def ping_device(mac):
    print(f"[*] Sending L2CAP pings to {mac}")
    try:
        subprocess.run(["l2ping", "-c", "10", mac])
    except Exception as e:
        print("[!] Error:", e)

def main():
    print("=== BlueTester ===")
    print("1. Scan Devices")
    print("2. Ping Device")
    choice = input("Choose option: ")

    if choice == "1":
        scan_devices()
    elif choice == "2":
        mac = input("Enter MAC address: ")
        ping_device(mac)
    else:
        print("Invalid option.")

if __name__ == "__main__":
    main()
