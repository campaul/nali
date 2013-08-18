import testify as T

from tests.nali_interpreter_test import InterpreterTestCase


class NamespaceTestCase(InterpreterTestCase):

    def test_define(self):
        self.interpreter.eval('def :foo 42')
        T.assert_equal(self.interpreter.eval('foo'), 42)

    def test_global_scope(self):
        self.interpreter.eval('def :foo 42')
        T.assert_equal(self.interpreter.eval('[foo]'), 42)
