from datetime import datetime
from os import getenv

from faker import Faker
from pydantic import BaseModel
from pydantic.types import Enum

from app.services.user_services import hash_password
from app.db.database import get_db_unyield
from app.models.lunch_models import Lunch as DB_Lunch
from app.models.organization_models import Organization, OrganizationInvite, OrganizationLaunchWallet
from app.models.user_models import User as DB_User, Withdrawal as DB_Withdrawal


fake = Faker()
NUM_RECORDS = int(getenv("NUM_RECORDS", 10))


class User(BaseModel):
    id: int
    email: str
    password_hash: str
    first_name: str
    last_name: str
    phone: str
    org_id: int
    is_admin: bool = False


class Org(BaseModel):
    id: int
    name: str
    lunch_price: float
    currency_code: str
    created_at: datetime
    updated_at: datetime
    is_deleted: bool = False


class OrgWallet(BaseModel):
    id: int
    org_id: int
    balance: float
    created_at: datetime
    updated_at: datetime
    is_deleted: bool = False


class OrgInvite(BaseModel):
    id: int
    email: str
    token: str
    ttl: datetime
    org_id: int
    created_at: datetime
    updated_at: datetime
    is_deleted: bool = False


class Withdrawal(BaseModel):
    id: int
    user_id: int
    amount: float
    status: Enum('success', 'pending') = 'pending'
    created_at: datetime
    updated_at: datetime
    is_deleted: bool = False


class Lunch(BaseModel):
    id: int
    org_id: int
    sender_id: int
    receiver_id: int
    quantity: int
    redeemed: bool = False
    note: str = None
    created_at: datetime
    updated_at: datetime
    is_deleted: bool = False


def seed_orgs() -> list[Org]:
    """generate orgs"""
    orgs: list[Org] = []
    for i in range(NUM_RECORDS):
        org = Org(
            id=i + 1,
            name=fake.company(),
            lunch_price=fake.pyfloat(
                left_digits=8, right_digits=2, positive=True),
            currency_code=fake.currency_code(),
            created_at=fake.date_time(),
            updated_at=fake.date_time(),
        )
        orgs.append(org)

    return orgs


def seed_users() -> tuple[list[Org], list[User]]:
    """generate users"""
    orgs = seed_orgs()

    users: list[User] = []
    for i in range(NUM_RECORDS):
        user = User(
            id=i + 1,
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            email=fake.email(),
            password_hash=hash_password(fake.password()),
            phone=str(fake.random.randint(1000000000, 9999999999)),
            org_id=fake.random.choice(orgs).id,
        )
        users.append(user)

    return orgs, users


def seed_org_wallets() -> list[OrgWallet]:
    """generate org wallets"""
    orgs, _ = seed_users()

    org_wallets: list[OrgWallet] = []
    for i in range(NUM_RECORDS):
        org_wallet = OrgWallet(
            id=i + 1,
            org_id=orgs[i].id,
            balance=fake.pyfloat(left_digits=8, right_digits=2, positive=True),
            created_at=fake.date_time(),
            updated_at=fake.date_time(),
        )
        org_wallets.append(org_wallet)
        print(org_wallet)
    return org_wallets


def seed_invites() -> list[OrgInvite]:
    """generates invites"""
    orgs = seed_orgs()

    invites: list[OrgInvite] = []
    for i in range(NUM_RECORDS):
        invite = OrgInvite(
            id=i + 1,
            email=fake.email(),
            token=fake.uuid4(),
            ttl=fake.date_time(),
            org_id=fake.random.choice(orgs).id,
            created_at=fake.date_time(),
            updated_at=fake.date_time(),
        )
        print(invite)
        invites.append(invite)

    return invites


def seed_withdrawals() -> list[Withdrawal]:
    """generates withdrawals"""
    _, users = seed_users()

    withdrawals: list[Withdrawal] = []
    for i in range(NUM_RECORDS):
        withdrawal = Withdrawal(
            id=i + 1,
            user_id=fake.random.choice(users).id,
            amount=fake.pyfloat(left_digits=8, right_digits=2, positive=True),
            created_at=fake.date_time(),
            updated_at=fake.date_time(),
        )
        print(withdrawal)
        withdrawals.append(withdrawal)

    return withdrawals


def seed_lunches() -> list[Lunch]:
    """generates lunches"""
    orgs, users = seed_users()

    lunches: list[Lunch] = []
    for i in range(NUM_RECORDS):
        lunch = Lunch(
            id=i + 1,
            org_id=fake.random.choice(orgs).id,
            sender_id=fake.random.choice(users).id,
            receiver_id=fake.random.choice(users).id,
            quantity=fake.random.randint(1, 5),
            note=fake.sentence(nb_words=4),
            created_at=fake.date_time(),
            updated_at=fake.date_time(),
        )
        print(lunch)
        lunches.append(lunch)

    return lunches


def populate_db():
    """populate the database"""
    db = get_db_unyield()

    orgs, users = seed_users()
    org_wallets = seed_org_wallets()
    invites = seed_invites()
    withdrawals = seed_withdrawals()
    lunches = seed_lunches()

    for org in orgs:
        db_org = Organization(**org.__dict__)
        db.add(db_org)
        db.commit()
        db.refresh(db_org)

    for user in users:
        db_user = DB_User(**user.__dict__)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

    for org_wallet in org_wallets:
        db_org_wallet = OrganizationLaunchWallet(**org_wallet.__dict__)
        db.add(db_org_wallet)
        db.commit()
        db.refresh(db_org_wallet)

    for invite in invites:
        db_invite = OrganizationInvite(**invite.__dict__)
        db.add(db_invite)
        db.commit()
        db.refresh(db_invite)

    for withdrawal in withdrawals:
        db_withdrawal = DB_Withdrawal(**withdrawal.__dict__)
        db.add(db_withdrawal)
        db.commit()
        db.refresh(db_withdrawal)

    for lunch in lunches:
        db_lunch = DB_Lunch(**lunch.__dict__)
        db.add(db_lunch)
        db.commit()
        db.refresh(db_lunch)


populate_db()
