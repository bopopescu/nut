define(['libs/Class','jquery'], function(Class,$){
    var UserFollow = Class.extend({
        init: function () {
            this.$follow = $(".follow");
            this.$follow.on('click', this.handleFollow.bind(this));
        },

        handleFollow: function (e) {
            var $followButton = $(e.currentTarget);
            var uid = $followButton.attr('data-user-id');
            var status = $followButton.attr('data-status');
            var action_url = "/u/" + uid;

            if (status == 1) {
                action_url += "/unfollow/";

            } else {
                action_url += "/follow/";
            }

            $.when($.ajax({
                url: action_url,
                dataType: 'json',
                method: 'POST'
            })).then(function success(data) {
                console.log('success');
                console.log(data);
                if (data.status == 1) {
                    $followButton.html('<i class="fa fa-check fa-lg"></i>&nbsp; 取消关注');
                    $followButton.attr('data-status', '1');
                    $followButton.removeClass("button-blue").addClass("btn-cancel");

                } else if (data.status == 2) {
                    console.log('mutual !!!');
                    $followButton.html('<i class="fa fa-exchange fa-lg"></i>&nbsp; 取消关柱');
                    $followButton.removeClass('button-blue').addClass('btn-cancel');
                    $followButton.attr('data-status', '1');

                } else if (data.status == 0) {
                    $followButton.html('<i class="fa fa-plus"></i>&nbsp; 关注');
                    $followButton.removeClass("btn-cancel").addClass("button-blue");
                    $followButton.attr('data-status', '0');
                } else {
                    console.log('did not response with valid data');
                }

            }, function fail(error) {
                console.log('failed' + error);
                var html = $(error.responseText);
                util.modalSignIn(html);
            });
        }
    });
    return UserFollow;
});


