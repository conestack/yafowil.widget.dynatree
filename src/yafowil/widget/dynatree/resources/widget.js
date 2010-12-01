(function($) {

    $(document).ready(function() {
        
        $('.yafowil-widget-dynatree').each(function () {
            var jqthis = $(this);
            var rawparams = jqthis.find('.dynatree-params').text().split('|');
            var params = new Array();
            for (var idx=0; idx<rawparams.length; idx++) {
                var pair = rawparams[idx].split(',');
                var value = pair[1].trim();
                if (!isNaN(value)) { value = parseInt(value); };
                if (value=='True') { value = true; };
                if (value=='False') { value = false; };
                key = pair[0].trim();
                if (key == 'type') {
                    sourcetype = value; 
                } else {
                    params[key] = value;
                };                
            };        
            if (sourcetype=='remote') {
                params['initAjax'] = {
        			'url': jqthis.find('.dynatree-source').text()
        		};
            };
    		// activation/ deactivation
    		params['onSelect'] = function(flag, dtnode) {
    			var sel_nodes = $(dtnode.tree.$tree).dynatree('getSelectedNodes');
    			var newvalue = '';
    			for (var idx=0; idx<sel_nodes.length; idx++) { 
    				newvalue = newvalue + sel_nodes[idx].data.key + '|';
    			};  
    			$(dtnode.tree.$tree).siblings('input').val(newvalue);
    		};            
            jqthis.find(".yafowil-widget-dynatree-tree").dynatree(params);
        });
        
    });
    
})(jQuery);