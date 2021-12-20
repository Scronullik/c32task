

$(document).ready(function () {
    updateUrlList();  // when loading the home page, it will run ajax to load the list of existing links
});

$(document).on('click', '.copy button[type="button"]', function (e) {
    e.preventDefault();
    let $element = $(this);
    navigator.clipboard.writeText($element.closest('.row').find('.link').children('a').attr('href'));
});

$(document).on('click', '.edit button[type="button"]', function (e) {
    e.preventDefault();
    let $element = $(this);
    $.ajax({  // loading the link editing form
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
    $element.closest('.row').find('.link').children('a').show();  // show current link
    $element.closest('#edit_link_form').remove();  // remove the link editing form
    $('.edit').show();  // show all edit buttons that were hidden due to editing the current link
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
 * Form handler function
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
            const isErrors = responseText.includes('error');  // check the form for errors

            // always add/update forms
            if (formID === 'create_link_form') {
                $('#create_link_form_segment').html(responseText);
            }
            else if (formID === 'edit_link_form') {
                initialEditLinkForm($element, responseText);
                $element.remove();
            }

            if (!isErrors) {  // if there are no errors in the forms after sending the form and response
                deleteParamURL('page');
                updateUrlList();  // link list update
            }
        },
    });
};

/**
 * The function performs actions after loading the link editing form
 */
function initialEditLinkForm($element, responseText) {
    let $link = $element.closest('.row').find('.link');
    $link.append(responseText);  // add form
    $link.children('a').hide();  // hide the current link (will be visible in the form of editing the link)
    $('.edit').hide();  // hide all edit buttons at the time of editing the current link
}

/**
 * The function loads or updates the list of existing links
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
 * The function removes the current parameter from the url by key.
 * If there are several parameters (for example: "?tag=t_1&tag=t_2") it is possible to delete by paramValue value.
 * If paramValue is not specified, all parameters by paramKey key will be deleted.
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