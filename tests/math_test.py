import testify as T

from tests.nali_interpreter_test import InterpreterTestCase


class MathTestCase(InterpreterTestCase):

    def test_addition(self):
        T.assert_equal(self.interpreter.eval('2 + 3'), 5)

    def test_subtraction(self):
        T.assert_equal(self.interpreter.eval('5 - 3'), 2)

    def test_multiplication(self):
        T.assert_equal(self.interpreter.eval('2 * 3'), 6)

    def test_division(self):
        T.assert_equal(self.interpreter.eval('8 / 2'), 4)

    def test_modulo(self):
        T.assert_equal(self.interpreter.eval('5 % 3'), 2)

    def test_order_of_operations(self):
        T.assert_equal(self.interpreter.eval('2 + 3 * 4'), 20)
        T.assert_equal(self.interpreter.eval('2 + (3 * 4)'), 14)
