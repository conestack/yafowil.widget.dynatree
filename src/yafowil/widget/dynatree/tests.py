from node.utils import UNSET
from odict import odict
from yafowil.base import factory
from yafowil.compat import IS_PY2
from yafowil.tests import fxml
from yafowil.tests import YafowilTestCase
from yafowil.utils import tag
from yafowil.widget.dynatree.widget import build_inline_dynatree
import unittest
import yafowil.loader  # noqa


if not IS_PY2:
    from importlib import reload


class TestDynatreeWidget(YafowilTestCase):

    def setUp(self):
        super(TestDynatreeWidget, self).setUp()
        from yafowil.widget.dynatree import widget
        reload(widget)

    @property
    def mock_tree(self):
        # A test tree
        tree = odict()
        animals = odict()
        tree['animal'] = ('Animals', animals)

        mammal = odict()
        mammal['horse'] = ('Horse', None)
        mammal['ape'] = ('Ape', None)
        mammal['elephant'] = ('Elephant', None)
        animals['mammal'] = ('Mammals', mammal)

        bird = odict()
        bird['turkey'] = ('Turkey', None)
        bird['swan'] = ('Swan', None)
        bird['hummingbird'] = ('Hummingbird', None)
        bird['duck'] = ('Duck', None)
        animals['bird'] = ('Birds', bird)

        return tree

    def test_inline_tree_renderer(self):
        html = build_inline_dynatree(
            self.mock_tree,
            'animal',
            tag,
            ulid='dynatree-source'
        )
        self.checkOutput("""
        <ul class="hiddenStructure" id="dynatree-source">
        <li class="selected" id="animal">Animals<ul>
        <li id="mammal">Mammals<ul>
        <li id="horse">Horse
        </li><li id="ape">Ape
        </li><li id="elephant">Elephant
        </li></ul>
        </li><li id="bird">Birds<ul>
        <li id="turkey">Turkey
        </li><li id="swan">Swan
        </li><li id="hummingbird">Hummingbird
        </li><li id="duck">Duck
        </li></ul>
        </li></ul>
        </li></ul>
        """, fxml(html))

    def test_plain_widget_source_is_string(self):
        # Render plain widget, source is string
        widget = factory(
            'dynatree',
            name='root',
            props={
                'source': 'http://www.foo.bar/baz.json'
            })
        self.checkOutput("""
        <div class="yafowil-widget-dynatree">
          <input id="input-root" name="root" type="hidden"/>
          <div class="dynatree-source hiddenStructure">http://www.foo.bar/baz.json</div>
          <div class="dynatree-params hiddenStructure">selectMode,1|minExpandLevel,1|rootVisible,False|autoCollapse,False|checkbox,True|imagePath,skin-bootstrap|type,remote</div>
          <div class="yafowil-widget-dynatree-tree"/>
        </div>
        """, fxml(widget()))

    def test_plain_widget_source_is_tree(self):
        # Render plain widget, source is tree
        widget = factory(
            'dynatree',
            name='root',
            props={
                'source': self.mock_tree
            })
        self.checkOutput("""
        <div class="yafowil-widget-dynatree">
          <input id="input-root" name="root" type="hidden"/>
          <ul class="hiddenStructure" id="dynatree-source-root">
        <li id="animal">Animals<ul>
        <li id="mammal">Mammals<ul>
        <li id="horse">Horse
        </li><li id="ape">Ape
        </li><li id="elephant">Elephant
        </li></ul>
        </li><li id="bird">Birds<ul>
        <li id="turkey">Turkey
        </li><li id="swan">Swan
        </li><li id="hummingbird">Hummingbird
        </li><li id="duck">Duck
        </li></ul>
        </li></ul>
        </li></ul>
          <div class="dynatree-params hiddenStructure">selectMode,1|minExpandLevel,1|rootVisible,False|autoCollapse,False|checkbox,True|imagePath,skin-bootstrap|type,local|initId,dynatree-source-root</div>
          <div class="yafowil-widget-dynatree-tree"/>
        </div>
        """, fxml(widget()))

    def test_plain_widget_source_is_callable(self):
        # Render plain widget, source is callable
        def tree_callable(widget, data):
            return self.mock_tree

        widget = factory(
            'dynatree',
            name='root',
            props={
                'source': tree_callable
            })
        self.checkOutput("""
        <div class="yafowil-widget-dynatree">
          <input id="input-root" name="root" type="hidden"/>
          <ul class="hiddenStructure" id="dynatree-source-root">
        <li id="animal">Animals<ul>
        <li id="mammal">Mammals<ul>
        <li id="horse">Horse
        </li><li id="ape">Ape
        </li><li id="elephant">Elephant
        </li></ul>
        </li><li id="bird">Birds<ul>
        <li id="turkey">Turkey
        </li><li id="swan">Swan
        </li><li id="hummingbird">Hummingbird
        </li><li id="duck">Duck
        </li></ul>
        </li></ul>
        </li></ul>
          <div class="dynatree-params hiddenStructure">selectMode,1|minExpandLevel,1|rootVisible,False|autoCollapse,False|checkbox,True|imagePath,skin-bootstrap|type,local|initId,dynatree-source-root</div>
          <div class="yafowil-widget-dynatree-tree"/>
        </div>
        """, fxml(widget()))

    def test_plain_widget_source_is_invalid(self):
        # Try to render plain widget, source is invalid
        widget = factory(
            'dynatree',
            name='root',
            value='ape',
            props={
                'source': object()
            })
        err = self.expectError(
            ValueError,
            widget
        )
        self.assertEqual(str(err), 'resulting source must be [o]dict or string')

    def test_plain_widget_source_is_tree_preset_values_single_select(self):
        # Render plain widget, source is tree, preselect ape, single select
        widget = factory(
            'dynatree',
            name='root',
            value='ape',
            props={
                'source': self.mock_tree
            })
        self.checkOutput("""
        <div class="yafowil-widget-dynatree">
          <input id="input-root" name="root" type="hidden" value="ape"/>
          <ul class="hiddenStructure" id="dynatree-source-root">
        <li id="animal">Animals<ul>
        <li id="mammal">Mammals<ul>
        <li id="horse">Horse
        </li><li class="selected" id="ape">Ape
        </li><li id="elephant">Elephant
        </li></ul>
        </li><li id="bird">Birds<ul>
        <li id="turkey">Turkey
        </li><li id="swan">Swan
        </li><li id="hummingbird">Hummingbird
        </li><li id="duck">Duck
        </li></ul>
        </li></ul>
        </li></ul>
          <div class="dynatree-params hiddenStructure">selectMode,1|minExpandLevel,1|rootVisible,False|autoCollapse,False|checkbox,True|imagePath,skin-bootstrap|type,local|initId,dynatree-source-root</div>
          <div class="yafowil-widget-dynatree-tree"/>
        </div>
        """, fxml(widget()))

    def test_plain_widget_source_is_tree_preset_values_multi_select(self):
        # Render plain widget, source is tree, preselect ape and swan,
        # multi select
        widget = factory(
            'dynatree',
            name='root',
            value=['ape', 'swan'],
            props={
                'source': self.mock_tree,
                'selectMode': 1
            })
        self.checkOutput("""
        <div class="yafowil-widget-dynatree">
          <input id="input-root" name="root" type="hidden" value="ape|swan"/>
          <ul class="hiddenStructure" id="dynatree-source-root">
        <li id="animal">Animals<ul>
        <li id="mammal">Mammals<ul>
        <li id="horse">Horse
        </li><li class="selected" id="ape">Ape
        </li><li id="elephant">Elephant
        </li></ul>
        </li><li id="bird">Birds<ul>
        <li id="turkey">Turkey
        </li><li class="selected" id="swan">Swan
        </li><li id="hummingbird">Hummingbird
        </li><li id="duck">Duck
        </li></ul>
        </li></ul>
        </li></ul>
          <div class="dynatree-params hiddenStructure">selectMode,1|minExpandLevel,1|rootVisible,False|autoCollapse,False|checkbox,True|imagePath,skin-bootstrap|type,local|initId,dynatree-source-root</div>
          <div class="yafowil-widget-dynatree-tree"/>
        </div>
        """, fxml(widget()))

    def test_extract_from_select_mode_1(self):
        # Extract from selectMode=1 - means single selection
        widget = factory(
            'dynatree',
            name='root',
            props={
                'source': self.mock_tree,
                'selectMode': 1
            })
        data = widget.extract({'root': 'somevalue|'})
        self.assertEqual(
            [data.name, data.value, data.extracted, data.errors],
            ['root', UNSET, 'somevalue', []]
        )
        data

    def test_extract_from_select_mode_2(self):
        # Extract from selectMode=2 - means multi selection
        widget = factory(
            'dynatree',
            name='root',
            props={
                'source': self.mock_tree,
                'selectMode': 2
            })
        data = widget.extract({'root': 'somevalue|'})
        self.assertEqual(
            [data.name, data.value, data.extracted, data.errors],
            ['root', UNSET, ['somevalue'], []]
        )
        data = widget.extract({'root': 'somevalue|othervalue'})
        self.assertEqual(
            [data.name, data.value, data.extracted, data.errors],
            ['root', UNSET, ['somevalue', 'othervalue'], []]
        )

    def test_extract_empty(self):
        widget = factory(
            'dynatree',
            name='root',
            props={
                'source': self.mock_tree,
                'selectMode': 2
            })
        data = widget.extract({})
        self.assertEqual(
            [data.name, data.value, data.extracted, data.errors],
            ['root', UNSET, UNSET, []]
        )


if __name__ == '__main__':
    unittest.main()
