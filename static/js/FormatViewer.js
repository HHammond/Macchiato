$(document).ready(function() {
    add_cell_comment_threads();
});

function add_cell_comment_threads() {
    $.map($('.output_wrapper'), function(x) {
        $(x).addClass('col-md-8');
    });
    $.map($('.output_wrapper'), function(x) {
        $(x).addClass('col-md-8');
    });
    $.map($('.cell'), function(x) {
        $(x).addClass('row');
        $(x).html("<div class='col-md-8' style='margin: 0;padding:0'>" + $(x).html() + "</div>");
        $(x).append("<div class='comments col-md-4' id='" + x.id + "_comments' ></div>");
    });
    $.map($('.comments'), function(x) {
        parent_cell = $(x).parent()[0]

        x.innerHTML = "\
        <a href='#' class='btn btn-xs btn-default'>\
        <span class='glyphicon glyphicon-comment'></span>\
        </a>\
        <br/>\
        <br/>\
        ";

        // $(x).html('<h3>Comments for ' + parent_cell.id + '</h3>')
        $.ajax({
            type: "GET",
            url: "/cs/" + parent_cell.id,
            dataType: "text",
            success: function(u) {
                x.innerHTML = '<p>' + u + '</p>'+x.innerHTML
            }
        });

    });
}

