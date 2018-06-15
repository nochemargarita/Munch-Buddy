let counter = 0;
$(".image-checkbox").each(function () {
    if ($(this).find('input[type="checkbox"]').first().attr("checked")) {
        $(this).addClass('image-checkbox-checked');
    } else {
    $(this).removeClass('image-checkbox-checked');
    }
});

// sync the state to the input
$(".image-checkbox").on("click", function (evt) {
    counter += 1;

    $(this).toggleClass('image-checkbox-checked');
    let $checkbox = $(this).find('input[type="checkbox"]');
    $checkbox.prop("checked",!$checkbox.prop("checked"));
    $('.fa-check').show();

    if (counter > 4){
        $('#submit-categories').attr('hidden', false);

    };

    evt.preventDefault();
    });