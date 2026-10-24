/*
 * yafowil dynatree widget
 *
 * Requires: jquery dynatree
 * Optional: bdajax
 */

if (typeof window.yafowil === 'undefined') yafowil = {};

(($) => {
    $(document).ready(() => {
        // initial binding
        yafowil.dynatree.binder();

        // add after ajax binding if bdajax present
        if (typeof window.bdajax !== 'undefined') {
            $.extend(bdajax.binders, {
                dynatree_binder: yafowil.dynatree.binder,
            });
        }
    });

    $.extend(yafowil, {
        dynatree: {
            binder: (context) => {
                $('.yafowil-widget-dynatree', context).each(function () {
                    const elem = $(this);
                    const rawparams = elem.find('.dynatree-params').text().split('|');
                    const params = [];
                    let sourcetype = '';
                    for (let idx = 0; idx < rawparams.length; idx++) {
                        const pair = rawparams[idx].split(',');
                        let value = pair[1].replace(/^\s+|\s+$/g, '');
                        if (!Number.isNaN(Number(value))) {
                            value = parseInt(value, 10);
                        }
                        if (value === 'True') {
                            value = true;
                        }
                        if (value === 'False') {
                            value = false;
                        }
                        const key = pair[0].replace(/^\s+|\s+$/g, '');
                        if (key === 'type') {
                            sourcetype = value;
                        } else {
                            params[key] = value;
                        }
                    }
                    if (sourcetype === 'remote') {
                        params.initAjax = {
                            url: elem.find('.dynatree-source').text(),
                            data: {
                                selected: elem.find('input').val(),
                            },
                        };
                    }
                    // activation / deactivation
                    params.onSelect = (_flag, dtnode) => {
                        const sel_nodes = $(dtnode.tree.$tree).dynatree('getSelectedNodes');
                        let newvalue = '';
                        for (let idx = 0; idx < sel_nodes.length; idx++) {
                            newvalue = `${newvalue}${sel_nodes[idx].data.key}|`;
                        }
                        $(dtnode.tree.$tree).siblings('input').val(newvalue);
                        $('.dynatreeSelectSensitive').trigger('yafowilDynatreeSelect');
                    };
                    elem.find('.yafowil-widget-dynatree-tree').dynatree(params);
                });
            },
        },
    });
})(jQuery);
