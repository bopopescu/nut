define(['jquery','libs/Class'],function(
    $,Class

){
    var CreateNewEntity = Class.extend({
        init: function () {
            this.createEntity();
            this.BrandAndTitle();
            //createNewEntity.changeChiefImage();
            this.postNewEntity();
            console.log('create new entity begin');
        },
        createEntity: function () {
            var form = $('.create-entity form');
            var entityExist = $(".entity-exist");
            var addEntity = $(".add-entity");
            var addEntityNote = $(".add-entity-note");
            var imageThumbails = $(".image-thumbnails");
            //  console.log(entityExist);
            form.on('submit', function (e) {
                // have to add tool function here ,
                // TODO : refactor the whole script ! by an
                //
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

                function valid_url_support(url) {
                    var reg = /\b(jd|360buy|tmall|taobao|95095|amazon)\.(cn|com|hk)/i;
                    return reg.test(url);

                }

                function show_url_not_support_message() {
                    $('#url_error_msg').html('请输入淘宝、天猫、亚马逊或京东的商品链接');
                }

                function hide_url_not_support_message() {
                    $('#url_error_msg').html('');
                }

                function remove_current_user_input() {
                    form.find("input[name='cand_url']").val('');
                }

                hide_url_not_support_message();
                var entity_url = form.find("input[name='cand_url']").val();
                if (!valid_url_support(entity_url)) {
                    show_url_not_support_message();
                    remove_current_user_input();
                    return false;
                }
                ;


                //console.log(this.action);
                addEntity.find(".title").text("");
                addEntity.find("input[name=title]").val("");

                $.ajax({
                    type: 'post',
                    url: this.action,
                    data: {cand_url: entity_url},
                    dataType: "json",
                    success: function (data) {

                        if (data.status == "EXIST") {
                            entityExist.find('a').attr("href", "/detail/" + data.data.entity_hash);
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
                            for (var i = 0; i < data.data.thumb_images.length; i++) {
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

                                $('<input name="thumb_images" type="hidden" value=' + data.data.thumb_images[i] + '>').appendTo($(".add-entity-note form"));
                            }
                            //createNewEntity.changeChiefImage(imageThumbails);

                            //if(data.data.taobao_id == undefined){
                            //$('<input type="hidden" name="origin_id" value="'+data.data.origin_id+'">').appendTo($(".add-entity-note form"));
                            //  '<input type="hidden" name="jd_title" value="'+data.data.jd_title+'">').appendTo($(".add-entity-note form"));
                            //$(".detail_taobao_brand").val(data.data.brand);
                            //                } else {
                            //                    $('<input type="hidden" name="taobao_id" value="'+data.data.taobao_id+'">' ).appendTo($(".add-entity-note form"));
                            ////'<input type="hidden" name="taobao_title" value="'+data.data.taobao_title+'">').appendTo($(".add-entity-note form"));
                            //                }
                            $(
                                '<input type="hidden" name="origin_id" value="' + data.data.origin_id + '">' +
                                '<input type="hidden" name="origin_source" value="' + data.data.origin_source + '">' +
                                '<input type="hidden" name="shop_link" value="' + data.data.shop_link + '">' +
                                '<input type="hidden" name="shop_nick" value="' + data.data.shop_nick + '">' +
                                '<input type="hidden" name="url" value="' + data.data.cand_url + '">' +
                                '<input type="hidden" name="price" value="' + data.data.price + '">' +
                                '<input type="hidden" name="chief_image_url" value="' + data.data.chief_image_url + '">' +
                                '<input type="hidden" name="cid" value="' + data.data.cid + '">' +
                                    //'<input type="hidden" name="selected_category_id" value="'+data.data.selected_category_id+'">' +
                                '<input type="hidden" name="cand_url" value="' + data.data.cand_url + '">' +
                                '<input name="user_id" type="hidden" value="' + data.data.user_id + '">').appendTo($(".add-entity-note form")
                            );
                            addEntity.slideDown();
                            addEntityNote.slideDown();
                        }
                    },
                    error: function (error) {
                        console.log(error);
                    }
                });
                e.preventDefault();
            });
        },
        BrandAndTitle: function () {
            var addEntity = $(".add-entity");
            addEntity.find("input[name='brand']").on('input propertychange', function () {
                var brand = $(this).val();
                if (brand.length > 0) {
                    addEntity.find(".brand").html(brand + " -");
                } else {
                    addEntity.find(".brand").html(brand);
                }
            });
            addEntity.find("input[name='title']").on('input propertychange', function () {
                var title = $(this).val();
                addEntity.find(".title").html(title);
            });
        },
        changeChiefImage: function (object) {
            // console.log(object);
            var image = object.find(".thumbnail");


            image.on('click', function () {
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
        postNewEntity: function () {
            var newEntityForm = $(".add-entity-note form");

            newEntityForm.on("submit", function (e) {
                var text = $.trim(newEntityForm.find("textarea[name='note_text']").val());
                if (text.length > 0) {
                    var brand = $(".add-entity input[name='brand']").val();
                    var title = $(".add-entity input[name='title']").val();
                    $('<input type="hidden" name="brand" value="' + brand + '">').appendTo(newEntityForm);
                    $('<input type="hidden" name="title" value="' + title + '">').appendTo(newEntityForm);
                    return true;
                } else {
                    $(".add-entity-note form textarea[name='note_text']").focus();
                    return false;
                }
            });


        }
    });

    return CreateNewEntity;

});