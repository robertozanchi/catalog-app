from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Category, Base, Item, User
 
engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine
 
DBSession = sessionmaker(bind=engine)
session = DBSession()


# Add Categories
Soccer = Category(name="Soccer")
session.add(Soccer)

Basketball = Category(name="Basketball")
session.add(Basketball)

Baseball = Category(name="Baseball")
session.add(Baseball)

Frisbee = Category(name="Frisbee")
session.add(Frisbee)

Snowboarding = Category(name="Snowboarding")
session.add(Snowboarding)

Climbing = Category(name="Climbing")
session.add(Climbing)

Foosball = Category(name="Foosball")
session.add(Foosball)

Skating = Category(name="Skating")
session.add(Skating)

Hockey = Category(name="Hockey")
session.add(Hockey)


# Add sample items
Snowboard = Item(name="Snowboard",category_id="5",user_id="1", description="Snowboards\
                 are boards that are usually the width of one's foot longways, with \
                 the ability to glide on snow.", image="https://upload.wikimedia.org/wikipedia/commons/5/55/Snowboard_with_Strap-In_Bindings_and_Stomp_Pad.png")
session.add(Snowboard)

Soccer_shoes = Item(name="Soccer Shoes",category_id="1",user_id="1", description="Item of \
	                footwear worn when playing football", image="https://upload.wikimedia.org/wikipedia/commons/9/94/Nike_Zoom_Air_Football_Boots.jpg")
session.add(Soccer_shoes)

session.commit()