

from mongo import get_db,CRUD
treasure_db=get_db("treasure")

treasure_industry=CRUD(treasure_db,"industry")
treasure_industry_detail=CRUD(treasure_db,"industry_detail")