define(['jquery','libs/underscore','libs/Class','libs/fastdom'],
    function($,_,Class,fastdom){

        var AnnualReport = Class.extend({
            init: function(){
                console.log('annual report');
                this.fixedReport = $('.fixed-ele');
                if (this.fixedReport.length > 0){
                    this.setupWatcher();
                }else{
                    return ;
                }
            },
            setupWatcher:function(){
                $(window).scroll(this.onScroll.bind(this));
            },
            onScroll:function(){
                if(this.read){
                    fastdom.clear(this.read);
                }
                this.read = fastdom.read(this.doRead.bind(this));
                if(this.write){
                    fastdom.clear(this.write);
                }
                this.write = fastdom.write(this.doWrite.bind(this));
            },
            doRead: function(){
                this.scrollTop = $(window).scrollTop();
                this.pageHeight = document.body.scrollHeight;
                this.footerHeight = $('#guoku_footer')[0].getBoundingClientRect().height;
                this.condition = this.pageHeight - this.footerHeight - 50;
            },
            doWrite: function(){
                var that = this ;
                if (!this.scrollTop){return ;}
                if (this.scrollTop > 50){
                    console.log(this.scrollTop);
                    console.log(this.condition);
                    fastdom.write(function(){
                          console.log('hide');
                        that.fixedReport.hide();
                    });

                }else{
                    fastdom.write(function(){
                          console.log('show');
                        that.fixedReport.show();
                    });
                }
            }

        });
        return AnnualReport;
    });