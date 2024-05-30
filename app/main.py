from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.models import Host, BatteryThreshold
from app.utils import ping_host, send_telegram_message
from app.snmp_battery_state import get_snmp_battery_state
from app.shutdown_server import shutdown_server, shutdown_server_manual
import time
from threading import Thread
import subprocess
from flask import current_app

thread = None

#@app.route('/')
#def index():
#    hosts = Host.query.all()
#    battery_state = get_snmp_battery_state()
#    return render_template('index.html', hosts=hosts, battery_state=battery_state)
@app.route('/')
def index():
    hosts = Host.query.all()
    battery_state = get_snmp_battery_state()
    messages = check_battery()  # Obtener los mensajes de check_battery()
    return render_template('index.html', hosts=hosts, battery_state=battery_state, messages=messages)  # Pasar los mensajes a la plantilla

@app.route('/delete_host/<int:host_id>', methods=['POST'])
def delete_host(host_id):
    host = Host.query.get_or_404(host_id)
    db.session.delete(host)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/shutdown_host/<int:host_id>', methods=['POST'])
def shutdown_host(host_id):
    host = Host.query.get_or_404(host_id)
    try:
        shutdown_server_manual(host.ip_address, host.username, host.password)  # Llama a la función desde shutdown_server.py
        print(f'Se está realizando un apagado manual del servidor {host.name}...')
        flash(f'Se está realizando un apagado manual del servidor {host.name}...', 'success')
    except Exception as e:
        print(f'Error al realizar un apagado manual del servidor {host.name}: {e}')
        flash(f'Error al realizar un apagado manual del servidor {host.name}: {e}', 'error')
    return redirect(url_for('index'))



@app.route('/add_host', methods=['GET', 'POST'])
def add_host():
    if request.method == 'POST':
        name = request.form['name']
        ip_address = request.form['ip_address']
        username = request.form['username']
        password = request.form['password']
        port = request.form['port']

        new_host = Host(name=name, ip_address=ip_address, username=username, password=password, port=port)
        db.session.add(new_host)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('add_host.html')


@app.route('/update_status')
def update_status():
    hosts = Host.query.all()
    for host in hosts:
        if ping_host(host.ip_address):
            host.status = 'activo'
        else:
            host.status = 'apagado'
        db.session.commit()
    return redirect(url_for('index'))


@app.route('/set_threshold', methods=['GET', 'POST'])
def set_threshold():
    global thread, stop_thread

    if request.method == 'POST':
        threshold = request.form['threshold']
        threshold_record = BatteryThreshold.query.first()
        if threshold_record:
            threshold_record.threshold = threshold
        else:
            threshold_record = BatteryThreshold(threshold=threshold)
            db.session.add(threshold_record)
        db.session.commit()

        if thread:
            stop_thread = True
            thread.join()
        stop_thread = False
        thread = Thread(target=check_battery_periodically)
        thread.start()

        return redirect(url_for('index'))

    current_threshold = BatteryThreshold.query.first()
    return render_template('set_threshold.html', threshold=current_threshold.threshold if current_threshold else 100)

def check_battery():
    with current_app.app_context():
        state = get_snmp_battery_state()
        messages = []

        if state is None:
            messages.append(('Sin conexión con el UPS', 'error'))

        threshold_record = BatteryThreshold.query.first()
        threshold = threshold_record.threshold if threshold_record else 100

        if state >= threshold:
            messages.append(('La batería está por encima del umbral. No se realizarán acciones.', 'success'))

        new_state = get_snmp_battery_state()

        if new_state is None:
            messages.append(('Sin conexión con el UPS', 'error'))

        if new_state < threshold:
            if new_state < state:
                messages.append(('La batería está por debajo del umbral. Se han apagado los servidores.', 'error'))
                shutdown_server()
                send_telegram_message("Se han apagado los servidores debido a un bajo estado de la batería.")
            else:
                messages.append(('La batería está por debajo del umbral, pero está aumentando. No se realizarán acciones.', 'warning'))

        return messages


def check_battery_periodically():
    global stop_thread
    with app.app_context():
        while not stop_thread:
            check_battery()
            time.sleep(5)
