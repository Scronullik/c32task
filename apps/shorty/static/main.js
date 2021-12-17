

$(document).ready(function () {
    updateUrlList();
});

$(document).on('click', '.copy button[type="button"]', function (e) {
    e.preventDefault();
    let $element = $(this);
    navigator.clipboard.writeText($element.closest('.row').find('.link').children('a').attr('href'));
});

$(document).on('click', '.edit button[type="button"]', function (e) {
    e.preventDefault();
    let $element = $(this);
    $.ajax({
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
    $element.closest('.row').find('.link').children('a').show();
    $element.closest('#edit_link_form').remove();
    $('.edit').show();
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

function formsHundler(element, e) {
    e.preventDefault();
    let $element = $(element);
    $.ajax({
        type: 'post',
        url: $element.attr('action'),
        data: $element.serialize(),
        success: function (responseText) {
            const formID = $element.attr('id');
            const isErrors = responseText.includes('error');
            if (formID === 'create_link_form') {
                $('#create_link_form_segment').html(responseText);
            }
            else if (formID === 'edit_link_form') {
                initialEditLinkForm($element, responseText);
                $element.remove();
            }
            if (!isErrors) {
                deleteParamURL('page');
                updateUrlList();
            }
        },
    });
};

function initialEditLinkForm($element, responseText) {
    let $link = $element.closest('.row').find('.link');
    $link.append(responseText);
    $link.children('a').hide();
    $('.edit').hide();
}

function updateUrlList() {
    let $linkListSegment = $('#link_list_segment');
    let params = {};
    const page = getParam('page');
    if (page == 1) {
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

function getParam(key, url = location.href) {
    let u = new URL(url);
    return u.searchParams.get(key);
}

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