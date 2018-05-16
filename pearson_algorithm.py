# In the current session, get user id
# query the like table and get all data
# then use that q to look for the categories that the current user liked
# category chosen, current user, user1


"""from math import sqrt
user_1 = [2, 1, 2, 2, 1]
user_2 = [1, 2, 2, 1, 2]
user_3 = [2, 1, 1, 2, 1]


zp = zip(user_1, user_3)
ser_1, ser_2 = zip(*zp)
sum_1 = sum(ser_1)
sum_2 = sum(ser_2)
sq_1 = sum([n * n for n in ser_1])
sq_2 = sum([n * n for n in ser_2])
prod_sum = sum([n * m for n, m in zp])
size = len(zp)
numerator = prod_sum - ((sum_1 * sum_2) / size)
denom = sqrt((sq_1 - (sum_1 * sum_1)/size) * (sq_2 - (sum_2 * sum_2)/size))
print numerator / denom"""
    
NUM_PEOPLE_MATCHED = 5
def get_all_liked_cat():
    """query the database and get all the info on that table.

        use 1 for categories that were not chosen.
        use 2 for categories that were chosen.

    """
    current_user_id = session.get('user_id')
    current_user = []
    users = {}
    
    like = Like.query.all()
    user_liked = Like.query.filter(Like.user_id == current_user_id).all()

    while len(users) <= NUM_PEOPLE_MATCHED:
        for item in like:
            if current_user_id != item.user_id:
                if item.user_id 
                users[item.user_id] = 
