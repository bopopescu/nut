/**
 * Created by edison on 14-9-21.
 */


/* Simple JavaScript Inheritance
 * By John Resig http://ejohn.org/
 * MIT Licensed.
 */
// Inspired by base2 and Prototype
(function(){
  var initializing = false, fnTest = /xyz/.test(function(){xyz;}) ? /\b_super\b/ : /.*/;

  // The base Class implementation (does nothing)
  this.Class = function(){};

  // Create a new Class that inherits from this class
  Class.extend = function(prop) {
    var _super = this.prototype;

    // Instantiate a base class (but only create the instance,
    // don't run the init constructor)
    initializing = true;
    var prototype = new this();
    initializing = false;

    // Copy the properties over onto the new prototype
    for (var name in prop) {
      // Check if we're overwriting an existing function
      prototype[name] = typeof prop[name] == "function" &&
        typeof _super[name] == "function" && fnTest.test(prop[name]) ?
        (function(name, fn){
          return function() {
            var tmp = this._super;

            // Add a new ._super() method that is the same method
            // but on the super-class
            this._super = _super[name];

            // The method only need to be bound temporarily, so we
            // remove it when we're done executing
            var ret = fn.apply(this, arguments);
            this._super = tmp;

            return ret;
          };
        })(name, prop[name]) :
        prop[name];
    }
    // The dummy class constructor
    function Class() {
      // All construction is actually done in the init method
      if ( !initializing && this.init )
        this.init.apply(this, arguments);
    }
    // Populate our constructed prototype object
    Class.prototype = prototype;

    // Enforce the constructor to be what we expect
    Class.prototype.constructor = Class;

    // And make this class extendable
    Class.extend = arguments.callee;

    return Class;
  };
})();


function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


function clearUserInputString(str){
    str = str.replace(/(\s+)/mg,' ');
    str = str.replace(/([><:$*&%])/mg, '');
    return str.trim();
}

var csrftoken = getCookie('csrftoken');
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});



(function ($, document, window) {


    var AjaxLoader = Class.extend({
        init:function(options){
            this.loading = false ;
            this.attach();
        },
        attach: function(){
            this.scrollHandler =this._handleScroll.bind(this);
            $(window).scroll(this.scrollHandler);
        },

        detach: function(){
            $(window).off('scroll', this.scrollHandler);
        },
        loadNextBatch:function(){
            jQuery.when(
                    this.beginLoad()
            ).then(
                    this.loadSuccess.bind(this),
                    this.loadFail.bind(this)
            );
        },
        _handleScroll: function(){
            if (this._shouldLoad()){
                this.loadNextBatch();
            }else{
                return ;
            }
        },
        _shouldLoad: function(){
            if (this.loading) {
                return false;
            }
           // use fast dom ?
           if (($(window).height() + $(window).scrollTop()) < ($(document).height()-155)){
               return false;
           }
           return  true;
        },

        getRequestUrl: function(){
            return this.request_url;
        },

        getData: function(){
            throw new Error('not implemented');
            return null;
        },
        beginLoad: function(){
            this.loading = true;
            var _url = this.getRequestUrl();
            var _data = this.getData();
            return $.ajax({
                url : _url ,
                data : _data,
                method: 'GET'
            });
        //    return a promise , like an ajax() here

        },
        loadSuccess: function(data){
            console.log(data);
            this.loading = false;

        },
        loadFail: function(data){
            //console.log(data);
            // ajax call fail , maybe later
            console.log('loading failed ');
            this.loading = false;
        }
    });

    var RelatedArticleLoader = AjaxLoader.extend({
        init: function(){
            this._super();
            this.current_page = 1 ;
        },
        getRequestUrl: function(){
            return window.location.pathname;
        },
        getData: function(){
            return {
                page: this.current_page + 1,
                target: 'related_article'
            };
        },
        loadSuccess: function(data){
            if (data.errors == 0){
                $('.more-article-wrapper:last-child').after(data['html']);
                this.current_page++;
                this.loading = false;
                if (!(data.has_next_page)){
                    this.handleLastPage();
                }
            }else{
                console.log('load error');
            }
            //console.log(data);
            console.log('load related article success');

        },
        handleLastPage:function(){
            this.detach();
        },

    });

    var ArticleLoader = AjaxLoader.extend({
        request_url: '/articles/',
        init: function(){
            this._super();
            this.current_page = 1;
            $('.load-more-button').click(this.loadNextBatch.bind(this));

        },
        getData: function(){
            return {
                refresh_time : this.getRefreshTime(),
                page :  this.current_page + 1,
            }
        },
        loadSuccess: function(data){
            if (data['errors'] === 0){
                 $(data['html']).appendTo($('#selection_article_list'));
                 if(data['has_next_page'] === false){
                     this.handleLastPage();
                 }
            }else{
            //TODO: handle fail load
            }
            this.current_page++;
            if (this.current_page % 3 == 0 && (data['has_next_page'] === true)){
                this.showLoadButton();
            }else{
                this.hideLoadButton();
            }
            this.loading = false;
            return ;

        },
        showLoadButton:function(){
            $('.load-more-button').show();
        },
        hideLoadButton:function(){
             $('.load-more-button').hide();
        },
        handleLastPage:function(){
            this.detach();
            this.hideLoadButton();
        },
        getRefreshTime: function(){
           return  $('#selection_article_list').attr('refresh-time');
        },

        _shouldLoad: function(){
            var page_condition = (this.current_page > 0) && (this.current_page % 3 != 0);
            return page_condition && this._super();
        },



    });



    var RecommendArticleLoader = AjaxLoader.extend({
        request_url:'recommend'
    });

    function show_sns_page_dot(){
            $('.nav-user-actions .round').css({display:'inline-block'});
            $('.setting-list .round').css({display: 'inline-block'});
    };
    function hide_sns_page_dot(){
            $('.nav-user-actions .round').css({display:'none'});
            $('.setting-list .round').css({display: 'none'});

    };
    var util = {
        handlePageScroll: function(){
            var last_scroll = 0 ;

            var fix_sidebar = $('#sidebar_fix');
            var footer = $('#guoku_footer');

            if(!fix_sidebar.length) return;

            fix_sidebar.css({display:'none'});

            function handleScrollSideBar(){

                if(!fix_sidebar.length) return;
                var sideBarWidth = fix_sidebar.width();
                var current_scroll = $(window).scrollTop();
                if (current_scroll>2020 && (last_scroll< 2020)){
                    console.log($(window).scrollTop());
                    fix_sidebar.width(sideBarWidth);
                    fix_sidebar.css({position:'fixed', top:'60px', display:'block',opacity:0});
                    fix_sidebar.stop().animate({opacity:1})
                }
                if (current_scroll>2020 && (last_scroll >= 2020)){
                    var fixbar_bound = fix_sidebar[0].getBoundingClientRect();
                    var footer_bound = footer[0].getBoundingClientRect();
                    if (fixbar_bound.bottom >= footer_bound.top){
                        fix_sidebar.find('.remove-ready').css({opacity:0});
                    }else{
                        if (last_scroll > current_scroll){
                             fix_sidebar.find('.remove-ready').css({opacity:1});
                        }

                    }


                    //console.log(fixbar_bound.bottom  + ' : ' + footer_bound.top);
                }

                if (current_scroll < 2020 ){
                    fix_sidebar.width('auto');
                    fix_sidebar.css({position:'relative', top:'0px', opacity:0});
                }


                last_scroll = current_scroll;
            }
            $(window).scroll(handleScrollSideBar);

        },
        checkEventRead:function(){
            // add by an , for event link status check , remove the red dot if event is read.
            // the key is defined in 2 places!  DRY...
            var viewed_event_slug_cookie_key = 'viewed_event_slug_cookie_key';
            if(!newest_event_slug){
                return ;
            }
            if ($.cookie(viewed_event_slug_cookie_key) === newest_event_slug){
                //console.log('event is read!');
                jQuery('.nav [href="/event/"] .round').css({display:'none'});
            }else{
                jQuery('.nav [href="/event/"] .round').css({display:'inline-block'});
            }

            return ;
        },

        checkSNSBindVisit: function(){
            var sns_bind_page_visited_key = 'SNS_BIND_PAGE_VISITED';
            if ($.cookie(sns_bind_page_visited_key) === 'visited'){
                hide_sns_page_dot();
            }else{
                show_sns_page_dot();
            }
        },

        modalSignIn: function(html) {
            var signModal = $('#SignInModal');
            var signContent = signModal.find('.modal-content');
            if (signContent.find('.row')[0]) {
                signModal.modal('show');
            } else {
                html.appendTo(signContent);
                signModal.modal('show');
            }
        },

        //modalReport: function(html){
        //    var reportModal = $('#ReportModal');
        //    var reportContent = reportModal.find('.modal-content');
        //    if (reportContent.find('.row')[0]) {
        //              reportModal.modal('show');
        //    } else {
        //              html.appendTo(reportContent);
        //              reportModal.modal('show');
        //    }
        //},
        //初始化 tag
        initTag: function () {
            //TODO : re initTag after user post note  by an
            var array = $(".with-tag");
            for (var i=0; i<array.length; i++) {
                // replace <br> with \n
                var str = array.eq(i).html(array.eq(i).html().replace(/\<br[!>]*\>/g, "\n")).text();
                if (str == undefined)
                    continue;
                //reg to match all legal charactor in tag
                var ereg = /[#＃][0-9a-zA-Z\u4e00-\u9fff\u3040-\u30FF\u30A0-\u30FF]+/g;

                var cut = str.match(ereg);
                if (cut == null){
                    array.eq(i).html(str.replace(/\n/g, "<br>"));
                    continue;
                }

                for (var j in cut){
                    str = str.replace(cut[j], "<a class='btn-link' rel='nofollow' href='/tag/"+encodeURI(cut[j].replace(/[#＃]/,""))+"' >"+cut[j]+"</a>&nbsp;");
                }

                array.eq(i).html(str.replace(/\n/g, "<br>"));
            }
        },

        like: function (object) {
            // 喜爱 like entity
            object.find('.btn-like, .like-action').on('click', function (e) {
                var like = $(this);
                var counter = like.find('.like-count');
                var entity_id = $(this).attr("data-entity");
                var heart = like.find("i");

                ga('send', 'event', 'button', 'click', 'like', entity_id);
            //  var status = 0;
                var url ;
                if (heart.hasClass("fa-heart-o")) {
                    url = "/entity/" + entity_id + '/like/';
                } else {
                    url = "/entity/" + entity_id + '/unlike/';
                }
            // url = url.replace(/\/[01]\//,"/"+status+"/");
            // console.log(url);
                $.ajax({
                    url: url,
                    type: 'POST',
                    jsonType:'json',
                    success: function(data) {
                        var count = parseInt(counter.text()) || 0;
                        var result = parseInt(data.status);
                        if (result === 1) {
                            counter.text(" "+(count + 1));
                            heart.removeClass('fa-heart-o');
                            heart.addClass('fa-heart');
                        } else if (result === 0){
                            //console.log(result);

                            if (count >1) {
                                counter.text(" " + (count - 1));

                            }else{
                                counter.text(" ");
                            }

                            heart.removeClass('fa-heart');
                            heart.addClass('fa-heart-o');
                        } else {
                            var html = $(data);
                            util.modalSignIn(html);
                        }
                    }
                });
                e.preventDefault();
            });
        },

        follower :function () {
            $(".follow").on('click', function(e) {
                //console.log($(this));
                var $this = $(this);
                var uid = $this.attr('data-user-id');
                var status = $this.attr('data-status');

                var action_url = "/u/" + uid;

                if(status == 1) {
                    //console.log("OKOKOKOK");
                    action_url +=  "/unfollow/";

                } else {
                    action_url +=  "/follow/";
                }

                $.when($.ajax({
                    url: action_url,
                    dataType:'json',
                    method:'POST'
                })).then(function success(data){
                    console.log('success');
                    console.log(data);
                        if (data.status == 1) {
                            $this.html('<i class="fa fa-check fa-lg"></i>&nbsp; 取消关注');
                            $this.attr('data-status', '1');
                            $this.removeClass("button-blue").addClass("btn-cancel");

                        }else if (data.status == 2){
                            console.log('mutual !!!');
                             $this.html('<i class="fa fa-exchange fa-lg"></i>&nbsp; 取消关柱');
                             $this.removeClass('button-blue').addClass('btn-cancel');
                             $this.attr('data-status','1');

                        }else if (data.status == 0) {
                            $this.html('<i class="fa fa-plus"></i>&nbsp; 关注');
                        //$this.html('<span class="img_follow"></span><b>关注</b>');
                            $this.removeClass("btn-cancel").addClass("button-blue");
                            $this.attr('data-status', '0');
                        }else{
                          console.log('did not response with valid data');
                        }

                }, function fail(error){
                    console.log('failed' + error);
                    var html = $(error.responseText);
                    util.modalSignIn(html);
                });
                //$.ajax({
                //    url: action_url,
                //    dataType:'json',
                //    method: 'post',
                //    success: function(data){
                //        //console.log(data);
                //
                //        if (data.status == 1) {
                //
                //            $this.html('<i class="fa fa-check fa-lg"></i>&nbsp; 取消关注');
                //            $this.attr('data-status', '1');
                //            $this.removeClass("button-blue").addClass("btn-cancel");
                //
                //        }else if (data.status == 2){
                //            console.log('mutual !!!');
                //             $this.html('<i class="fa fa-exchange fa-lg"></i>&nbsp; 取消关柱');
                //             $this.removeClass('button-blue').addClass('btn-cancel');
                //             $this.attr('data-status','1');
                //
                //        }else if (data.status == 0) {
                //            $this.html('<i class="fa fa-plus"></i>&nbsp; 关注');
                //        //$this.html('<span class="img_follow"></span><b>关注</b>');
                //            $this.removeClass("btn-cancel").addClass("button-blue");
                //            $this.attr('data-status', '0');
                //        } else {
                //            var html = $(data);
                //            util.modalSignIn(html);
                //        }
                //    }
                //});
                //e.preventDefault();
            })
        },

        gotop: function() {

            $(".btn-top").on('click', function() {
                $("html, body").animate(
                    {scrollTop : 0}, 800
                );
                return false;
            });
        }
    };

    var createNewEntity = {
        createEntity: function () {
            var form = $('.create-entity form');
            var entityExist = $(".entity-exist");
            var addEntity = $(".add-entity");
            var addEntityNote = $(".add-entity-note");
            var imageThumbails = $(".image-thumbnails");
            //  console.log(entityExist);
            form.on('submit', function(e) {
                // have to add tool function here ,
                // TODO : refactor the whole script ! by an
                //

                function valid_url_support(url){
                    var reg= /\b(jd|360buy|tmall|taobao|95095|amazon)\.(cn|com|hk)/i;
                    return reg.test(url);

                }
                function show_url_not_support_message(){
                    $('#url_error_msg').html('请输入淘宝，天猫或京东的商品链接。');
                }
                function hide_url_not_support_message(){
                    $('#url_error_msg').html('');
                }
                function remove_current_user_input(){
                    form.find("input[name='cand_url']").val('');
                }

                hide_url_not_support_message();
                var entity_url = form.find("input[name='cand_url']").val();
                if (!valid_url_support(entity_url)){
                        show_url_not_support_message();
                        remove_current_user_input();
                    return false;
                };


            //console.log(this.action);
                addEntity.find(".title").text("");
                addEntity.find("input[name=title]").val("");

                $.ajax({
                    type: 'post',
                    url: this.action,
                    data: {cand_url:entity_url},
                    dataType:"json",
                    success : function (data) {

                        if(data.status == "EXIST") {
                            entityExist.find('a').attr("href", "/detail/"+data.data.entity_hash);
                            entityExist.slideDown();
                        } else {
                            entityExist.slideUp();

            //console.log(data.data.user_context);
                            addEntityNote.find("a img").attr("src", data.data.user_avatar);
            // addEntityNote.find('.media-heading').html(data.data.user_context.nickname);

                            var title = $.trim(data.data.title);
                            var brand = $.trim(data.data.brand);
                            addEntity.find(".title").text(title);
                            addEntity.find("input[name=title]").val(title);
                            addEntity.find("input[name=brand]").val(brand);
            //                if (data.data.taobao_id == undefined) {
            //                    title = $.trim(data.data.jd_title);
            //                    var brand = $.trim(data.data.brand);
            //                    addEntity.find(".title").text(title);
            //                    addEntity.find("input[name=title]").val(title);
            //                    addEntity.find("input[name=brand]").val(brand);
            //                } else {
            //                    $(".detail_title span:eq(1)").text(data.data.taobao_title);
            ////  $(".detail_title_input").val(data.data.taobao_title);
            //                    title = $.trim(data.data.taobao_title);
            //                    addEntity.find(".title").text(title);
            //                    addEntity.find("input[name=title]").val(title);
            //                }
                            addEntity.find(".entity-chief-img").attr('src', data.data.chief_image_url);
                            imageThumbails.html("");
                            var html_string = "";
                            for(var i=0; i < data.data.thumb_images.length; i++) {
            //  console.log(data.data.thumb_images[i]);
                                var fix = data.data.taobao_id == undefined ? "" : "_64x64.jpg";
                                if (i == 0) {
                                    html_string = "<div class='col-xs-3 col-sm-2'><div class='current-image thumbnail'><img class='img-responsive' src="
                                        + data.data.thumb_images[i] + fix + "></div></div>";
            //  imageThumbails.append(html_string);
                                    $(html_string).appendTo(imageThumbails);

                                } else {
                                    html_string = "<div class='col-xs-3 col-sm-2'><div class='thumbnail'><img class='img-responsive' src="
                                        + data.data.thumb_images[i] + fix + "></div></div>";
                                    $(html_string).appendTo(imageThumbails);
            //imageThumbails.append(html_string);
            //createNewEntity.changeChiefImage($(html_string));
            //console.log("okokoko");
                                }

                                $('<input name="thumb_images" type="hidden" value='+data.data.thumb_images[i]+'>').appendTo($(".add-entity-note form"));
                            }
                            createNewEntity.changeChiefImage(imageThumbails);

                            //if(data.data.taobao_id == undefined){
                            //$('<input type="hidden" name="origin_id" value="'+data.data.origin_id+'">').appendTo($(".add-entity-note form"));
            //  '<input type="hidden" name="jd_title" value="'+data.data.jd_title+'">').appendTo($(".add-entity-note form"));
            //$(".detail_taobao_brand").val(data.data.brand);
            //                } else {
            //                    $('<input type="hidden" name="taobao_id" value="'+data.data.taobao_id+'">' ).appendTo($(".add-entity-note form"));
            ////'<input type="hidden" name="taobao_title" value="'+data.data.taobao_title+'">').appendTo($(".add-entity-note form"));
            //                }
                            $(
                                '<input type="hidden" name="origin_id" value="'+data.data.origin_id+'">' +
                                '<input type="hidden" name="origin_source" value="'+data.data.origin_source+'">' +
                                '<input type="hidden" name="shop_link" value="'+data.data.shop_link+'">' +
                                '<input type="hidden" name="shop_nick" value="'+data.data.shop_nick+'">' +
                                '<input type="hidden" name="url" value="'+data.data.cand_url+'">' +
                                '<input type="hidden" name="price" value="'+data.data.price+'">' +
                                '<input type="hidden" name="chief_image_url" value="'+data.data.chief_image_url+'">' +
                                '<input type="hidden" name="cid" value="'+data.data.cid+'">' +
                                //'<input type="hidden" name="selected_category_id" value="'+data.data.selected_category_id+'">' +
                                '<input type="hidden" name="cand_url" value="'+data.data.cand_url+'">' +
                                '<input name="user_id" type="hidden" value="'+data.data.user_id+'">').appendTo($(".add-entity-note form")
                            );
                            addEntity.slideDown();
                            addEntityNote.slideDown();
                        }
                    },
                    error: function(error) {
                        console.log(error);
                    }
                });
                e.preventDefault();
            });
        },

        BrandAndTitle: function() {
            var addEntity = $(".add-entity");
            addEntity.find("input[name='brand']").on('input propertychange', function() {
                var brand = $(this).val();
                if (brand.length > 0) {
                    addEntity.find(".brand").html(brand + " -");
                } else {
                    addEntity.find(".brand").html(brand);
                }
            });
            addEntity.find("input[name='title']").on('input propertychange', function() {
                var title = $(this).val();
                addEntity.find(".title").html(title);
            });
        },

        changeChiefImage : function(object) {
           // console.log(object);
            var image = object.find(".thumbnail");


            image.on('click', function() {
           //     console.log($(this));
                if (!$(this).hasClass('current-image')) {
                    object.find(".current-image").removeClass('current-image');
                    $(this).addClass('current-image');
                    var image_url = $(this).find('img').attr('src');
                      //    console.log(image_url.replace('64x64', '310x310'));
                    var origin_image_url = image_url.replace('_64x64.jpg', '');
                      //    console.log(big_image_url);
                    $('.entity-chief-img').attr('src', origin_image_url);
                      //    console.log($(".add-entity-note form input[name='chief_image_url']"));
                    $(".add-entity-note form input[name='chief_image_url']").val(origin_image_url);
                }
            });
        },

        postNewEntity: function() {
            var newEntityForm = $(".add-entity-note form");

            newEntityForm.on("submit", function (e){
                var text = $.trim(newEntityForm.find("textarea[name='note_text']").val());
                if (text.length > 0) {
                    var brand = $(".add-entity input[name='brand']").val();
                    var title = $(".add-entity input[name='title']").val();
                    $('<input type="hidden" name="brand" value="'+brand+'">').appendTo(newEntityForm);
                    $('<input type="hidden" name="title" value="'+title+'">').appendTo(newEntityForm);
                    return true;
                } else {
                    $(".add-entity-note form textarea[name='note_text']").focus();
                    return false;
                }
            });
        }
    };

    var selection = {
        loadData: function () {

            var $selection = $('#selection');
            var page = $selection.parent().find('.pager');
            var counter = 1;
            page.hide();


            if ($selection[0]) {
                var flag = false;
           //     console.log(counter);
                $(window).scroll(function () {

                    if($(this).scrollTop()>100) {
                        $(".btn-top").fadeIn();
                    } else {
                        $(".btn-top").fadeOut();
                    }

                    if (counter % 3 == 0 ) {
                        page.show();
                    } else {
                        page.hide();
                    }
                    //这里临时不采用自动加载，换成分页

                    if (($(window).height() + $(window).scrollTop()) >= ($(document).height()-25) && flag == false && counter % 3 != 0) {
                      //        console.log("okokokokoko");
                      //        page.hide();
                        flag = true;
                      //        var url = window.location.href;
                        var aQuery = window.location.href.split('?');

                        var url = aQuery[0];
                        var p = 1; var c = 0;
                        if (aQuery.length > 1) {
                            var param = aQuery[1].split('&');
                            var param_p;
                      //            console.log(param);
                            if (param.length > 1) {
                      //                param_c = param[0].split('=');
                      //                c = parseInt(param_c[1]);
                                param_p = param[0].split('=');
                                p = parseInt(param_p[1]);
                            }
                        }

                      //        var last_entity = $selection.find('.entity-selection:last');
                      //        var time = last_entity.find(".timestr").attr("name");
                        var time = $selection.attr('data-refresh');
                        var data = {
                            'p': p+counter,
                            'page': p+counter,
                            't':time
                        };

                        if (c != 0 ){
                            data['c'] = c;
                        }
                      //        console.log(data);
                      //        console.log(time);
                        $.ajax({
                            url: url,
                            type: "GET",
                            data: data,
                            dataType:'json',
                            success: function(data) {
                      //                result =  $.parseJSON(data);
                      //                var status = parseInt(result.status);
                                if (data.status === 1) {
                                    var $html = $(data.data);
                      //                    $html.each(function () {
                      //                        util.showEntityTitle($(this));
                      //                    });
                                    util.like($html);
                                    $html.appendTo($selection);
                                    counter ++;
                                    flag = false;
                                }
                            }
                        });
                    }
                });
            }
           // var entities = $selection.find('.entity-selection');
           // console.log(entities);
        }

    };

    function sendReport(){
        var _form = $('#report_form_wrapper form');
        if (_form.length){
            $.when($.ajax({
                url: _form.attr('action'),
                data: _form.serialize(),
                method: 'POST',
            })).then(
                function reportSuccess(data){
                    return ;
                },
                function reportFail(){
                    return ;
                }
            );
        }

    };

    var detail = {
            initReportButton: function(){
                $('#report_trigger').click(function(){
                    var url = $(this).attr('report-url');
                    $.when($.ajax({
                        url: url,
                        method: 'GET',
                    })).then(
                        function(htmltext){
                            //this call will return a  rendered template
                            bootbox.dialog({
                               title: '举报商品',
                               message: htmltext,
                                buttons: {
                                    success:{
                                        label:'发送',
                                        className:'btn-primary',
                                        callback: sendReport
                                    },
                                }
                            });
                        },function(){
                            console.log('get report form fail ');
                        });
                });
            },
            initVisitorNote:function(){
                $('#visitor_note').click(function(){
                    $.when(
                        $.ajax({
                            url: '/login/'
                        })
                    ).then(
                        function success(data){
                            var html = $(data);
                            util.modalSignIn(html);
                        },
                        function fail(){}
                    );

                });
            },
            detailImageHover: function () {
            // 鼠标放细节图上后效果
                function findThumbImages(){
                    return $('.other-pic-list img');
                }

                findThumbImages().each(function(idx, thumb){
                    function handleTrumb(){
                        var newSrc = $(this)
                                    .prop('src')
                                    .replace(/images\/\d+\//i, 'images/310/');
                        var oldSrc = $('.detail-pic-left #buy-btn-img img').prop('src');
                        if (newSrc !== oldSrc){
                            $('.detail-pic-left #buy-btn-img img').prop('src', newSrc);
                        }
                    }
                    $(thumb).mouseenter(handleTrumb);
                    $(thumb).click(handleTrumb);
                });
        },

        shareWeibo: function() {
           // var self =
            function get_share_content(){
                var product_name = $('#detail_content .goods_name').html() + ' : ';
                var product_primary_note = $('#detail_content .common-note-list .comment_word').html();
                var content = (product_name + product_primary_note);
                    content = content.replace(/<[\s\S]*?>/g, "");
                    content = content.replace(/%/, "");
                    content = content.replace(/&nbsp;/, "");
                return content ;
            }

            $('.detail-share a').on('click', function(e){
                e.preventDefault();

                var url = location.href;
           //     console.log(url);
                var pic = $('.detail_pic img').attr("src");
           //     console.log(pic);
                var content = get_share_content();
           //     console.log(content);

           //     console.log(content);
                var param = {
                    url:url,
                    type:'3',
                    count:'0',
                    appkey:'1459383851',
                    title:content,
                    pic:pic,
                    ralateUid:'2179686555',
                    rnd:new Date().valueOf()
                };
                var temp = [];
                for( var p in param ){
                    temp.push(p + '=' + encodeURIComponent( param[p] || '' ) )
                }
                var link = "http://service.weibo.com/share/share.php?" + temp.join('&');
                window.open(link);
            });
        },

        postNote: function () {
            var $note = $(".post-note");
            var $form = $note.find("form");
            var $textarea = $form.find("textarea");
            //console.log($textarea.value);
            $textarea.on('focus', function(){
                $form.addClass('active');
            });
            //console.log($note);

            var $cancel = $form.find('.btn-cancel');
           //     console.log($cancel);
            $cancel.on('click', function() {
           //     console.log(this);
                $form.removeClass('active');
            });

            $form.on('submit', function (e) {
                if ($.trim($textarea[0].value).length === 0) {
                    $textarea[0].value = '';
                    $textarea.focus();
                } else {
                    //console.log($form.serialize());
                    $.post(this.action, $form.serialize(), function (result){
                        result = $.parseJSON(result);
                        var status = parseInt(result.status);
                        if (status === 1) {
                            var $html = $(result.data);

                            detail.clickComment($html);

                       //            console.log($html);
                      //            self.poke();
                      //            $('<div class="sep"></div>').appendTo($notes);
                            $html.appendTo($(".common-note-list"));

                            //TODO : beware , if the dom operation is slow ,\
                            // detail.update($html.parent()) may not find the parent element
                            //
                            detail.updateNote($html.find('.comment_operate'));


                            $note.parent().remove();
                            util.initTag();
                        } else if (status === 0) {
                            // error
                        }
                    });
                }

           //     console.log("OKOKOKO");
                 e.preventDefault();
                 return false ;

            });
        },

        noteAction: function () {

            var noteDetail = $(".comment_operate");
            noteDetail.each(function(){
           //     var $this = $(this);
           //     console.log($(this));
                detail.clickComment($(this));
                detail.updateNote($(this));
                detail.poke($(this));
            });
        },

        updateNote: function (noteItem) {
           // console.log(noteItem);

            //console.warn('the following line , can not find note_content for new note (just added to page via ajax call)')
            var note_content = noteItem.parent().find(".comment_word.content");
            var note_update_form = noteItem.find(".update-note-form");
            var note_text = note_update_form.find('textarea');
            //console.log(note_text);
            var origin_text = note_content.html() || '';

            //var htmltag = "<a href=\"\" target=\"_blank\">";
            origin_text = origin_text.replace(/<(.|\n)+?>/gi, "");
            noteItem.find(".update-note").on('click', function() {
           //     var form = noteItem.find();
                console.log(origin_text);
                if (note_update_form.css('display') != 'block') {
                    note_content.hide();
                    note_update_form.show();
                    note_text.html(origin_text);
                      //    console.log(origin_text);
                      //    return;
                } else {
                    note_update_form.hide();
                    note_content.show();
                }
            });

            note_update_form.find('.btn-cancel').on('click', function() {
                note_update_form.hide();
                note_content.show();
            });
            note_update_form.on('submit', function(e) {
                      //   鸶te note_text[0].value;
                      //    var url = note_update_form[0].action;
                      //    console.log(note_text[0].value);
                var note_content_text = $.trim(note_text[0].value);
                    note_content_text = clearUserInputString(note_content_text);

                if (note_content_text.length > 0) {
                        $.ajax({
                            type: 'post',
                            dataType:'json',
                            url: note_update_form[0].action,
                            data: $(this).serialize(),
                            success: function (data) {
                                if (parseInt(data.result) === 1) {
                                    note_content.html(note_content_text);
                                    note_update_form.hide();
                                    note_content.show();
                                }
                                util.initTag();
                            }
                        });
                    } else {
                    note_text.focus();
                    // TODO: handle empty input
                }
                e.preventDefault();
            });
        },

        commentAction: function(comment) {
            var form = comment.find('form');
            var commentText = form.find('.comment-content');
            var replyToUser = '';
            var replyToComment = '';
           // console.log(commentText);
            comment.find('.btn-cancel').on('click', function() {

                comment.slideToggle('fast');
                //commentText.val('');
            });

            function reply(commentItem) {
           //     console.log(commentItem.find('.reply'));
                commentItem.find('.reply').on('click', function (e) {

                    var commentContent = commentItem.find('.comment-content');
                    var nickname = commentItem.find('.nickname');
                      //    console.log(nickname);
                    commentText.val('回复 ' + $.trim(nickname.text()) + ': ');
                    commentText.focus();
                    replyToUser = commentContent.attr('data-creator');
                    replyToComment = commentContent.attr('data-comment');
                      //    }
                    return false;
                });

                commentItem.find('.close').on('click', function (e) {
                    var comment_id = $(this).attr('data-comment');
                    var url = '/entity/note/comment/' + comment_id + '/delete/';
                      //    console.log(comment_id);
                    $.ajax({
                        url:url,
                        type: 'post',
                        dataType:'json',
                        success: function(data){
                      //            console.log(data);
                            if (data.status === 1) {
                                commentItem.remove();
                            }
                        }
                    });

                    return false;
                });
            }

            comment.find('.media').each(function () {
                reply($(this));
            });

           // var commentItem = commentItem;
            form.on('submit', function(e) {
                var input = commentText[0];
                var text = input.value;

                text = text.replace(/^回复.*[:：]/, function (str, index) {
                    if (index === 0) {
                        return '';
                    }
                    return str;
                });
                text = $.trim(text);
                if (text.length > 0) {
                    var url = form[0].action;
                    var data = {
                        'content': text,
                        'reply_to_user_id': replyToUser,
                        'reply_to_comment_id': replyToComment
                    };

                    $.ajax({
                        type:"post",
                        url:url,
                        data:data,
                        success: function(result) {
                      //            console.log(result);
                            try {
                                result = $.parseJSON(result);
                      //                var status = parseInt(result.status);
                      //                if (status === 1) {
                                var $html = $(result.data);
                                reply($html);
                                $html.insertBefore(form);
                      //                }
                                commentText.val('');
                            } catch (err) {
                                var html = $(result);
                                util.modalSignIn(html);
                            }
                        }
                    });
                } else {
                    input.value = '';
                    input.focus();
                }
                e.preventDefault();
            });
        },

        clickComment: function (note) {

           // console.log(noteDetail);
           // console.log(note);
            // TODO : none login user's  note comment will lost in login process , to an
            note.find('.add-comment').on('click', function (e) {
                var comments = note.parent().find('.note-comment-list');
                var notecontent = note.parent();
           //     console.log(notecontent);
                if(comments[0]) {
                    comments.slideToggle('fast');
                } else {

                    var url = '/entity/note/' + $(this).attr('data-note') + '/comment/';
                      //    console.log(url);
                    $.ajax({
                        url: url,
                        type: 'GET',
                        async: false,
                        success: function(data){
                            result =  $.parseJSON(data);
                            var $html = $(result.data);
                      //            self.noteComment($html);
                            detail.commentAction($html);
                            $html.appendTo(notecontent);
                            // TODO : ant is here !!!
                            $html.slideToggle('fast');
                      //            initTag();
                        },
                        error: function(ajaxContext) {
                             console.log(ajaxContext['responseText']);
                        }
                    });
                    return false;
                }
            });
        },

        poke : function (note) {
           // 给评论点赞
           //console.log("OKOKOKOKO");
            note.find('.poke').on('click', function (e) {
           //     console.log($(this));
                var poke = $(this);
                var note_id = poke.attr('data-note');
                var counter = poke.find('span');
                var poke_icon = poke.find('i');
                var url = '/note/' + note_id + '/poke/';

                $.ajax({
                    type:'post',
                    dataType:'json',
                    url: url,
                    success: function (data){
                        var count = parseInt(counter.html()) || 0;
                        var result = parseInt(data.result);

                        if (result === 1) {
                            count++;
                      //            $counter.text(count).addClass("count_blue");
                            poke_icon.addClass('fa-thumbs-up');
                            poke_icon.removeClass('fa-thumbs-o-up');

                            if (count === 1) {
                                $('<span class="poke-count">' + count + '</span>').appendTo(poke);
                            } else {
                                counter.html(count);
                            }
                        } else if (result === 0) {
                            count--;
                      //            $counter.text(count).removeClass("count_blue");
                            poke_icon.addClass('fa-thumbs-o-up');
                            poke_icon.removeClass('fa-thumbs-up');

                            if (count === 0) {
                                poke.find('span').remove();
                            } else {
                                counter.html(count);
                            }
                        } else {
                            var html = $(data);
                            util.modalSignIn(html);
                        }
                    },
                    error: function(data){
                         var html=$(data.responseText);
                         util.modalSignIn(html);
                    }

                });
            })
        }
    };

    var message = {
        loadData: function(){
            var message = $("#message");
           // console.log(message);
           // $(".btn-top").on('click', function() {
           //     $("html, body").animate(
                      //    {scrollTop : 0}, 800
           //     );
           //     return false;
           // });

            if (message[0]) {
                var flag = false;
                $(window).scroll(function () {
                    //回到顶部按钮效果
                    if ($(this).scrollTop() > 100) {
                        $(".btn-top").fadeIn();
                    } else {
                        $(".btn-top").fadeOut();
                    }

                      //    console.log(($(window).height()));
                    if (($(window).height() + $(window).scrollTop()) >= ($(document).height()-25)&& flag == false) {
                        flag = true;
                        var url = window.location.href;
                        var last_message = message.find('.timestr:last');
                        var timestamp = last_message.attr('timestamp');

                        $.ajax({
                            url: url,
                            type: 'GET',
                            data: {'timestamp':timestamp},
                            success: function(data){
                      //                console.log(data);
                                var result = $.parseJSON(data);
                                var status = parseInt(result.status);
                                if (status == 1 ) {
                                    var html = $(result.data);
                      //                console.log(html);
                                    html.appendTo(message);
                                }
                                flag = false;
                            }
                        });
                    }
                });
            }
        }
    };

    var event = {
        loadData: function() {
            var event = $("#event");
            var counter = 1;

            if (event[0]) {
                var flag = false;
                $(window).scroll(function (){
                    //DUP
                    if ($(this).scrollTop() > 100) {
                        $(".btn-top").fadeIn();
                    } else {
                        $(".btn-top").fadeOut();
                    }

                    if (($(window).height() + $(window).scrollTop()) >= ($(document).height()-25) && flag == false) {
                        flag = true;
                        var aQuery = window.location.href.split('?');
                        var url = aQuery[0];
                        var last_event = event.find('.entity-selection:last');
                        var time = last_event.find('.timestr:last');
                        var timestamp = time.attr('timestamp');

                        $.ajax({
                            url: url,
                            type: 'GET',
                            data: {'timestamp':timestamp, 'p':++counter },
                            success: function(data){
                      //                console.log(data);
                                var result = $.parseJSON(data);
                                var status = parseInt(result.status);
                                if (status == 1 ) {
                                    var html = $(result.data);
                      //                console.log(html);
                                    util.like(html);
                                    html.appendTo(event);
                                }
                                flag = false;
                      //                counter ++;
                            }
                        });
                    }
                });
            }

        }
    };

    // add by an
    var account_setting = {
    //    用户编辑个人资料
        handleUserInfo:function(){
            function show_message(selector, message){
                $(selector).html(message);
            }
            function remove_message(selector){
                $(selector).html('');
            }

            function clean_username() {

                var username = $.trim($('#id_nickname').val());
                $('#id_nickname').val(username);
                return username;
            }

            function check_username(){
                remove_message('#username_error_msg');
                var username = clean_username();
                var err_msg = '用户名格式：中英文数字皆可，2-16个字符。';
                var usernameRegex = /^[\u4e00-\u9fa5a-zA-Z0-9]{2,16}$/;
                if(usernameRegex.test(username) === false){
                    show_message('#username_error_msg', '用户名格式：中英文数字皆可，2-16个字符。');
                    return false ;
                }else{
                    return true;
                }
                //TODO : write a test for the reg up .

            }
            function check_email(){
                return true;
            }
            function clean_bio(){
                var bio = $.trim($('#id_bio').val());
                    bio = clearUserInputString(bio);
                    $('#id_bio').val(bio);
                return bio;
            }
            function check_bio(){
                remove_message('#bio_error_msg');
                var bio = clean_bio();
                var err_msg = '简介请限制在两百字以内。';

                if (bio.length >200){
                    show_message('#bio_error_msg',err_msg);
                    return false;
                }else{
                    return true;
                }
            }

            var userSettinForm = $('[action="/u/settings/"]');
            if (!!userSettinForm.length){
                userSettinForm.eq(0).submit(function(){
                    //console.log('intercepted');
                    if (check_bio() && check_email() && check_username()){
                        return true;
                    }else{
                        return false;
                    }
                });
            }
        }
    };

    var link_page={
        initLinks: function(){
            jQuery('.link-item img').each(function(index, item){
                 var src = jQuery(item).attr('src');
                 var alter_src = jQuery(item).attr('alter-img');

                 jQuery(item).mouseout(function(){
                     jQuery(this).attr({src: src });
                 });
                 jQuery(item).mouseover(function(){
                     jQuery(this).attr({src: alter_src});
                 });


            });
        }
    };

    var selection_article={
        init_loader: function(){
            var article_list = $('#selection_article_list');
            if (article_list && article_list.length){
                var article_loader = new ArticleLoader();
            }
        }
    };

    var article_detail={
        init_loader: function(){
            var main_article = $('#main_article');
            if(main_article && main_article.length){
                var related_article_loader = new RelatedArticleLoader();
            }
        },
    };




    (function init() {
           //   console.log($.find());

        util.like($('body'));
        util.follower();
        util.initTag();
        util.gotop();
        util.handlePageScroll();

        createNewEntity.createEntity();
        createNewEntity.BrandAndTitle();
           //   createNewEntity.changeChiefImage();
        createNewEntity.postNewEntity();
        selection.loadData();

        detail.detailImageHover();
        detail.shareWeibo();
        detail.postNote();
        detail.noteAction();
        detail.initVisitorNote();
        detail.initReportButton();

        message.loadData();
        event.loadData();

        //add by an
        account_setting.handleUserInfo();
        util.checkEventRead();
        util.checkSNSBindVisit();
        link_page.initLinks();

        selection_article.init_loader();
        article_detail.init_loader();
    })();
})(jQuery, document, window);