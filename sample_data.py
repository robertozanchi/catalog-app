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

# Add sample user
John = User(name="John Smith", email="john@smith.com",
            picture="https://upload.wikimedia.org/wikipedia/commons/2/29/Houghton_\
            STC_22790_-_Generall_Historie_of_Virginia%2C_New_England%2C_and_the_Su\
            mmer_Isles%2C_John_Smith.jpg")

# Add sample items
Snowboard = Item(name="Snowboard",category_id="",user_id="", description="", image="")
session.add(Snowboard)

session.commit()