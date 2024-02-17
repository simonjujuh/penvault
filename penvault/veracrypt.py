import shutil, sys
import subprocess

def veracrypt_binary_path():
    return shutil.which("veracrypt")


def create_container(container_path, project_size, password):
    # check if path already exists
    command = [veracrypt_binary_path(), "--text", "--create", 
               str(container_path),
               f"--size={project_size}", 
               f"--password={password}", 
                "--volume-type=normal", 
                "--encryption=AES", 
                "--hash=sha-512", 
                "--filesystem=fat", 
                "--pim=0", 
                "--keyfiles=", 
                "--random-source=/dev/urandom"
              ]
    
    try:
        # Execute the command
        subprocess.run(command, text=True) #, capture_output=False ,text=True)
        print(f"[+] container '{container_path}' created successfully")
    except subprocess.CalledProcessError as e:
        print(f"[-] error while creating '{container_path}': {e}")
        sys.exit(1)
    

def mount_container(container_path, mount_path, password):
    command = [veracrypt_binary_path(), "--text", "--mount", 
                str(container_path),
                str(mount_path),
                f"--password={password}",
                "--pim=0",
                "--keyfiles=",
                "--protect-hidden=no"
                ]
    try:
        # Execute the command
        subprocess.run(command, text=True, check=True)
        print(f"[+] container '{container_path}' mounted successfully at '{mount_path}'")

    except subprocess.CalledProcessError as e:
        print(f"[-] error while opening {container_path}: {e}")
        sys.exit(1)


def umount_container(container_path):
    command = [veracrypt_binary_path(), "--text", "--dismount", str(container_path)]

    try:
        # Execute the command
        subprocess.run(command, text=True, check=True)
        print(f"[+] container '{container_path}' dismounted successfully")

    except subprocess.CalledProcessError as e:
        print(f"[-] error while dismonting {container_path}: {e}")


def list_mounted_containers():
    command = [veracrypt_binary_path(), "--text", "--list"]
    try:
        # Execute the command
        command_output = subprocess.run(command, text=True, capture_output=True)
        return parse_veracrypt_output(command_output.stdout)
    except subprocess.CalledProcessError as e:
        print(f"[-] could not list containers: {e}")


def parse_veracrypt_output(output):
    entries = output.split('\n')
    info_list = []

    for entry in entries:
        if entry.strip() == "":
            continue
        info = {}
        parts = entry.split(':', 1)

        if len(parts) == 2:
            values = parts[1].split()
            
            info["path"] = values[0]
            info["device"] = values[1]
            info["mount point"] = values[2]

            info_list.append(info)

    return info_list

