import testify as T

from nali_interpreter import tokenize


class TokenizerTestCase(T.TestCase):

    def test_tokenize_empty_string(self):
        T.assert_equal(tokenize(''), [])

    def test_tokenize_single_token(self):
        T.assert_equal(tokenize('foo'), ['foo'])

    def test_tokenize_parenthesis(self):
        T.assert_equal(tokenize('(foo)'), ['(', 'foo', ')'])

    def test_tokenize_brackets(self):
        T.assert_equal(tokenize('[foo]'), ['[', 'foo', ']'])

    def test_tokenize_bar(self):
        T.assert_equal(tokenize('|foo|'), ['|', 'foo', '|'])

    def test_tokenize_arithmetic(self):
        T.assert_equal(tokenize('1+2-3'), ['1', '+', '2', '-', '3'])

    def test_tokenize_semicolon(self):
        T.assert_equal(tokenize('foo;bar'), ['foo', ';', 'bar'])

    def test_tokenize_brackes(self):
        T.assert_equal(tokenize('{foo}'), ['{', 'foo', '}'])

    def test_tokenize_colon(self):
        T.assert_equal(tokenize('foo:bar'), ['foo', ':bar'])

    def test_tokenize_period(self):
        T.assert_equal(tokenize('foo.bar'), ['foo', '.bar'])


if __name__ == "__main__":
    T.run()
