from __future__ import print_function
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Create database
Base = declarative_base()

# The Account class corresponds to the "accounts" database table.
class Account(Base):
    __tablename__ = 'accounts'
    id = Column(Integer, primary_key=True)
    #balance = Column(Integer)
    card = Column(Integer)

# The Items class corresponds to the "items" database table.
class Item(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True)
    name = Column(String(32))
    count = Column(Integer)
    sold = Column(Integer)
    price = Column(Float)

# Create an engine to communicate with the database. The "cockroachdb://" prefix
# for the engine URL indicates that we are connecting to CockroachDB.
engine = create_engine("cockroachdb://FourthWall@localhost:26257/myStore?sslmode=disable")
Session = sessionmaker(bind=engine)

# Automatically create the "accounts" and "items" tables based on the Account and Item classes.
Base.metadata.create_all(engine)

# Insert two rows into the "accounts" table.
session = Session()
session.add_all([
    Account(id=1, card=4532759734545858 ),	# Visa
    Account(id=2, card=5409889944179029),	# MasterCard
    Account(id=3, card=6011033621379697),	# Discover
    Account(id=4, card=36004244846408),		# Diners Club
    Account(id=5, card=3566005734880650),	# JCB
    Account(id=6, card=371263462726550),	# American Express
    Account(id=7, card=6222520119138184),	# China UnionPay
    Item(id=1, name="Chair", count=20, sold=0, price=39.99),
    Item(id=2, name="Table", count=10, sold=0, price=89.99),
    Item(id=3, name="Lamp", count=10, sold=0, price=25.99),
])
session.commit()

# Print out the accounts
for account in session.query(Account):
    print(account.id, account.card)

# Print out the items
for item in session.query(Item):
    print(item.id, item.name, item.count, item.sold, item.price)