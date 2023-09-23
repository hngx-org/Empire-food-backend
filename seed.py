from datetime import datetime, timedelta
from os import getenv
import itertools
from pprint import pprint

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
    status: Enum('redeemed', 'not_redeemed') = 'not_redeemed'
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
        pprint(org)
        orgs.append(org)

    return orgs


def seed_users() -> tuple[list[Org], list[User]]:
    """generate users"""
    orgs = seed_orgs()

    users: list[User] = []
    admins: list[User] = []
    for i in range(NUM_RECORDS):
        user = User(
            id=i + 1,
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            email=fake.email(),
            password_hash=fake.password(),
            phone=str(fake.random.randint(1000000000, 9999999999)),
            org_id=i + 1,
            is_admin=True
        )
        pprint(user)
        user.password_hash = hash_password(user.password_hash)
        admins.append(user)

    for i in range(NUM_RECORDS, NUM_RECORDS * 3):
        user = User(
            id=i + 1,
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            email=fake.email(),
            password_hash=fake.password(),
            phone=str(fake.random.randint(1000000000, 9999999999)),
            org_id=fake.random.choice(orgs).id,
        )
        pprint(user)
        user.password_hash = hash_password(user.password_hash)
        users.append(user)

    return orgs, list(users)


def seed_org_wallets() -> tuple[list[Org], list[User], list[OrgWallet]]:
    """generate org wallets"""
    orgs, users = seed_users()

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
        pprint(org_wallet)
    return orgs, users, org_wallets


# def seed_invites() -> list[OrgInvite]:
#     """generates invites"""
#     orgs, users, org_wallets = seed_org_wallets()

#     invites: list[OrgInvite] = []
#     for i in range(NUM_RECORDS * 3):
#         user = fake.random.choice(users)
#         org = fake.random.choice(orgs)
#         invite = OrgInvite(
#             id=i + 1,
#             email=user.email,
#             token=fake.uuid4(),
#             ttl=datetime.now() + timedelta(minutes=30),
#             org_id=org.id,
#             created_at=datetime.now(),
#             updated_at=datetime.now(),
#         )
#         print(invite)
#         invites.append(invite)

#     return invites


def seed_withdrawals() -> tuple[list[Org], list[User], list[OrgWallet], list[Withdrawal]]:
    """generates withdrawals"""
    orgs, users, wallets = seed_org_wallets()

    withdrawals: list[Withdrawal] = []
    for i in range(NUM_RECORDS * 2):
        user = fake.random.choice(users)
        org = list(itertools.filterfalse(
            lambda org: org.id != user.org_id, orgs))[0]
        wallet = list(itertools.filterfalse(
            lambda wallet: wallet.id != org.id, wallets))[0]
        amount = fake.pyfloat(left_digits=5, right_digits=2, positive=True)
        while amount > wallet.balance:
            amount = fake.pyfloat(left_digits=5, right_digits=2, positive=True)

        for wall in wallets:
            if wall.id == wallet.id:
                balance = wall.balance - amount
                wallet.balance = float(f"{balance:.2f}")
        pprint(wallet)
        withdrawal = Withdrawal(
            id=i + 1,
            user_id=user.id,
            amount=amount,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        pprint(withdrawal)
        withdrawals.append(withdrawal)

    return orgs, users, wallets, withdrawals


def seed_lunches() -> tuple[list[Org], list[User], list[OrgWallet], list[Withdrawal], list[Lunch]]:
    """generates lunches"""
    orgs, users, wallets, withdrawals = seed_withdrawals()

    lunches: list[Lunch] = []
    for i in range(NUM_RECORDS * 2):
        sender = fake.random.choice(users)
        org_users = list(itertools.filterfalse(
            lambda user: user.org_id != sender.org_id and user != sender, users))
        receiver = fake.random.choice(org_users)

        lunch = Lunch(
            id=i + 1,
            org_id=sender.org_id,
            sender_id=fake.random.choice(users).id,
            receiver_id=receiver.id,
            quantity=fake.random.randint(1, 5),
            note=fake.sentence(nb_words=4),
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        pprint(lunch)
        lunches.append(lunch)

    return orgs, users, wallets, withdrawals, lunches


def populate_db():
    """populate the database"""
    db = get_db_unyield()

    orgs, users, wallets, withdrawals, lunches = seed_lunches()

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

    for org_wallet in wallets:
        db_org_wallet = OrganizationLaunchWallet(**org_wallet.__dict__)
        db.add(db_org_wallet)
        db.commit()
        db.refresh(db_org_wallet)

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
