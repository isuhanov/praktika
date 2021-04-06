'use strict'

let url_block, btn_url, flag;
flag = false;
url_block = $('.url_block');

btn_url = $('.btn_url ');
$(document).ready(function(){
    url_block.each(function(){
        $(this).hide();
    });
})


// console.log(btn_url);
btn_url.on('click', function(e){
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



    // btn_url.filter(`#${el}`).toggleClass('active');
    // btn_url.each(function(){
    //     if( $(this).hasClass('actice')){
    //         url_block.each(function(){
    //             $(this).fadeOut();
    //         });
    //         url_block.filter(`#${el}`).fadeIn();
    //     }else{
    //         url_block.each(function(){
    //             $(this).fadeOut();
    //         });
    //     }
    // })


    // if(flag === false){

    //     url_block.each(function(){
    //         $(this).fadeOut();
    //     });

        
    //     let el = e.target.id;
    //     console.log(el.type);
    //     btn_url.filter(`#${el}`).toggleClass('active');
    //     url_block.filter(`#${el}`).fadeIn();
    //     console.log(url_block);
    //     flag = true;

    // }else if(flag === true){
    //     let el = e.target.id;
        
    //     btn_url.each(function(){
    //         $(this).removeClass('active');
    //     }); 

    //     btn_url.filter(`#${el}`).toggleClass('active');
    //     console.log(el.type);
    //     url_block.filter(`#${el}`).fadeOut();
    //     console.log(url_block);
    //     flag = false;

    // }
});