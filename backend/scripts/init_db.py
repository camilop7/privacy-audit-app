from app.db.session import SessionLocal, engine
from app.models.user import User, UserRole
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db.session import Base
import uuid
from faker import Faker
import random
from app.core.security import hash_password

fake = Faker()


def seed_admin_user(db: Session):
    admin_email = "admin@privacyapp.com"
    existing = db.query(User).filter(User.email == admin_email).first()

    if existing:
        print("⚠️ Admin user already exists.")
        return

    new_user = User(
        id=uuid.uuid4(),
        email=admin_email,
        hashed_password=hash_password("admin123"),  # ✅ Secure password here
        username="admin",
        role=UserRole.admin
    )

    db.add(new_user)
    try:
        db.commit()
        print("✅ Admin user created.")
    except IntegrityError as e:
        db.rollback()
        print("❌ Could not create admin user:", str(e))


def seed_fake_users(db: Session, total: int = 50):
    print(f"👥 Seeding {total} fake users...")
    roles = [UserRole.user, UserRole.analyst]

    for _ in range(total):
        user = User(
            id=uuid.uuid4(),
            email=fake.unique.email(),
            hashed_password=hash_password("user123"),
            username=fake.unique.user_name(),
            role=random.choice(roles),
            full_name=fake.name(),
            phone=fake.phone_number(),
            address=fake.address(),
            company=fake.company(),
            job_title=fake.job(),
            bio=fake.text(max_nb_chars=200),
            profile_picture=fake.image_url()
        )
        db.add(user)

    try:
        db.commit()
        print("✅ Fake users seeded.")
    except IntegrityError as e:
        db.rollback()
        print("❌ Error seeding users:", str(e))


def main():
    print("📦 Creating DB tables if not exist...")
    ## Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    seed_admin_user(db)
    seed_fake_users(db, total=50)
    db.close()


if __name__ == "__main__":
    main()
