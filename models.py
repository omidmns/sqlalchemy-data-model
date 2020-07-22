import sqlalchemy
import os
from sqlalchemy import DECIMAL, Column, Integer, String, Boolean, ForeignKey, ForeignKeyConstraint
from sqlalchemy.types import DateTime, SmallInteger
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import database_exists, create_database
from faker import Faker
import random
from datetime import datetime

fake = Faker()

user = 'docker_pg' #os.environ['POSTGRES_USER']
pwd = 'helloworld' #os.environ['POSTGRES_PASSWORD']
db = 'finnai_db1_seed20' #os.environ['POSTGRES_DB']
host = 'localhost' #'db'
port = '5433' #'5432'
engine = create_engine(
        'postgres://%s:%s@%s:%s/%s' % (user, pwd, host, port, db))

if not database_exists(engine.url):
            create_database(engine.url)

db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

class address(Base):
    """
    address table
    """
    __tablename__ = 'address'
    address_id = Column(Integer,autoincrement=True, primary_key=True, nullable=False)
    isActive = Column(Boolean, nullable=False, default=True)
    street_address_1 = Column(String(900), nullable=False)
    street_address_2 = Column(String(900))
    city = Column(String(900), nullable=False)
    zip = Column(String(10), nullable=False)

class feedback(Base):

    __tablename__ = 'feedback'
    feedback_id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    feedback_text = Column(String(900), nullable=False)
    first_name = Column(String(45))
    last_name = Column(String(45))
    email = Column(String(45)) 
    order_order_id = Column(Integer,ForeignKey('orders.order_id') ,nullable=False) 

class inventory(Base):

    __tablename__ = 'inventory'
    inventory_id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    inventory_quantity = Column(SmallInteger, nullable=False) 
    inventory_min = Column(SmallInteger, nullable=False) 
    inventory_max = Column(SmallInteger, nullable=False) 
    isActive = Column(Boolean, nullable=False, default=True) 
    brand_brand_id = Column(Integer, ForeignKey('brand.brand_id'),nullable=False) 
 
class item_type(Base):

    __tablename__ = 'item_type'
    item_type_id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    item_type_name = Column(String(45), nullable=False) 
    isActive = Column(Boolean, nullable=False, default=True)

class item(Base):

    __tablename__ = 'item'
    item_id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    item_name = Column(String(45))
    isActive = Column(Boolean, nullable=False, default=True)
    inventory_inventory_id = Column(Integer, ForeignKey('inventory.inventory_id'),nullable=False)
    item_type_item_type_id = Column(Integer, ForeignKey('item_type.item_type_id'),nullable=False)
  
class orders(Base):

    __tablename__ = 'orders'
    order_id =  Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    ordered_time = Column(DateTime, nullable=False)
    address_address_id = Column(Integer, ForeignKey('address.address_id'),nullable=False)
    phone_number_phone_number_id = Column(Integer, ForeignKey('phone_number.phone_number_id'),nullable=False)

class order_has_item(Base):

    __tablename__ = 'order_has_item'
    order_has_item_id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    quantity = Column(SmallInteger, nullable=False) 
    price_price_id = Column(Integer, ForeignKey('price.price_id'),nullable=False)
    order_order_id = Column(Integer, ForeignKey('orders.order_id'),nullable=False)
 
class phone_number(Base):

    __tablename__ = 'phone_number'
    phone_number_id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    phone_number = Column(String(22), nullable=False) 
    isActive = Column(Boolean, nullable=False, default=True)
    area_code =  Column(String(22))

class price(Base):

    __tablename__ = 'price'
    price_id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    item_item_id = Column(Integer, ForeignKey('item.item_id'),nullable=False)
    price_tag = Column(DECIMAL(10,0), nullable=False) 
    isActive = Column(Boolean, nullable=False, default=True)
   
class supplier(Base):

    __tablename__ = 'supplier'
    supplier_id = Column(SmallInteger, nullable=False, primary_key=True, autoincrement=True)
    supplier_name = Column(String(45), nullable=False) 
    isActive = Column(Boolean, nullable=False, default=True)
    phone_number_id = Column(Integer, ForeignKey('phone_number.phone_number_id'),nullable=False)
    address_address_id = Column(Integer, ForeignKey('address.address_id'), nullable=False)
   
class brand(Base):

    __tablename__ = 'brand'
    brand_id = Column(Integer, autoincrement=True, primary_key=True, nullable=False)
    brand_name = Column(String(200), nullable=False)
    isActive = Column(Boolean, nullable=False, default=True)
    supplier_supplier_id = Column(SmallInteger, ForeignKey('supplier.supplier_id'), nullable=False)

class seed:
    """
    seeder for tables
    """
    
    def __init__(self, N=0):

        self.seeder(N)

    def seeder(self,N):
        for _ in range(N):
            self.seed_order_has_item()

    def seed_address(self):
            
            street = fake.address()
            city = fake.city()
            zip = fake.zipcode()

            address_st = address(
                street_address_1 = street,
                city = city,
                zip = zip
            )
            db_session.add(address_st)
            db_session.commit()
            
            return address_st

    def seed_phone(self):    

            phone_numer = fake.phone_number()

            phn = phone_number(
                phone_number = phone_numer
            )
            db_session.add(phn)
            db_session.commit()

            return phn

    def seed_order(self):

            order_time = datetime.now()
            add = self.seed_address()
            phone = self.seed_phone()

            order =orders(
                ordered_time = order_time,
                address_address_id = add.address_id,
                phone_number_phone_number_id = phone.phone_number_id
            )
            db_session.add(order)
            db_session.commit()

            self.seed_feedback(order)

            return order

    def seed_feedback(self, order):            

            feedback_text = fake.text()
            feedback_first_name = fake.first_name()
            feedback_last_name = fake.last_name()
            feedback_email = fake.email()

            fback = feedback(
                feedback_text = feedback_text,
                first_name = feedback_first_name,
                last_name = feedback_last_name,
                email = feedback_email,
                order_order_id = order.order_id
            )
            db_session.add(fback)
            db_session.commit()

            return fback

    def seed_supplier(self):        

            supplier_name = fake.name()
            phone = self.seed_phone()
            address = self.seed_address()

            supl = supplier(
                supplier_name = supplier_name,
                phone_number_id = phone.phone_number_id,
                address_address_id = address.address_id
            )
            db_session.add(supl)
            db_session.commit()

            return supl

    def seed_brand(self):

            brand_name = fake.country()
            supplier = self.seed_supplier()

            br = brand(
                brand_name = brand_name,
                supplier_supplier_id = supplier.supplier_id
            )
            db_session.add(br)
            db_session.commit()

            return br

    def seed_inventory(self):

            inventory_min = random.randint(20,50)
            inventory_max = random.randint(100,10000)
            inventory_quantity = random.randint(20,10000)
            brand = self.seed_brand()

            invent = inventory(
                inventory_quantity = inventory_quantity,
                inventory_min = inventory_min,
                inventory_max = inventory_max,
                brand_brand_id = brand.brand_id
            )
            db_session.add(invent)
            db_session.commit()

            return invent

    def seed_item_type(self):

            item_type_name = fake.last_name()

            it_type = item_type(
                item_type_name=item_type_name
            ) 
            db_session.add(it_type)
            db_session.commit()

            return it_type
            
    def seed_item(self):
            
            item_name = fake.first_name()
            inventory = self.seed_inventory()
            item_type = self.seed_item_type()

            it = item(
                item_name = item_name,
                inventory_inventory_id = inventory.inventory_id,
                item_type_item_type_id = item_type.item_type_id
            )
            db_session.add(it)
            db_session.commit()

            return it

    def seed_price(self):

            price_tag = random.randint(1000,15000)/100
            item = self.seed_item()

            pr = price(
                item_item_id = item.item_id,
                price_tag = price_tag
            )
            db_session.add(pr)
            db_session.commit()
            
            return pr

    def seed_order_has_item(self):

            order_quantity_1 = random.randint(1,10)
            
            order1 = self.seed_order()
            price1 = self.seed_price()
            order_item1 = order_has_item(
                quantity = order_quantity_1,
                price_price_id = price1.price_id,
                order_order_id = order1.order_id
            )
            db_session.add(order_item1)

            price2 = self.seed_price()
            order_quantity_2 = random.randint(1,10)
            order_item2 = order_has_item(
                quantity = order_quantity_2,
                price_price_id = price2.price_id,
                order_order_id = order1.order_id
            )
            db_session.add(order_item2)
            db_session.commit()      

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine) 
    seed(5)
