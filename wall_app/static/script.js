$(document).ready(function(){
    $("#post_form").submit(function(e){
        e.preventDefault();
        $.ajax({
            url: '/wall/post_message_ajax',
            method: 'post',
            data: $(this).serialize(),
            success: function(response){
                $("#messages").prepend(response);
                $("#post_form")[0].reset();
            }
        });
    });
    $("form").submit(function(e){
        e.preventDefault();
        var id = $(this).attr("id");
        var num = "";
        for(i = id.length - 1; i >= 0; i--){
            if(id[i] != "-"){
                num = id[i] + num;
            } else {
                break;
            }
        }
        $.ajax({
            url:'/wall/post_comment_ajax',
            method: 'post',
            data: $(this).serialize(),
            success: function(response){
                $(`#comments-${num}`).prepend(response);
                $(`#comment_form-${num}`)[0].reset();
            }
        });
    });
    $("button").click(function(e){
        e.preventDefault();
        $.ajax({
            url: "https://cat-fact.herokuapp.com/facts/random?animal_type=cat&amount=5",
            method: "get",
            success: function(response){
                console.log(response);
                var html = "";
                for(var fact of response){
                    html += `<p>${fact.text}</p>`;
                }
                $("#facts").html(html);
            }
        });
    });
});                     