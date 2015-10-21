/**
 * Created by omairshamshir on 9/22/15.
 */


function open_crawl_modal(crawl_type) {
    $("#crawl_button").prop('disabled', false);
    $('#myModal').modal('show');
    var crawl_msg = 'Start ' + crawl_type + ' Crawl';
    $('#crawl_type').val(crawl_type);
    $("#crawl_modal_header").text(crawl_msg);
}


function send_crawl_request() {
    $("#crawl_button").prop('disabled', true);
    var crawl_type = $('#crawl_type').val();
    $.ajax({
        url: '/control/crawl',
        method: 'POST',
        data: $('#crawl-form').serialize()
    }).done(function (response) {
        location.href = "http://54.225.86.142:8085/" + response;
    }).fail(function () {

    });
}