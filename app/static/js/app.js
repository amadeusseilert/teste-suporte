
function makeGuess(post_id, guess) {
    $("#guess-form").ajaxSubmit({
        url: "/home/" + post_id + "/" + guess,
        type: "post",
        success: function(data){
            data = JSON.parse(data)
            $('#button-group-' + data['component']).remove();
            $('#true-counter-' + data['component']).text(data['tg']);
            $('#false-counter-' + data['component']).text(data['fg']);
        }
    })
}