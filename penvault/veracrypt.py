import shutil
import subprocess

def veracrypt_binary_path():
    verabin = shutil.which("veracrypt")
    if not verabin:
        raise Exception('Veracryt is not in your PATH')
    
    return verabin


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
    
    subprocess.run(command, text=True, check=True) #, capture_output=False 
    

def mount_container(container_path, mount_path, password):
    command = [veracrypt_binary_path(), "--text", "--mount", 
                str(container_path),
                str(mount_path),
                f"--password={password}",
                "--pim=0",
                "--keyfiles=",
                "--protect-hidden=no"
                ]
    
    subprocess.run(command, text=True, check=True)


def umount_container(container_path):
    command = [veracrypt_binary_path(), "--text", "--dismount", str(container_path)]

    subprocess.run(command, text=True, check=True)


def list_mounted_containers():
    command = [veracrypt_binary_path(), "--text", "--list"]
    command_output = subprocess.run(command, text=True, capture_output=True)

    # Parser les données
    mounted_containers = []
    for line in command_output.stdout.split('\n'):
        if line.strip():
            info = line.split(': ')
            mounted_container.append(info[1].split())

    return mount_container
