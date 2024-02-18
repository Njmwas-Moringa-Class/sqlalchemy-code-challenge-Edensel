from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine('sqlite:///restaurants.db', echo=True)


Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()


class Review(Base):
    __tablename__ = 'reviews'
    id = Column(Integer, primary_key=True)
    star_rating = Column(Integer)
    restaurant_id = Column(Integer, ForeignKey('restaurants.id'))
    customer_id = Column(Integer, ForeignKey('customers.id'))

    restaurant = relationship("Restaurant", back_populates="reviews")
    customer = relationship("Customer", back_populates="reviews")

    def customer(self):
        return self.customer

    def restaurant(self):
        return self.restaurant

    def full_review(self):
        return f"Review for {self.restaurant.name} by {self.customer.full_name()}: {self.star_rating} stars."


class Restaurant(Base):
    __tablename__ = 'restaurants'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Integer)
    reviews = relationship("Review", back_populates="restaurant")

    def reviews(self):
        return self.reviews

    def customers(self):
        return [review.customer for review in self.reviews]

    @classmethod
    def fanciest(cls):
        return session.query(cls).order_by(cls.price.desc()).first()

    def all_reviews(self):
        return [review.full_review() for review in self.reviews]


class Customer(Base):
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    reviews = relationship("Review", back_populates="customer")

    def reviews(self):
        return self.reviews

    def restaurants(self):
        return [review.restaurant for review in self.reviews]

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def favorite_restaurant(self):
        reviews = sorted(self.reviews, key=lambda x: x.star_rating, reverse=True)
        return reviews[0].restaurant if reviews else None

    def add_review(self, restaurant, rating):
        review = Review(restaurant=restaurant, customer=self, star_rating=rating)
        self.reviews.append(review)

    def delete_reviews(self, restaurant):
        for review in self.reviews:
            if review.restaurant == restaurant:
                self.reviews.remove(review)
                session.delete(review)


Base.metadata.create_all(engine)
