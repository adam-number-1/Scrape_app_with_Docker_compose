from sqlalchemy import create_engine, Column, Integer, String, Date, inspect
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine("mysql+pymysql://root:testpwd@some-mysql:3306/scrape_data")

session = sessionmaker(bind=engine)()

base = declarative_base()

class Ad_values(base): # sqlalchemy doesn¨t like tables with no PK
    __tablename__ = "price_info"

    id = Column(String(20),name="ad_id", primary_key=True)
    price = Column(Integer, name="ad_price")
    date = Column(Date, name="date", primary_key=True)

    @classmethod
    def latest_price(cls, id: str) -> int | None:

        price: int
        
        try:
            price = (
                session
                .query(cls)
                .filter(cls.id == id)    
                .order_by(cls.date.desc())    
                .first()    
                .price
                )
        except AttributeError: # that means the ad by ID was not found
            price = None
        return price


base.metadata.create_all(engine)

if __name__ == "__main__":
    # for testing stuff out
    pass

    




