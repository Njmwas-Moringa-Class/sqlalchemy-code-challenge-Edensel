#!/usr/bin/env python3
import random
import ipdb;
from models import Customer,Review,Restaurant
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker



if __name__ == '__main__':
    
    engine = create_engine('sqlite:///db/restaurants.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    ipdb.set_trace()
