import $ from 'jquery';

// widget.js must extend an existing yafowil namespace instead of replacing it.
window.jQuery = $;
window.yafowil = { other: 'other' };
const orig_ready = $.fn.ready;
$.fn.ready = function () {
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

QUnit.test('extend existing yafowil namespace', (assert) => {
    assert.strictEqual(window.yafowil.other, 'other');
    assert.strictEqual(typeof window.yafowil.dynatree.binder, 'function');
});
