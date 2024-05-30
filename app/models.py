from app import db

class Host(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    ip_address = db.Column(db.String(64), index=True)
    username = db.Column(db.String(64))
    password = db.Column(db.String(128))
    port = db.Column(db.Integer, default=22)
    status = db.Column(db.String(64), default='unknown')

    def __repr__(self):
        return f'<Host {self.name}>'

class BatteryThreshold(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    threshold = db.Column(db.Integer, default=100)

    def __repr__(self):
        return f'<BatteryThreshold {self.threshold}>'
