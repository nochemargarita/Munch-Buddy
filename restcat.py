from model import Like
def rest_cat():
    """add restaurant and category to RestaurantCategory database."""

    like = Like.query.all()

    with open('restaurants.json', 'r') as filename:
        for item in filename:
            info = json.loads(item)
            print len(info['categories']), len(like)
            for i in range(len(info['categories'])):
                for indx in range(len(like)):
                    cat_alias = like[indx].category.cat_alias
                    if cat_alias in info['categories'][i]['alias']:
                        rest_cate = RestaurantCategory(rest_id=info['id'], cat_id=like[indx].cat_id)



rest_cat()