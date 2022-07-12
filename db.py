from sqlalchemy import create_engine
from sqlalchemy import Column, BigInteger, Text, Date
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import database_exists, create_database

# Postgres database configuration
pg_config = {
    'user': 'johnboyle',
    'password': '#Trinity13',
    'host': '127.0.0.1',
    'port': '5432',
    'db': 'swe_jobs'
}

# Postgres database connection url
url = f"postgresql://{pg_config['user']}:{pg_config['password']}@{pg_config['host']}:{pg_config['port']}/{pg_config['db']}"

# Create the database if it does not exist
if not database_exists(url):
    create_database(url)

# Create engine, session and base
engine = create_engine(url, pool_size=50, echo=False)
session = sessionmaker(bind=engine)()
Base = declarative_base()

# Create job table
class Job(Base):
    __tablename__ = 'jobs'

    id = Column(BigInteger, primary_key=True)
    title = Column(Text, nullable=False)
    company = Column(Text, nullable=False)
    location = Column(Text, nullable=False)
    description = Column(Text, nullable=False)
    link = Column(Text, nullable=False)
    date = Column(Date, nullable=False)
    createdAt = Column(Date, nullable=False)
    updatedAt = Column(Date, nullable=False)

    def __repr__(self):
        return f"User(id={self.id!r}, title={self.title!r}, company={self.company!r}, location={self.location!r}, description={self.description!r}, link={self.link!r}, date={self.date!r})"

Base.metadata.create_all(engine)