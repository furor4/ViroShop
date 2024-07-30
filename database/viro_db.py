from sqlalchemy import create_engine, VARCHAR, BigInteger, Column, String, Float
from sqlalchemy.orm import sessionmaker, declarative_base

postgresql_db = 'postgresql://postgres:51535759o@localhost:5432/ViroShopDB'  # Вставьте свои данные для подключения к
# базе данных постгреса

engine = create_engine(postgresql_db, echo=True)

Base = declarative_base()


class Settings(Base):
    __tablename__ = 'settings'
    send_text = Column(VARCHAR(255), primary_key=True)
    file_id = Column(VARCHAR(250))


class Keyboard(Base):
    __tablename__ = 'keyboard'
    text = Column(VARCHAR(25), primary_key=True)
    url = Column(VARCHAR(250))


class User(Base):
    __tablename__ = 'users'
    user_id = Column(BigInteger, primary_key=True, index=True)
    username = Column(String)
    full_name = Column(String)
    balance = Column(BigInteger, default=0)


class Products(Base):
    __tablename__ = 'products'
    product_id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    price = Column(Float)


Base.metadata.create_all(engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
