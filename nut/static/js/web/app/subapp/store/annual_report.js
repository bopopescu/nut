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
                this.screenHeight = window.screen.height;
                this.pageHeight = document.body.scrollHeight;
                this.footerHeight = $('#guoku_footer')[0].getBoundingClientRect().height;
                this.leftCondition = this.screenHeight + this.scrollTop;
                //where is the 90, I calculate it.but I don't know where is it from
                this.rightCondition = this.pageHeight - this.footerHeight + 90;
            },
            doWrite: function(){
                var that = this ;
                if (!this.scrollTop){return ;}
                if (this.leftCondition > this.rightCondition){
                    fastdom.write(function(){
                        that.fixedReport.removeClass('shown-report');
                        that.fixedReport.addClass('hidden-report');
                        that.fixedReport.hide();
                    });

                }else{
                    fastdom.write(function(){
                        that.fixedReport.removeClass('hidden-report');
                        that.fixedReport.addClass('shown-report');
                        that.fixedReport.show();
                    });
                }
            }

        });
        return AnnualReport;
    });