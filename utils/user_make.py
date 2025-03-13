from database import SessionLocal
from user.infra.db_models.user import User
from datetime import datetime
from crypto import Crypto

with SessionLocal() as db:
    for i in range(50):
        user = User(
            id=f'UserID-{str(i).zfill(2)}',
            name=f'TestUser_{i}',
            email=f'test-user_{i}@example.com',
            password=Crypto().encrypt('test'),
            memo=None,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        db.add(user)
    db.commit()