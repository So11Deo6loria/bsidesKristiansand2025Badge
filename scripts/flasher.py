import os
import platform
import time
import shutil
import subprocess

UF2_FILE = os.path.join("scripts", "microPython-pico.uf2")
DRIVE_NAME = "RPI-RP2"
FIRMWARE_DIR = "firmware"


def check_rshell_availability():
    try:
        result = subprocess.run(['rshell', 'ls'], capture_output=True, text=True, check=True)
        return "No MicroPython boards connected" not in result.stdout
    except subprocess.CalledProcessError:
        return False
    except FileNotFoundError:
        print("[!] rshell not found. Install it with 'pip install rshell'")
        return False


def get_mount_path():
    system = platform.system()
    if system == "Darwin":
        return "/Volumes"
    elif system == "Linux":
        return f"/media/{os.getenv('USER')}"
    else:
        raise RuntimeError("Unsupported OS")


def find_mounted_drive():
    base_path = get_mount_path()
    try:
        for drive in os.listdir(base_path):
            if DRIVE_NAME in drive:
                return os.path.join(base_path, drive)
    except Exception as e:
        print(f"[!] Error locating mounted drive at {base_path}: {e}")
    return None


def copy_uf2_to_drive():
    mounted_drive = find_mounted_drive()
    if mounted_drive:
        try:
            dest_path = os.path.join(mounted_drive, os.path.basename(UF2_FILE))
            shutil.copy(UF2_FILE, dest_path)
            print(f"[+] Copied {UF2_FILE} to {mounted_drive}")
            return True
        except Exception as e:
            print(f"[!] Failed to copy UF2: {e}")
    else:
        print(f"[!] Drive '{DRIVE_NAME}' not found.")
    return False


def sync_filesystem():
    try:
        subprocess.run(['rshell', 'rsync', '-a', f'{FIRMWARE_DIR}/', '/pyboard'], check=True)
        print("[+] Firmware sync successful.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[!] rsync failed: {e}")
        return False


def wait_for_pico():
    print("[*] Waiting for Raspberry Pi Pico...")
    while True:
        if not check_rshell_availability():
            print("[*] No device via rshell. Trying UF2 flash...")
            if copy_uf2_to_drive():
                print("[*] UF2 copied. Waiting for reboot...")
                time.sleep(5)
        else:
            if sync_filesystem():
                input("[+] Press Enter to continue or Ctrl+C to exit.")
        time.sleep(2)


if __name__ == "__main__":
    wait_for_pico()
