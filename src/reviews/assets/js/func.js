var sender = {
    ajaxByUrl: function (url, method, action) {
        var request=new XMLHttpRequest();
        request.open(method, url);
        // Задаём функцию, которая будет вызываться при изменении состояния готовности запроса
        request.onreadystatechange = function () {
            // Проверяем состояние готовности и статус запроса
            if (request.readyState === 4 && request.status === 200) {
                // Десериализуем полученную JSON строку в объект JavaScript
                action(request.responseText);
            }
        };
        request.send();
    },
};

var actions ={
    load_cities_choices: function (html) {
        var select_city = document.querySelector('#select-city');
        select_city.innerHTML = html;
    },
    comment_ajax_delete: function (html) {
        window.location = '/comments/';
    },
};