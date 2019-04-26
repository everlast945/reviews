document.addEventListener('DOMContentLoaded', function() {
    var ajaxElements = document.querySelectorAll('.js-select-region-ajax');
    [].forEach.call(ajaxElements, function (ajaxElement) {
        ajaxElement.addEventListener('change', function (e) {
            var url = ajaxElement.getAttribute('data-url');
            var select_value = ajaxElement.options[ajaxElement.selectedIndex].value;
            url += select_value + '/';
            sender.ajaxByUrl(url, 'GET', actions.load_cities_choices);
        });
    });

    var commentDeleteButtons = document.querySelectorAll('.js-comment-delete');
    [].forEach.call(commentDeleteButtons, function (commentDeleteButton) {
        commentDeleteButton.addEventListener('click', function (e) {
            var url = commentDeleteButton.getAttribute('data-url');
            sender.ajaxByUrl(url, 'DELETE', actions.comment_ajax_delete());
        });
    });
});
