from faker import Faker
import random

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Restaurant, Review, Customer

if __name__ == '__main__':
    # Create SQLAlchemy engine
    engine = create_engine('sqlite:///db/restaurants.db')
    
    # Bind the engine to a session
    Session = sessionmaker(bind=engine)
    session = Session()

    # Initialize Faker to generate fake data
    fake = Faker()

    # Generate fake data for restaurants
    for i in range(50):
        restaurant = Restaurant(
            name=fake.unique.name(),
            price=random.randint(5, 60)
        )
        session.add(restaurant)

    # Generate fake data for customers
    for i in range(25):
        customer = Customer(
            first_name=fake.name(),
            last_name=fake.name()
        )
        session.add(customer)

    # Commit the added restaurants and customers
    session.commit()


    # Generate fake data for reviews
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


    # Commit the added reviews
    session.commit()

    # Close the session
    session.close()
