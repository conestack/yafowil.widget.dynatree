import $ from 'jquery';
import '../src/bundle.js';

// widget.js is a classic script relying on a global jQuery. Load it via
// script tag and capture its DOM ready callback instead of letting jQuery run
// it once, so each registration branch can be exercised.
window.jQuery = $;
const ready_callbacks = [];
const orig_ready = $.fn.ready;
$.fn.ready = function (fn) {
    ready_callbacks.push(fn);
    return this;
};
await new Promise((resolve, reject) => {
    const script = document.createElement('script');
    script.src = new URL('../src/widget.js', import.meta.url).href;
    script.onload = resolve;
    script.onerror = reject;
    document.head.appendChild(script);
});
$.fn.ready = orig_ready;

QUnit.module('dynatree', (hooks) => {
    let container, dynatree_calls, selected_nodes;

    function create_widget(params, source_url) {
        const widget = $('<div class="yafowil-widget-dynatree" />').appendTo(container);
        $('<input type="hidden" />').val('a|').appendTo(widget);
        if (source_url) {
            $('<div class="dynatree-source hiddenStructure" />').text(source_url).appendTo(widget);
        }
        $('<div class="dynatree-params hiddenStructure" />').text(params).appendTo(widget);
        $('<div class="yafowil-widget-dynatree-tree" />').appendTo(widget);
        return widget;
    }

    hooks.beforeEach(() => {
        container = $('<div />').appendTo('body');
        dynatree_calls = [];
        selected_nodes = [];
        // mock jquery.dynatree plugin
        $.fn.dynatree = function (arg) {
            if (arg === 'getSelectedNodes') {
                return selected_nodes;
            }
            dynatree_calls.push([this, arg]);
            return this;
        };
    });
    hooks.afterEach(() => {
        container.remove();
        delete $.fn.dynatree;
        delete window.bdajax;
    });

    QUnit.test('namespace', (assert) => {
        assert.strictEqual(typeof window.yafowil.dynatree.binder, 'function');
        assert.strictEqual(ready_callbacks.length, 1);
    });

    QUnit.test('binder with local source', (assert) => {
        const widget = create_widget(
            'selectMode,2|minExpandLevel, 1 |rootVisible,False|autoCollapse,True|' +
                'checkbox,True|imagePath,skin/|type,local|initId,tree-source',
        );
        yafowil.dynatree.binder(container);

        assert.strictEqual(dynatree_calls.length, 1);
        const [tree, params] = dynatree_calls[0];
        assert.true(tree.is($('.yafowil-widget-dynatree-tree', widget)));
        assert.strictEqual(params.selectMode, 2);
        assert.strictEqual(params.minExpandLevel, 1);
        assert.strictEqual(params.rootVisible, false);
        assert.strictEqual(params.autoCollapse, true);
        assert.strictEqual(params.checkbox, true);
        assert.strictEqual(params.imagePath, 'skin/');
        assert.strictEqual(params.initId, 'tree-source');
        assert.strictEqual(params.type, undefined);
        assert.strictEqual(params.initAjax, undefined);
        assert.strictEqual(typeof params.onSelect, 'function');
    });

    QUnit.test('binder with remote source', (assert) => {
        create_widget('selectMode,1|type,remote', 'http://example.com/tree');
        yafowil.dynatree.binder(container);

        assert.strictEqual(dynatree_calls.length, 1);
        const params = dynatree_calls[0][1];
        assert.strictEqual(params.selectMode, 1);
        assert.deepEqual(params.initAjax, {
            url: 'http://example.com/tree',
            data: {
                selected: 'a|',
            },
        });
    });

    QUnit.test('binder does not leak global variables', (assert) => {
        create_widget('selectMode,1|type,local');
        yafowil.dynatree.binder(container);
        assert.strictEqual(dynatree_calls.length, 1);
        assert.false(Object.hasOwn(window, 'key'));
    });

    QUnit.test('binder respects context', (assert) => {
        create_widget('selectMode,1|type,local');
        yafowil.dynatree.binder($('<div />'));
        assert.strictEqual(dynatree_calls.length, 0);
    });

    QUnit.test('onSelect', (assert) => {
        const widget = create_widget('selectMode,2|type,local');
        const sensitive = $('<div class="dynatreeSelectSensitive" />').appendTo(container);
        sensitive.on('yafowilDynatreeSelect', () => {
            assert.step('yafowilDynatreeSelect');
        });
        yafowil.dynatree.binder(container);
        const [tree, params] = dynatree_calls[0];

        selected_nodes = [{ data: { key: 'b' } }, { data: { key: 'c' } }];
        params.onSelect(true, { tree: { $tree: tree[0] } });
        assert.strictEqual($('input', widget).val(), 'b|c|');
        assert.verifySteps(['yafowilDynatreeSelect']);

        selected_nodes = [];
        params.onSelect(false, { tree: { $tree: tree[0] } });
        assert.strictEqual($('input', widget).val(), '');
        assert.verifySteps(['yafowilDynatreeSelect']);
    });

    QUnit.module('ready', (hooks) => {
        const orig_binder = yafowil.dynatree.binder;
        let bound;

        hooks.beforeEach(() => {
            bound = 0;
            yafowil.dynatree.binder = () => {
                bound++;
            };
        });
        hooks.afterEach(() => {
            yafowil.dynatree.binder = orig_binder;
        });

        QUnit.test('initial binding', (assert) => {
            ready_callbacks[0]();
            assert.strictEqual(bound, 1);
        });

        QUnit.test('register bdajax binder', (assert) => {
            window.bdajax = { binders: {} };
            ready_callbacks[0]();
            assert.strictEqual(bound, 1);
            assert.strictEqual(window.bdajax.binders.dynatree_binder, yafowil.dynatree.binder);
        });
    });
});
