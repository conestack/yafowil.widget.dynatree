import $ from 'jquery';

const widget_url = new URL('../src/widget.js', import.meta.url).href;

// widget.js must extend an existing yafowil namespace instead of replacing it.
window.jQuery = $;
window.yafowil = { other: 'other' };
const orig_ready = $.fn.ready;
$.fn.ready = function () {
    return this;
};
await new Promise((resolve, reject) => {
    const script = document.createElement('script');
    script.src = widget_url;
    script.onload = resolve;
    script.onerror = reject;
    document.head.appendChild(script);
});
$.fn.ready = orig_ready;

QUnit.module('namespace', (hooks) => {
    let orig_yafowil;

    hooks.beforeEach(() => {
        orig_yafowil = window.yafowil;
        $.fn.ready = function () {
            return this;
        };
    });
    hooks.afterEach(() => {
        window.yafowil = orig_yafowil;
        $.fn.ready = orig_ready;
    });

    QUnit.test('extend existing yafowil namespace', (assert) => {
        assert.strictEqual(window.yafowil.other, 'other');
        assert.strictEqual(typeof window.yafowil.dynatree.binder, 'function');
    });

    QUnit.test('create yafowil namespace in strict mode code', async (assert) => {
        delete window.yafowil;
        const source = await (await fetch(widget_url)).text();
        new Function(`'use strict';\n${source}`)();
        assert.strictEqual(typeof window.yafowil.dynatree.binder, 'function');
    });
});
