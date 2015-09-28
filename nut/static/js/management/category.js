;(function ($) {
    var url = "/management/category/";
    var new_data;
    var old_data;

    var category_group = $("#category");
    var category = $("#sub-category");
    var init_category = category.attr("data-init");
    //
    //var old_category_group = $("#old_category_group");
    //var old_category = $("#old_category");
    //var old_init_category = old_category.attr("data-oldinit");

    $.get(url, function (data) {
        //var return_data = $.parseJSON(data);
        //new_data = return_data["new_category"];
        //old_data = return_data["old_category"];
        //console.log(return_data);
        relatedOption(category_group, category, getNewOptions(data), init_category);
        //relatedOption(old_category_group, old_category, getOldOptions(old_data), old_init_category);
    });
    //$.ajax({
    //    url: url,
    //    dataType: 'json',
    //    success: function(data){
    //
    //    }
    //});

    function getNewOptions(data) {
        var options = [];
        for (var t in data) {
            var option = {};
            option["value"] = t;
            option["text"] = t;
            option['options'] = [];

            var values = data[t];
            for (var i = 0; i < values.length; i++) {
                option['options'].push({
                    value: values[i]["category_id"],
                    text: values[i]["category_title"]
                });
            }
            options.push(option);
        }

        options.sort(function (value1, value2) {
            if (value1.text < value2.text) return 1;
            return -1;
        });

        return options;
    }

    //function getOldOptions(data) {
    //    var options = [];
    //
    //    for (var i = 0; i < data.length; i++) {
    //        var id = data[i]["category_id"];
    //        var title = data[i]["category_title"];
    //
    //        if (id >= 1 && id <= 12) {
    //            options[i] = {};
    //            options[i]["value"] = id;
    //            options[i]["text"] = title;
    //            options[i]["options"] = [];
    //        }
    //        if (id == 12) {
    //            options[i]["options"].push({ value: 12, text: "其他" });
    //        }
    //    }
    //
    //    for (var j = 0; j < data.length; j++) {
    //        var id = data[j]["category_id"];
    //        var pid = data[j]["category_pid"];
    //        var title = data[j]["category_title"];
    //
    //        if (id > 12) {
    //            for (var k = 0; k < options.length; k++) {
    //                if (pid == options[k].value) {
    //                    options[k].options.push({ value: id, text: title });
    //                }
    //            }
    //        }
    //    }
    //
    //    return options;
    //}

    function relatedOption(select1, select2, options, init) {
        //console.log(options);
        var l2_options = [];
        for (var i = 0; i < options.length; i++) {
            var l1_option = createOption(options[i].value, options[i].text);
            //l1_option.appendTo(select1);

            var more_options = options[i].options;
            for (var j = 0; j < more_options.length; j++) {
                if (more_options[j].value == init) {
                    select(l1_option);
                    l2_options = more_options;
                }
            }
        }

        for (var k = 0; k < l2_options.length; k++) {
            var l2_option = createOption(l2_options[k].value, l2_options[k].text);
            l2_option.appendTo(select2);
            if (l2_options[k].value == init) {
                select(l2_option);
            }
        }

        select1.change(function () {
            $("option", select2).each(function () {
                $(this).remove();
            });

            var select_value = select1.val();
            //console.log(select_value);
            var more_options;
            for (var i = 0; i < options.length; i++) {
                if (options[i].value == select_value) {
                    more_options = options[i].options;
                }
            }
            //console.log(options);

            for (var j = 0; j < more_options.length; j++) {
                var option_level2 = createOption(more_options[j].value, more_options[j].text);
                select2.append(option_level2);
            }
        });

        select1.click(showOptionModal())

        function showOptionModal(){
            console.log('show option modal');
        }

        function createOption(value, text) {
            return $("<option " + "value='" + value + "'>" + text + "</option>");
        }

        function select(option) {
            option.attr("selected", "selected");
        }
    }
})(jQuery);