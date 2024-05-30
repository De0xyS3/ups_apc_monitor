import paramiko
import time
from app.utils import send_telegram_message_sync


def shutdown_server(max_retries=3):
    # Obtener todos los servidores de la base de datos
    servers = Host.query.all()

    for server in servers:
        ip_address = server.ip_address
        username = server.username
        password = server.password

        # Crear una instancia de cliente SSH
        ssh = paramiko.SSHClient()
        # Establecer la política de agregar automáticamente claves de host
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        attempts = 0
        success = False

        while attempts < max_retries and not success:
            try:
                # Conectar al servidor remoto
                ssh.connect(ip_address, username=username, password=password)
                # Ejecutar el comando de apagado
                ssh.exec_command('shutdown -h now')
                success = True
                success_message = f'Servidor en {ip_address} apagado correctamente.'
                send_telegram_message_sync(success_message)  # Enviar mensaje de éxito
                print(success_message)
            except paramiko.AuthenticationException:
                error_message = f'Error de autenticación al conectar al servidor en {ip_address}.'
                print(error_message)
                send_telegram_message_sync(error_message)  # Enviar mensaje de error de autenticación
                break  # No reintentar en caso de error de autenticación
            except paramiko.SSHException as e:
                attempts += 1
                error_message = f'Error al conectar al servidor en {ip_address}, intento {attempts}: {e}'
                print(error_message)
                if attempts >= max_retries:
                    final_error_message = f"No se pudo apagar el servidor en {ip_address} después de {attempts} intentos. Error: {e}"
                    send_telegram_message_sync(final_error_message)  # Enviar mensaje de error después de max_retries intentos
                    print(final_error_message)
            finally:
                # Cerrar la conexión SSH
                ssh.close()


def shutdown_server_manual(ip_address, username, password, max_retries=3):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    attempts = 0
    success = False

    while attempts < max_retries and not success:
        try:
            ssh.connect(ip_address, username=username, password=password)
            ssh.exec_command('sudo /sbin/shutdown -h now')
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

    return success
