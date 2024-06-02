import paramiko
import time
from app.utils import send_telegram_message_sync


def shutdown_server(max_retries=10):
    try:
        # Obtener todos los servidores de la base de datos
        servers = Host.query.all()

        for server in servers:
            shutdown_host_manual(server.ip_address, server.username, server.password, server.category, max_retries=max_retries)

    except Exception as e:
        error_message = f'Error al apagar los servidores: {e}'
        print(error_message)
        send_telegram_message_sync(error_message)  # Enviar mensaje de error

# Función para apagar el servidor según su tipo
def shutdown_host_manual(ip_address, username, password, category, max_retries=10):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    attempts = 0
    success = False

    while attempts < max_retries and not success:
        try:
            ssh.connect(ip_address, username=username, password=password)

            if category == 'Linux':
                command = 'sudo /sbin/shutdown -h now'
            elif category == 'Windows':
                command = 'shutdown /s /f /t 0'
            elif category == 'FreeBSD':
                command = 'sudo /sbin/shutdown -h now'
            elif category == 'VMware':
                command = 'sudo halt'
            elif category == 'Proxmox':
                command = 'sudo /sbin/shutdown -h now'
            elif category == 'Synology':
                command = 'sudo -i'
                synology_command = 'synopoweroff'
            else:
                raise Exception("Unsupported host category")

            if category == 'Synology':
                # Open an interactive shell
                channel = ssh.invoke_shell()

                # Send the command to escalate privileges
                channel.send(command + '\n')
                time.sleep(1)
                output = channel.recv(1024).decode()

                # Send the password for sudo
                channel.send(password + '\n')
                time.sleep(1)
                output += channel.recv(1024).decode()

                # Send the shutdown command
                channel.send(synology_command + '\n')
                time.sleep(1)
                output += channel.recv(1024).decode()

                # Check if the shutdown command was successful
                if 'shutdown' in output.lower() or 'poweroff' in output.lower():
                    success = True
                    success_message = f'Se apagó correctamente el servidor en {ip_address}'
                    send_telegram_message_sync(success_message)  # Enviar mensaje de éxito
                    print(success_message)
                else:
                    raise Exception("Failed to execute shutdown command on Synology")
            else:
                # Ejecutar el comando adecuado
                stdin, stdout, stderr = ssh.exec_command(command)
                stdout.channel.recv_exit_status()  # Esperar a que el comando termine
                stderr_output = stderr.read().decode()
                if stderr_output:
                    raise Exception(stderr_output)

                success = True
                success_message = f'Se apagó correctamente el servidor en {ip_address}'
                send_telegram_message_sync(success_message)  # Enviar mensaje de éxito
                print(success_message)

        except Exception as e:
            attempts += 1
            error_message = f'Error al apagar el servidor en {ip_address}, intento {attempts}: {e}'
            print(error_message)
            if attempts >= max_retries:
                final_error_message = f"No se pudo apagar el servidor en {ip_address} después de {attempts} intentos. Error: {e}"
                send_telegram_message_sync(final_error_message)  # Enviar mensaje de error después de max_retries intentos
                print(final_error_message)
        finally:
            ssh.close()
