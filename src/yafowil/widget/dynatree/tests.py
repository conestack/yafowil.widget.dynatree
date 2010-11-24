import unittest
import doctest 
from pprint import pprint
from interlude import interact
import lxml.etree as etree

optionflags = doctest.NORMALIZE_WHITESPACE | \
              doctest.ELLIPSIS | \
              doctest.REPORT_ONLY_FIRST_FAILURE

TESTFILES = [
    'widget.txt',
]

def prettyxml(xml):
    et = etree.fromstring(xml)
    return etree.tostring(et, pretty_print=True)


def test_suite():
    return unittest.TestSuite([
        doctest.DocFileSuite(
            file, 
            optionflags=optionflags,
            globs={'interact': interact,
                   'pprint': pprint,
                   'prettyxml': prettyxml},
        ) for file in TESTFILES
    ])

if __name__ == '__main__':                                   #pragma NO COVERAGE
    unittest.main(defaultTest='test_suite')                  #pragma NO COVERAGE