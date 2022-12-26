from crystalpol.shared.config import Config

import unittest


class TestConfig(unittest.TestCase):
    def test_class_instantiation(self):
        config = Config(
            mem=1,
            level="b3lyp/aug-cc-pVDZ",
            n_atoms=10
        )
        self.assertIsInstance(config, Config)

    def test_config_raises_exception(self):
        with self.assertRaises(ValueError):
            Config(
                mem="1",
                level="b3lyp/aug-cc-pVDZ",
                n_atoms=10
            )
