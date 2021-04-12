'use strict'

let url_block, btn_url, flag;
flag = false;
url_block = $('.url_block');//получения блоков с классом '.url_block'

btn_url = $('.btn_url ');//получения блоков с классом '.btn_url '
$(document).ready(function(){//при готовности документа скрыть все подвкладки
    url_block.each(function(){
        $(this).hide();
    });
})


btn_url.on('click', function(e){//при нажатии меняю класс
    let el = e.target.id;
    btn_url.filter(`#${el}`).toggleClass('active');
    if(btn_url.filter(`#${el}`).hasClass('active')){
        url_block.filter(`#${el}`).fadeIn();
        for(let i = 0; i < 4; i++){
            if( i != el){
                url_block.filter(`#${i}`).fadeOut();
                btn_url.filter(`#${i}`).removeClass('active');
            }
        }
    }else{
        url_block.filter(`#${el}`).fadeOut();
    }

});