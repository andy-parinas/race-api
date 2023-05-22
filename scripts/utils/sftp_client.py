import paramiko
from paramiko import SSHClient
from app.settings import settings



def create_ssh_client():
    try:
        private_key = paramiko.RSAKey.from_private_key_file(settings.SFTP_PRIVATE_KEY)
        ssh_client = SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname=settings.SFTP_HOST, port=settings.SFTP_PORT, username=settings.SFTP_USERNAME, pkey=private_key)
        return ssh_client
    except Exception as e:
        print("Error creating ssh client \n")
        print(e)
        return None
    



def get_files_in_dir(remote_dir: str):
    client = create_ssh_client()

    if client is None:
        return []

    try:
        sftp = client.open_sftp()
        file_list = sftp.listdir(remote_dir)
        return file_list
    except Exception as e:
        print("Error getting files in dir \n")
        print(e)
        return []
    finally:
        sftp.close()
        client.close()


def download_file( remote_dir: str, file_name: str, destination_dir: str):
    client = create_ssh_client()
    if client is None:
        return None


    try:
        sftp = client.open_sftp()
        sftp.get(f"{remote_dir}/{file_name}", f"{destination_dir}/{file_name}")
        return f"{destination_dir}/{file_name}"
    except Exception as e:
        print("Error downloading file \n")
        print(e)
        return None
    finally:
        sftp.close()
        client.close()

