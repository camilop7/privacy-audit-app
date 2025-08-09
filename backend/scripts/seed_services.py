from app.db.session import SessionLocal
from app.models.service import Service

def run():
    db = SessionLocal()
    items = [
        ("Privacy Audit Lite", 199.0, 60),
        ("Privacy Audit Pro", 499.0, 120),
        ("Phone Risk Scan", 0.0, 5),
    ]
    for name, price, mins in items:
        if not db.query(Service).filter(Service.name == name).first():
            db.add(Service(name=name, price=price, duration_minutes=mins, description=f"{name} package"))
    db.commit(); db.close()

if __name__ == "__main__":
    run()
