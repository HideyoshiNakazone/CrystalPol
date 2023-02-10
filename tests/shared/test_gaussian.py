from crystalpol.shared.system.molecule import Molecule
from crystalpol.shared.system.crystal import Crystal
from crystalpol.shared.system.atom import Atom
from crystalpol.shared.config import Config
from crystalpol.gaussian import Gaussian

from pathlib import Path
from io import StringIO

from unittest import mock, TestCase
import unittest


class TestGaussian(TestCase):

    def test_class_instantiation(self):
        gaussian = Gaussian(
            Config(
                mem=1,
                level="b3lyp/aug-cc-pVDZ",
                n_atoms=10
            )
        )

        self.assertIsInstance(gaussian, Gaussian)

    def test_check_keyword(self):
        gaussian = Gaussian(
            Config(
                mem=1,
                level="b3lyp/aug-cc-pVDZ",
                n_atoms=10,
                pop="lorota"
            )
        )

        self.assertEqual(gaussian.config.pop, "chelpg")

    @mock.patch('crystalpol.gaussian.os')
    def test_create_simulation_dir(self, os_mock):
        os_mock.path.exists.return_value = False
        os_mock.makedirs = mock.MagicMock()

        gaussian = Gaussian(
            Config(
                mem=1,
                level="b3lyp/aug-cc-pVDZ",
                n_atoms=10
            )
        )
        gaussian.create_simulation_dir()

        self.assertTrue(os_mock.makedirs.called)

    @mock.patch('crystalpol.gaussian.os')
    def test_create_simulation_dir_raises_exception(self, os_mock):
        os_mock.path.exists.return_value = True
        os_mock.makedirs = mock.MagicMock()
        gaussian = Gaussian(
            Config(
                mem=1,
                level="b3lyp/aug-cc-pVDZ",
                n_atoms=10
            )
        )

        with self.assertRaises(RuntimeError):
            gaussian.create_simulation_dir()

    # @mock.patch('crystalpol.gaussian.os')
    @mock.patch('crystalpol.gaussian.open')
    def test_make_gaussian_input_cycle_1(self, open_mock):

        open_mock.return_value = StringIO()

        crystal = self.create_crystal()

        gaussian = Gaussian(
            Config(
                mem=1,
                level="b3lyp/aug-cc-pVDZ",
                n_atoms=10
            )
        )
        gaussian_input = gaussian.make_gaussian_input(1, Path(), crystal)
        expected_output = """\
%Mem=1Gb
%Nprocs=1
#P b3lyp/aug-cc-pVDZ Pop=chelpg Density=Current NoSymm

crystalpol - Cycle number 1

0 1
H        0.00000       0.00000       0.00000

"""
        self.assertEqual(gaussian_input, expected_output)

    @mock.patch('crystalpol.gaussian.open')
    def test_make_gaussian_input_cycle_2(self, open_mock):

        open_mock.return_value = StringIO()

        crystal = self.create_crystal()

        gaussian = Gaussian(
            Config(
                mem=1,
                level="b3lyp/aug-cc-pVDZ",
                n_atoms=10
            )
        )
        gaussian_input = gaussian.make_gaussian_input(2, "test", crystal)
        expected_output = """\
%Mem=1Gb
%Nprocs=1
#P b3lyp/aug-cc-pVDZ Pop=chelpg Density=Current NoSymm charge

crystalpol - Cycle number 2

0 1
H        0.00000       0.00000       0.00000

H        0.00000       0.00000       0.00000

"""
        self.assertEqual(gaussian_input, expected_output)

    def test_make_gaussian_charges(self):

        file = StringIO()
        crystal = self.create_crystal()

        gaussian = Gaussian(
            Config(
                mem=1,
                level="b3lyp/aug-cc-pVDZ",
                n_atoms=10
            )
        )
        gaussian.make_gaussian_charges(file, crystal)
        file.seek(0)

        charges_string = file.read()
        expected_charges = 'H        0.00000       0.00000       0.00000\n\n'

        self.assertEqual(charges_string, expected_charges)

    @mock.patch('crystalpol.gaussian.os')
    @mock.patch('crystalpol.gaussian.subprocess.call', autospec=True, return_value=0)
    @mock.patch('crystalpol.gaussian.Gaussian.make_gaussian_input')
    def test_run(self, make_gaussian_input_mock, subprocess_call_mock, os_mock):
        os_mock.path.exists.return_value = False

        gaussian = Gaussian(
            Config(
                mem=1,
                level="b3lyp/aug-cc-pVDZ",
                n_atoms=10
            )
        )
        gaussian.run(1, self.create_crystal())

        self.assertTrue(subprocess_call_mock.called)

    @mock.patch('crystalpol.gaussian.os')
    @mock.patch('crystalpol.gaussian.subprocess.call', autospec=True, return_value=1)
    @mock.patch('crystalpol.gaussian.Gaussian.make_gaussian_input')
    def test_run_raises_exception(self, subprocess_call_mock, make_gaussian_input_mock, os_mock):
        os_mock.path.exists.return_value = False

        gaussian = Gaussian(
            Config(
                mem=1,
                level="b3lyp/aug-cc-pVDZ",
                n_atoms=10
            )
        )

        with self.assertRaises(RuntimeError):
            gaussian.run(1, self.create_crystal())

    @staticmethod
    def create_crystal():

        crystal_structure = [
            ['H ']
        ]

        crystal = Crystal(crystal_structure)

        molecule = Molecule("TESTE")
        molecule.add_atom(
            Atom(
                na=1,
                rx=0,
                ry=0,
                rz=0,
            )
        )

        crystal.add_cell([molecule])
        crystal.add_cell([molecule])

        return crystal


if __name__ == '__main__':
    unittest.main()
