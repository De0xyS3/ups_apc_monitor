# UPS Monitor

UPS Monitor es una aplicación web desarrollada con Flask que permite monitorear y gestionar servidores y el estado de las baterías de un sistema de alimentación ininterrumpida (UPS).
![image](https://github.com/De0xyS3/ups_apc_monitor/assets/87393512/11c87cc6-1b24-44b2-9a4a-e5e37b579089)

## Características

- Visualización del estado de los servidores en tiempo real.
- Monitorización del estado de la batería del UPS mediante SNMP.
- Gestión de servidores: agregado, actualización y eliminación de servidores.
- Configuración del umbral de la batería para activar acciones automáticas.
- Funcionalidad de apagado automático de servidores cuando el estado de la batería del UPS está por debajo del umbral configurado.

## Instalación

1. Clona este repositorio en tu máquina local:
https://github.com/De0xyS3/ups_monitor_apc.git

2. Ve al directorio del proyecto:
cd ups_monitor


## Configuración del Proyecto

### Configurar la Base de Datos

1. **flask db init**: Inicializa las migraciones en el proyecto Flask (solo la primera vez).
2. **flask db migrate**: Crea un nuevo archivo de migración basado en los cambios en el modelo de la base de datos.
3. **flask db upgrade**: Aplica las migraciones pendientes al esquema de la base de datos.

### Configurar el Entorno Virtual

1. **python3 -m venv venv**: Crea un nuevo entorno virtual llamado "venv" en el directorio del proyecto.
2. **source venv/bin/activate**: Activa el entorno virtual en sistemas Linux o macOS.
3. **venv\Scripts\activate**: Activa el entorno virtual en sistemas Windows.
4. **apt install python3-flask**

### Instalar Dependencias

Ejecuta el siguiente comando para instalar todas las dependencias del proyecto:

```bash
pip install -r requirements.txt
```

### Ejecución del Proyecto

Para ejecutar la aplicación, utiliza el siguiente comando:

```bash
flask run
```
La aplicación estará disponible en tu navegador web en `http://localhost:5000`.

## Contribuciones

Las contribuciones son bienvenidas. Si tienes sugerencias de mejoras, funcionalidades adicionales o encuentras algún error, por favor crea un _issue_ o envía un _pull request_.

## Licencia

Este proyecto está bajo la [Licencia MIT](LICENSE).





