from tempfile import TemporaryFile

from ruamel.yaml import YAML
from ruamel.yaml.scalarstring import FoldedScalarString

import eyamladd


class TestEyamladd():
    def test_eyaml_block_parsing(self):
        eyaml = """\
    ENC[PKCS7,MIIBeQYJKoZIhvcNAQcDoIIBajCCAWYCAQAxggEhMIIBHQIBADAFMAACAQEw
    DQYJKoZIhvcNAQEBBQAEggEAqcl1NXkwXvasks+WFoWfKjydHk9WuA/NI97u
    of6Gi61pvf6i2ZO45hqUSQVn0Lbz3nH7Juv3kcXGFZlrvi5/UK1jcT7gqOlb
    EWLS+zXFmf26Ou9j4shXiMQPpvPFeqV9X8t+gO84lzJFTgovzgkLNeCD1tIx
    EMqDO8zYXxzXPXT21L2e79XL+qiVWtjsPe2q6TPDJN4BD+lq1laki8CZa5cE
    wNBlWjPtlUVUk8ptSM9xaZMK5q9NRrJ/0uGIeBUAGdM2Po5BfNpfc9YyHFeH
    xbvzUmgkQYVXuvWp0XSM9vRPBZWQtnmqwh2VA22+CgD+mE3drmohraX3hCC1
    UdC6wDA8BgkqhkiG9w0BBwEwHQYJYIZIAWUDBAEqBBD39+PUE1rNQN3rtk9l
    589EgBBFMsMP2N1a4alw3UvIDYRu]
"""
        output = "ENC[PKCS7,MIIBeQYJKoZIhvcNAQcDoIIBajCCAWYCAQAxggEhMIIBHQIBADAFMAACAQEw\u0007\nDQYJKoZIhvcNAQEBBQAEggEAqcl1NXkwXvasks+WFoWfKjydHk9WuA/NI97u\u0007\nof6Gi61pvf6i2ZO45hqUSQVn0Lbz3nH7Juv3kcXGFZlrvi5/UK1jcT7gqOlb\u0007\nEWLS+zXFmf26Ou9j4shXiMQPpvPFeqV9X8t+gO84lzJFTgovzgkLNeCD1tIx\u0007\nEMqDO8zYXxzXPXT21L2e79XL+qiVWtjsPe2q6TPDJN4BD+lq1laki8CZa5cE\u0007\nwNBlWjPtlUVUk8ptSM9xaZMK5q9NRrJ/0uGIeBUAGdM2Po5BfNpfc9YyHFeH\u0007\nxbvzUmgkQYVXuvWp0XSM9vRPBZWQtnmqwh2VA22+CgD+mE3drmohraX3hCC1\u0007\nUdC6wDA8BgkqhkiG9w0BBwEwHQYJYIZIAWUDBAEqBBD39+PUE1rNQN3rtk9l\u0007\n589EgBBFMsMP2N1a4alw3UvIDYRu]\n"
        result = eyamladd.parse_eyaml_block(eyaml)
        assert result == FoldedScalarString(output)

    def test_yaml_output(self):
        eyaml = """\
    ENC[PKCS7,MIIBeQYJKoZIhvcNAQcDoIIBajCCAWYCAQAxggEhMIIBHQIBADAFMAACAQEw
    DQYJKoZIhvcNAQEBBQAEggEAqcl1NXkwXvasks+WFoWfKjydHk9WuA/NI97u
    of6Gi61pvf6i2ZO45hqUSQVn0Lbz3nH7Juv3kcXGFZlrvi5/UK1jcT7gqOlb
    EWLS+zXFmf26Ou9j4shXiMQPpvPFeqV9X8t+gO84lzJFTgovzgkLNeCD1tIx
    EMqDO8zYXxzXPXT21L2e79XL+qiVWtjsPe2q6TPDJN4BD+lq1laki8CZa5cE
    wNBlWjPtlUVUk8ptSM9xaZMK5q9NRrJ/0uGIeBUAGdM2Po5BfNpfc9YyHFeH
    xbvzUmgkQYVXuvWp0XSM9vRPBZWQtnmqwh2VA22+CgD+mE3drmohraX3hCC1
    UdC6wDA8BgkqhkiG9w0BBwEwHQYJYIZIAWUDBAEqBBD39+PUE1rNQN3rtk9l
    589EgBBFMsMP2N1a4alw3UvIDYRu]
"""
        output = """\
test: >
  ENC[PKCS7,MIIBeQYJKoZIhvcNAQcDoIIBajCCAWYCAQAxggEhMIIBHQIBADAFMAACAQEw
  DQYJKoZIhvcNAQEBBQAEggEAqcl1NXkwXvasks+WFoWfKjydHk9WuA/NI97u
  of6Gi61pvf6i2ZO45hqUSQVn0Lbz3nH7Juv3kcXGFZlrvi5/UK1jcT7gqOlb
  EWLS+zXFmf26Ou9j4shXiMQPpvPFeqV9X8t+gO84lzJFTgovzgkLNeCD1tIx
  EMqDO8zYXxzXPXT21L2e79XL+qiVWtjsPe2q6TPDJN4BD+lq1laki8CZa5cE
  wNBlWjPtlUVUk8ptSM9xaZMK5q9NRrJ/0uGIeBUAGdM2Po5BfNpfc9YyHFeH
  xbvzUmgkQYVXuvWp0XSM9vRPBZWQtnmqwh2VA22+CgD+mE3drmohraX3hCC1
  UdC6wDA8BgkqhkiG9w0BBwEwHQYJYIZIAWUDBAEqBBD39+PUE1rNQN3rtk9l
  589EgBBFMsMP2N1a4alw3UvIDYRu]
"""
        # Annoyingly, ruamel.yaml dump does not have a simple way to write to a
        # string instead of a stream (e.g. dumps), so use a tempfile instead.
        with TemporaryFile() as f:
            yaml = YAML()
            yaml.dump({'test': eyamladd.parse_eyaml_block(eyaml)}, f)

            # Ensure the file is ready to be read from after the write
            f.flush()
            f.seek(0)
            result = f.read().decode()

        assert result == output

    def test_deep_merge(self):
        src = {
            'key1b': 'newvalue1b',
            'newkey1': 'newvalue1',
            'key1c': {
                'key2b': {
                    'key3b': [
                        'item2'
                    ]
                }
            }
        }

        dst = {
            'key1a': 'value1a',
            'key1b': 'value1b',
            'key1c': {
                'key2a': 'value2a',
                'key2b': {
                    'key3a': 'value3a',
                    'key3b': [
                        'item1',
                        'item2',
                        {
                            'key5a': 'value5a'
                        }
                    ]
                }
            }
        }

        # Note that lists are appended to when merged
        merged = {
            'key1a': 'value1a',
            'key1b': 'newvalue1b',
            'newkey1': 'newvalue1',
            'key1c': {
                'key2a': 'value2a',
                'key2b': {
                    'key3a': 'value3a',
                    'key3b': [
                        'item1',
                        'item2',
                        {
                            'key5a': 'value5a',
                        },
                        'item2'
                    ]
                }
            }
        }

        eyamladd.merge(dst, src)
        assert dst == merged

    def test_encrypt_all(self, monkeypatch):
        def mockencrypt(data, public_key):
            return FoldedScalarString('encrypted')

        data = {
            'test1': 'cleartext1',
            'test2': {
                'test3': 'cleartext2',
                'test4': [
                    'cleartext3',
                    {
                        'test5': 'cleartext4'
                    },
                ]
            }
        }

        output = {
            'test1': 'encrypted',
            'test2': {
                'test3': 'encrypted',
                'test4': [
                    'encrypted',
                    {
                        'test5': 'encrypted'
                    },
                ]
            }
        }

        monkeypatch.setattr(eyamladd, "encrypt", mockencrypt)
        result = dict(eyamladd.encrypt_all(data, None))
        assert result == output
