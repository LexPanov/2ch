$(function () {
    var active_id = '';
    var $label_top = $('.reply-label-top');
    var $label_bot = $('.reply-label-bot');
    var text_open = $label_top.first().text();
    var text_close = 'Закрыть форму постинга';
    var $postform = $('#postform');
    $('.makaba').on('click', '.reply-label-top', function(){
        if(active_id == 'bot') $label_bot.text(text_open);
        if(active_id == 'top') {
            $postform.hide();
            $label_top.text(text_open);
            active_id = '';
        }else{
            $('#TopNormalReply').after($postform);
            $postform.show();
            $label_top.text(text_close);
            active_id = 'top';
        }
    });
});