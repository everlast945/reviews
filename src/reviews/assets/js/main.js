document.addEventListener('DOMContentLoaded', function() {

    // Событие при выборе региона на форме
    var ajaxElements = document.querySelectorAll('.js-select-region-ajax');
    [].forEach.call(ajaxElements, function (ajaxElement) {
        ajaxElement.addEventListener('change', function (e) {
            var url = ajaxElement.getAttribute('data-url');
            var select_value = ajaxElement.options[ajaxElement.selectedIndex].value;
            url += select_value + '/';
            sender.ajaxWithAction(url, 'GET', actions.load_cities_choices);
        });
    });


    // Событие ко кнопке удаления комментария
    var commentDeleteButtons = document.querySelectorAll('.js-comment-delete');
    [].forEach.call(commentDeleteButtons, function (commentDeleteButton) {
        commentDeleteButton.addEventListener('click', function (e) {
            var url = commentDeleteButton.getAttribute('data-url');
            sender.ajaxWithAction(url, 'DELETE', actions.comment_ajax_delete());
        });
    });
});
