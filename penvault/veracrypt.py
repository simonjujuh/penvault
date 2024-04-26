import shutil
import subprocess


verabin = shutil.which("veracrypt")
if not verabin:
    raise Exception('Veracryt is not in your PATH')


def create_container(container_path, project_size, password):
    command = [verabin, "--text", "--create", 
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
    command = [verabin, "--text", "--mount", 
                str(container_path),
                str(mount_path),
                f"--password={password}",
                "--pim=0",
                "--keyfiles=",
                "--protect-hidden=no"
                ]
    
    subprocess.run(command, text=True, check=True)


def umount_container(container_path):
    command = [verabin, "--text", "--dismount", str(container_path)]

    subprocess.run(command, text=True, check=True)


def list_mounted_containers():
    command = [verabin, "--text", "--list"]
    command_output = subprocess.run(command, text=True, capture_output=True)

    return command_output.stdout

