function SKU_MNG_APP(){
    this.init();
}

_.extend(SKU_MNG_APP.prototype, {

    init: function(){
        this._property_template = _.template($('#sku_attr_template').html())
        this.render_attributes();
        this.handle_create_attribute();
        this.handle_delete_attribute()
        this.handle_save_sku();
    },

    handle_save_sku:function(){
        $('#sku_form').submit(this.save_sku.bind(this));
        //luoqian add here for ajax post
        $('#sku_form .sku-save').click(this.save_sku.bind(this));
    },

    save_sku: function(e){
        $('#id_attrs').val(this.collect_attribute());
        return true;
    },
    get_attr_name: function(attr_group){
        return  $(attr_group).find('.attr-name-input').val();
    },
    get_attr_value:function(attr_group){
        return $(attr_group).find('.attr-value-input').val();
    },
    collect_attribute: function(){
        var that = this;
        var attribute_dic = {};
        $('.attr-group').each(function(index,attr_group){
            if (!that.get_attr_name(attr_group) || !that.get_attr_value(attr_group)){
                return ;
            }
            attribute_dic[that.get_attr_name(attr_group)] = that.get_attr_value(attr_group);
        });
        return JSON.stringify(attribute_dic);
    },
    handle_delete_attribute: function(){
        $('.attr-table').on('click', '.attr-remove' , this.remove_attr.bind(this));
    },
    handle_create_attribute:function(){
        $('.attr-add').click(this.add_attr.bind(this));
    },
    get_property_dom: function(){
        return $(this._property_template())
    },
    remove_attr: function(e){
        $(e.currentTarget).parent().parent().remove();
    },
    add_attr: function(){
        $dom = this.get_property_dom();
        $('.attr-add-tr').parent().prepend($dom);
        return $dom;
    },
    render_attributes:function(){
        if ($('#sku_attr_json').length <= 0 ){
            return ;
        }

        var attrs = JSON.parse($('#sku_attr_json').val());
        if(attrs){
            for (key in attrs){
                if(attrs.hasOwnProperty(key)){
                    var new_input = this.add_attr();
                    new_input.find('.attr-name-input').val(key);
                    new_input.find('.attr-value-input').val(attrs[key])
                }
            }
        }
    }
});


var sku_app = new SKU_MNG_APP();