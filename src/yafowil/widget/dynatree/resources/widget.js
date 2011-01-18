/* 
 * yafowil dynatree widget
 * 
 * Requires: jquery dynatree
 * Optional: bdajax
 */

if (typeof(window['yafowil']) == "undefined") yafowil = {};

(function($) {

    $(document).ready(function() {
        // initial binding
        yafowil.dynatree.binder();
        
        // add after ajax binding if bdajax present
        if (typeof(window['bdajax']) != "undefined") {
            $.extend(bdajax.binders, {
                dynatree_binder: yafowil.dynatree.binder
            });
        }
    });
    
    $.extend(yafowil, {
        
        dynatree: {
            
            binder: function(context) {
                $('.yafowil-widget-dynatree', context).each(function () {
                    var elem = $(this);
                    var rawparams = elem
                        .find('.dynatree-params')
                        .text()
                        .split('|');
                    var params = new Array();
                    for (var idx=0; idx < rawparams.length; idx++) {
                        var pair = rawparams[idx].split(',');
                        var value = pair[1].trim();
                        if (!isNaN(value)) {
                            value = parseInt(value);
                        };
                        if (value=='True') {
                            value = true;
                        };
                        if (value=='False') {
                            value = false;
                        };
                        key = pair[0].trim();
                        if (key == 'type') {
                            sourcetype = value; 
                        } else {
                            params[key] = value;
                        };                
                    };        
                    if (sourcetype=='remote') {
                        params['initAjax'] = {
                            url: elem.find('.dynatree-source').text(),
                            data: {
                                selected: elem.find('input').val()
                            }
                        };
                    };
                    // activation / deactivation
                    params['onSelect'] = function(flag, dtnode) {
                        var sel_nodes = 
                            $(dtnode.tree.$tree).dynatree('getSelectedNodes');
                        var newvalue = '';
                        for (var idx=0; idx < sel_nodes.length; idx++) { 
                            newvalue = newvalue + sel_nodes[idx].data.key + '|';
                        };  
                        $(dtnode.tree.$tree).siblings('input').val(newvalue);
                        $('.dynatreeSelectSensitive').trigger('yafowilDynatreeSelect');
                    };            
                    elem.find(".yafowil-widget-dynatree-tree").dynatree(params);
                });
            }
        }
    });
    
})(jQuery);