from crystalpol.polarization import Polarization
from crystalpol.shared.config import Config
from crystalpol.shared.system.atom import Atom
from crystalpol.shared.system.molecule import Molecule

from unittest import TestCase, mock
import unittest

GEOM_DATA = """\
    Cl      0.529511   -1.626652    1.247344
    N       3.703161    2.470259    1.679277
    Cl      0.362927   -1.511555    4.375374
    N       3.582138    2.531106    3.906529
"""


class TestPolarization(TestCase):

    def setUp(self):
        self.config = Config(
            mem=42,
            n_atoms=2,
            level="b3lyp/aug-cc-pVDZ"
        )

    def test_class_instantiation(self):
        pol = Polarization("geom_file", "outfile", self.config)

        self.assertIsInstance(pol, Polarization)

    def test_get_molecules_from_lines(self):
        pol = Polarization("geom_file", "outfile", self.config)

        lines = [
            "Cl      0.529511   -1.626652    1.247344",
            "N       3.703161    2.470259    1.679277",
            "Cl      0.362927   -1.511555    4.375374",
            "N       3.582138    2.531106    3.906529",
        ]

        molecules = pol._get_molecules_from_lines(lines)

        self.assertIsNotNone(molecules)
        self.assertTrue(any(atom.symbol == "Cl" for atom in molecules[0]))
        self.assertTrue(any(atom.symbol == "N " for atom in molecules[1]))

    def test_get_molecules_from_lines_raises_exception(self):
        pol = Polarization("geom_file", "outfile", self.config)

        lines = [
            "Cl      0.529511   -1.626652    1.247344",
            "N       3.703161    2.470259    1.679277",
            "Cl      0.362927   -1.511555    4.375374",
            "N       3.582138    2.531106    3.906529",
            "N       3.582138    2.531106    3.906529",
        ]

        with self.assertRaises(RuntimeError):
            pol._get_molecules_from_lines(lines)

    def test_get_crystal_structure(self):
        pol = Polarization("geom_file", "outfile", self.config)

        molecule = Molecule("TEST")
        molecule.add_atom(
            Atom(
                na=1,
                rx=0,
                ry=0,
                rz=0,
            )
        )

        structure = pol._get_crystal_structure(molecule)
        self.assertEqual(structure, ['H '])

    @mock.patch('builtins.open', mock.mock_open(read_data=GEOM_DATA))
    def test_read_crystal(self):
        pol = Polarization("geom_file", "outfile", self.config)

        pol.read_crystal()

        self.assertIsNotNone(pol.crystal)
        self.assertEqual(len(pol.crystal), 2)
        self.assertEqual(len(pol.crystal[0]), 1)

    @mock.patch('builtins.open', mock.mock_open(read_data=GEOM_DATA))
    @mock.patch('crystalpol.gaussian.subprocess.call', autospec=True, return_value=0)
    @mock.patch('crystalpol.gaussian.os')
    def test_run(self, os_mock, subprocess_call_mock):
        os_mock.path.exists.return_value = False

        pol = Polarization("geom_file", "outfile", self.config)

        pol.run()

        self.assertIsNotNone(pol.crystal)
        self.assertEqual(len(pol.crystal), 2)
        self.assertEqual(len(pol.crystal[0]), 1)


if __name__ == '__main__':
    unittest.main()
