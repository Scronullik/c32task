

$(document).ready(function () {
    updateUrlList();
});

$(document).on('click', '.copy_button', function (e) {
    e.preventDefault();
    let $element = $(this);
    navigator.clipboard.writeText($element.closest('.row').find('.link').children('a').attr('href'));
});

$(document).on('click', '.edit_button', function (e) {
    e.preventDefault();
    let $element = $(this);
    $.ajax({
        type: 'get',
        url: $element.data('action-url'),
        success: function (responseText) {
            initEditLinkForm($element, responseText);
        },
    });
});

$(document).on('click', '.cancel_edit_button', function (e) {
    e.preventDefault();
    let $element = $(this);
    $element.closest('.row').find('.link').children('a').show();
    $element.closest('#edit_link_form').remove();
    $('.edit').show();
});

$(document).on('submit', '#edit_link_form', function (e) {
    e.preventDefault();
    let $element = $(this);
    $.ajax({
        type: 'post',
        url: $element.attr('action'),
        data: $element.serialize(),
        success: function (responseText) {
            if (responseText.includes($element.attr('id'))) {
                initEditLinkForm($element, responseText);
                $element.remove();
            }
            else {
                $('#link_list_segment').html(responseText);
            }
        },
    });
});

function initEditLinkForm($element, responseText) {
    let $link = $element.closest('.row').find('.link');
    $link.children('a').hide();
    $link.append(responseText);
    $('.edit').hide();
}

function updateUrlList() {
    let $linkListSegment = $('#link_list_segment');
    $.ajax({
        type: 'get',
        url: $linkListSegment.data('action-url'),
        success: function (responseText) {
            $linkListSegment.html(responseText);
        },
    });
};
