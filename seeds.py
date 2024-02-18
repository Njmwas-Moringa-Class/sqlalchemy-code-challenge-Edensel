from faker import Faker
import random

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Restaurant, Review, Customer

if __name__ == '__main__':
    
    engine = create_engine('sqlite:///db/restaurants.db')
    
   
    Session = sessionmaker(bind=engine)
    session = Session()

    fake = Faker()

    for i in range(50):
        restaurant = Restaurant(
            name=fake.unique.name(),
            price=random.randint(5, 60)
        )
        session.add(restaurant)

    for i in range(25):
        customer = Customer(
            first_name=fake.name(),
            last_name=fake.name()
        )
        session.add(customer)

    session.commit()

    for restaurant in session.query(Restaurant).all():
        for _ in range(random.randint(1, 5)):
            customer = random.choice(session.query(Customer).all())
            review = Review(
                score=random.randint(0, 10),
                comment=fake.sentence(),
                restaurant=restaurant,
                customer=customer,
            )
            session.add(review)


    session.commit()
    session.close()
