function displayRestaurants(results) {
    let restaurants = results;
    $('#restaurants').html(restaurants);

    for (let restaurant in restaurants) {
        $('#restaurants').append(`<p id=${restaurant}> 
                                      <img src=${restaurants[restaurant]['image']} width="50px" height="50px"> 
                                      <a href=${restaurants[restaurant]['url']}>
                                        ${restaurants[restaurant]['title']}
                                      </a>
                                      <button id=${restaurant} onClick='deleteRestaurant(this.id)'>DELETE</button>
                                  </p>
                                `);

    }

}

function getRestaurants() {
    $.get('/restaurants.json', displayRestaurants);
}

getRestaurants();


function deleteRestaurant(restaurant){
    $.post('/delete_liked_restaurant', {data: restaurant}, function(data){
        $(`p#${data}`).empty()
    });
}

