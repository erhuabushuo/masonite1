from masonite.helpers import clean_request_input
import cgi

class TestCleanRequestInput:

    def test_can_clean_string(self):
        assert clean_request_input('<img """><script>alert(\'hey\')</script>">') == '&lt;img &quot;&quot;&quot;&gt;&lt;script&gt;alert(&#x27;hey&#x27;)&lt;/script&gt;&quot;&gt;'

    def test_can_clean_list(self):
        assert clean_request_input(
            ['<img """><script>alert(\'hey\')</script>">', '<img """><script>alert(\'hey\')</script>">']
        ) == [
            '&lt;img &quot;&quot;&quot;&gt;&lt;script&gt;alert(&#x27;hey&#x27;)&lt;/script&gt;&quot;&gt;',
            '&lt;img &quot;&quot;&quot;&gt;&lt;script&gt;alert(&#x27;hey&#x27;)&lt;/script&gt;&quot;&gt;'
        ]

    def test_can_clean_dictionary(self):
        assert clean_request_input(
            {'key': '<img """><script>alert(\'hey\')</script>">'}
        ) == {'key': '&lt;img &quot;&quot;&quot;&gt;&lt;script&gt;alert(&#x27;hey&#x27;)&lt;/script&gt;&quot;&gt;'}

    def test_can_clean_multiple_dictionary(self):
        assert clean_request_input(
            {
                "conta_corrente": {
                    "ocultar": False,
                    "visao_geral": True,
                    "extrato": True
                }
            }
        ) == {
            "conta_corrente": {
                "ocultar": False,
                "visao_geral": True,
                "extrato": True
            }
        }

    def test_does_not_clean_field_storage_objects(self):
        fieldstorage = FieldStorageTest()
        assert clean_request_input(fieldstorage) == fieldstorage


class FieldStorageTest(cgi.FieldStorage):
    pass
