#!/usr/bin/env python3
import random
from sqlalchemy import create_engine
from models import Customer,Review,Restaurant
from sqlalchemy.orm import sessionmaker
import ipdb;


if __name__ == '__main__':
    
    engine = create_engine('sqlite:///restaurants.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    ipdb.set_trace()
