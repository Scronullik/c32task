

$(document).ready(function () {
    updateUrlList();  // при загрузки home page выполняем ajax чтобы подгрузить список существующих ссылок
});

$(document).on('click', '.copy button[type="button"]', function (e) {
    e.preventDefault();
    let $element = $(this);
    navigator.clipboard.writeText($element.closest('.row').find('.link').children('a').attr('href'));
});

$(document).on('click', '.edit button[type="button"]', function (e) {
    e.preventDefault();
    let $element = $(this);
    $.ajax({  // загружаем форму редактирования ссылки
        type: 'get',
        url: $element.data('action-url'),
        success: function (responseText) {
            initialEditLinkForm($element, responseText);
        },
    });
});

$(document).on('click', '#edit_link_form .cancel_button', function (e) {
    e.preventDefault();
    let $element = $(this);
    $element.closest('.row').find('.link').children('a').show();  // показываем текущую ссылку
    $element.closest('#edit_link_form').remove();  // удаляем форму редактирования
    $('.edit').show();  // показываем все кнопки редатирования, которые были скрыты из-за редактирования текущей ссылки
});


$(document).on('submit', '#create_link_form', function (e) {
    formsHundler(this, e);
});

$(document).on('submit', '#edit_link_form', function (e) {
    formsHundler(this, e);
});


$(document).on('click', '.previous_page', function (e) {
    e.preventDefault();
    updateUrlList();
});

$(document).on('click', '.next_page', function (e) {
    e.preventDefault();
    updateUrlList();
});

/**
 * Функция-обработчик форм
 */
function formsHundler(element, e) {
    e.preventDefault();
    let $element = $(element);
    $.ajax({
        type: 'post',
        url: $element.attr('action'),
        data: $element.serialize(),
        success: function (responseText) {

            const formID = $element.attr('id');
            const isErrors = responseText.includes('error');  // проверяем форму на наличие ошибок

            // всегда добаляем/обноляем формы
            if (formID === 'create_link_form') {
                $('#create_link_form_segment').html(responseText);
            }
            else if (formID === 'edit_link_form') {
                initialEditLinkForm($element, responseText);
                $element.remove();
            }

            if (!isErrors) {  // если после отправки формы и ответа, ошибок в формах нету
                deleteParamURL('page');
                updateUrlList();  // обновляем список ссылок
            }
        },
    });
};

function initialEditLinkForm($element, responseText) {
    let $link = $element.closest('.row').find('.link');
    $link.append(responseText);
    $link.children('a').hide();  // скрываем ссылку (будет видна в форме)
    $('.edit').hide();  // скрываем все кнопки редактирования на момент редактирования текущей ссылки
}

/**
 * Функция загружает или обновленяет список существующих ссылок
 */
function updateUrlList() {
    let $linkListSegment = $('#link_list_segment');
    let params = {};
    const page = getParam('page');
    if (!page || page == 1) {
        deleteParamURL('page');
    }
    else {
        params.page = page;
    }
    $.ajax({
        type: 'get',
        url: $linkListSegment.data('action-url'),
        data: params,
        success: function (responseText) {
            $linkListSegment.html(responseText);
        },
    });
};


/**
 * based code on https://github.com/Scronullik/whatyouknow/blob/8de31ff095141c850e33349d8a47cb4cf3e6be0a/apps/core/static/core/js/urls.js#L31
 * @param {string} key 
 * @param {string} url 
 * @return
 */
function getParam(key, url = location.href) {
    let u = new URL(url);
    return u.searchParams.get(key);
}


/**
 * based code on https://github.com/Scronullik/whatyouknow/blob/8de31ff095141c850e33349d8a47cb4cf3e6be0a/apps/core/static/core/js/urls.js#L85
 * Функция удаляет текущий парамер из юрла по ключу. Если параметров несколько (например: "?tag=t_1&tag=t_2") возможно удаление по значению paramValue.
 * Если paramValue не указан, будет удалёны все параметры по ключу paramValue. 
 * @param {string} paramKey 
 * @param {*} paramValue 
 * @param {string} url 
 */
function deleteParamURL(paramKey, paramValue = null, url = location.href) {
    let u = new URL(url);
    let list = u.searchParams.getAll(paramKey);

    if (paramValue && list.length > 1) {
        const index = list.indexOf(paramValue);
        if (list.indexOf(paramValue) > -1) {
            list.splice(index, 1);
        }
        u.searchParams.delete(paramKey);
        list.map(function (item, index) {
            u.searchParams.append(paramKey, item);
        });
    }
    else {
        u.searchParams.delete(paramKey);
    }

    history.pushState(null, null, u);
}