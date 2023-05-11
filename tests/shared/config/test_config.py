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

    def test_config_raises_exception_on_mem_none(self):
        with self.assertRaises(ValueError):
            Config(
                mem=None,
                level="b3lyp/aug-cc-pVDZ",
                n_atoms=10
            )

    def test_config_raises_exception_on_mem_zero_or_negative(self):

        with self.assertRaises(ValueError):
            Config(
                mem=0,
                level="b3lyp/aug-cc-pVDZ",
                n_atoms=10
            )

        with self.assertRaises(ValueError):
            Config(
                mem=-1,
                level="b3lyp/aug-cc-pVDZ",
                n_atoms=10
            )

    def test_config_raises_exception_on_level_none(self):

        with self.assertRaises(ValueError):
            Config(
                mem=1,
                level=None,
                n_atoms=10
            )

    def test_config_raises_exception_on_n_atoms_zero(self):

        with self.assertRaises(ValueError):
            Config(
                mem=1,
                level="b3lyp/aug-cc-pVDZ",
                n_atoms=0
            )

    def test_set_charge_tolerance(self):
        config = Config(
            mem=1,
            level="b3lyp/aug-cc-pVDZ",
            n_atoms=10,
            charge_tolerance=0.001
        )
        self.assertEqual(config.charge_tolerance, 0.001)
