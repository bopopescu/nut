var elems = Array.prototype.slice.call(document.querySelectorAll('.js-switch'));

function postSuccess(data){
    console.log(data);
}
function postFail(data){
    console.log(data);
}

function switchChange(){
    console.log(this);
    console.log(this['data-id']);
    console.log($(this).prop('checked'));
    console.log($(this).attr('data-id'));
    var tag_id = $(this).attr('data-id');
    var url = '/management/t/' + tag_id + '/topArticleTag/' ;
    var data =  {id:tag_id ,isTopArticleTag: $(this).prop('checked')};

    when($.ajax({
        type:'POST',
        url: url,
        data: data,
    })).then(
        postSuccess,
        postFail
    );
}

elems.forEach(function(ele) {
  var switchery = new Switchery(ele);
      ele.onchange = switchChange;
});