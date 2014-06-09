$(document).ready(function() {
    add_cell_comment_threads();
});
var entityMap = {
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': '&quot;',
    "'": '&#39;',
    "/": '&#x2F;',
};

function escapeHtml(string) {
    return String(string).replace(/[&<>"'\/]/g, function(s) {
        return entityMap[s];
    });
}

function add_cell_comment_threads() {
    // Wrap output cells for proper output
    $.map($('.output_wrapper'), function(x) {
        $(x).addClass('col-md-8');
    });
    // Add comment sections to cells
    $.map($('.cell'), function(x) {
        $(x).addClass('row');
        $(x).addClass('clearfix')
        $(x).html("<div class='col-md-8 cell_content'>" + $(x).html() + "</div>");
        $(x).append("<div class='comments col-md-4' id='" + x.id + "_comments' ></div>");
    });
    // Setup comment sections and pull data from server
    $.map($('.comments'), function(x) {
        parent_cell = $(x).parent()[0]
        cell_id = parent_cell.id.match(/^cell_([0-9]+)/)[1]
        $(x).append("<div class='content_area media'></div>")
        $(x).append("<div class='tools'></div>")
        add_new_comment_button_to_cell(cell_id)
        retrieve_comment_data(cell_id)
    });
}

function retrieve_comment_data(cell_id) {
    $("#cell_" + cell_id + "_comments > .content_area").first().empty()
    $.getJSON("/nb/" + file_id + "/cs/" + cell_id, function(json) {
        $.each(json.comment_data, function(i, data) {
            inner_content = "\
            <h4 class='media-heading'>" + escapeHtml(data.username) + "</h4>\
            <div class='media-body'>" + escapeHtml(data.content) + '</div>'
            $("#cell_" + cell_id + "_comments > .content_area").first().append("<div class='comment media-object'>" + inner_content + "</div>")
        });
    })
}

function add_new_comment_button_to_cell(cell_id) {
    $("#cell_" + cell_id + "_comments > .tools").first().append("\
        <a href='javascript:add_create_comment_form(" + cell_id + ");' class='comment-button'>\
        <span class='glyphicon glyphicon-comment'></span>" + "\
        <br/>");
    // $("#cell_" + cell_id + "_comments > .tools").first().append("<a href='javascript:add_create_comment_form(" + cell_id + ");' class='btn btn-sm btn-default'><span class='glyphicon glyphicon-plus'></span></a>" + "<br/>");
}

function remove_comment_form(cell_id) {
    $("#cell_" + cell_id + "_comments > .tools").first().empty()
    add_new_comment_button_to_cell(cell_id)
}

function add_create_comment_form(cell_id) {
    cell = $("#cell_" + cell_id + "_comments > .tools").first()
    var form_id = "new_comment_form_" + cell_id
    var url = "/upload/nb/" + file_id + "/cs/" + cell_id;
    $(cell).html("\
        <form name='add_comment' \
            action='/upload/nb/" + file_id + "/cs/" + cell_id + "' \
            class='form' id='" + form_id + "'>\
        <textarea name='comment' class='form-control' rows='4' placeholder='Leave a comment'></textarea>\
        <br />\
        <input type='hidden' name='cell_contents'></input>\
        <input type='submit' value='Submit' class='btn btn-default'></input>&nbsp;\
        <input type='submit' value='Cancel' class='btn btn-default'></input>&nbsp;");
    // <a href='javascript:remove_comment_form(" + cell_id + ");' class='btn btn-default' role='button'>Cancel</a></form>");
    $("#" + form_id).find("input[value='Cancel']").click(function(event) {
        event.preventDefault();
        remove_comment_form(cell_id)
    });
    $("#" + form_id).find("input[value='Submit']").click(function(event) {
        event.preventDefault();
        var $form = $("#" + form_id),
            comment_text = $form.find("textarea[name='comment']").val(),
            url = $form.attr("action");
        console.log(comment_text)
        // Send the data using post
        var posting = $.post(url, {
            'comment': comment_text
        });
        // Put the results in a div
        posting.done(function(data) {
            remove_comment_form(cell_id)
            retrieve_comment_data(cell_id)
        });
    });
    // $("#" + form_id).find("input[value='Submit']").click(function(event){
    //     event.preventDefault();
    //     console.log(event);
    //     // var $form = $(this),
    //     //     comment_text = $form.find("textarea[name='comment']").val(),
    //     //     url = $form.attr("action");
    //     // // Send the data using post
    //     // var posting = $.post(url, {
    //     //     'comment': comment_text
    //     // });
    //     // // Put the results in a div
    //     // posting.done(function(data) {
    //     //     remove_comment_form(cell_id)
    //     //     retrieve_comment_data(cell_id)
    //     // });
    //     // return false;
    // });
    // $("#" + form_id).submit(function(event) {
    //     event.preventDefault();
    //         console.log(event);
    //     var $form = $(this),
    //         comment_text = $form.find("textarea[name='comment']").val(),
    //         url = $form.attr("action");
    //     // Send the data using post
    //     var posting = $.post(url, {
    //         'comment': comment_text
    //     });
    //     // Put the results in a div
    //     posting.done(function(data) {
    //         remove_comment_form(cell_id)
    //         retrieve_comment_data(cell_id)
    //     });
    // });
}