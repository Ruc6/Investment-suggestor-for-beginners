from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Float
DATABASE_URL = (
    "postgresql://postgres:Ruc%405006@localhost:5432/userbd"
)


engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()
class UserRecommendation(Base):

    __tablename__ = "recommendations"

    id = Column(Integer, primary_key=True, index=True)

    age = Column(Integer)

    income = Column(Float)

    risk = Column(String)

    investment_period = Column(Integer)

    allocation = Column(String)

    llm_response = Column(String)
Base.metadata.create_all(bind=engine)
print("table created")