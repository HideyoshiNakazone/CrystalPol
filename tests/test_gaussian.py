import os

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

    @mock.patch('crystalpol.gaussian.os')
    def test_create_step_dir(self, os_mock):
        os_mock.path.exists.return_value = False
        os_mock.makedirs = mock.MagicMock()

        gaussian = Gaussian(
            Config(
                mem=1,
                level="b3lyp/aug-cc-pVDZ",
                n_atoms=10
            )
        )
        gaussian.create_step_dir(1)

        self.assertTrue(os_mock.makedirs.called)

    @mock.patch('crystalpol.gaussian.os')
    def test_create_step_dir_raises_exception(self, os_mock):
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
            gaussian.create_step_dir(1)

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
        gaussian_input = gaussian.make_gaussian_input(1, Path('test.gjf'), crystal)
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
        gaussian_input = gaussian.make_gaussian_input(2, Path('test.gjf'), crystal)
        expected_output = """\
%Mem=1Gb
%Nprocs=1
#P b3lyp/aug-cc-pVDZ Pop=chelpg Density=Current NoSymm charge

crystalpol - Cycle number 2

0 1
H        0.00000       0.00000       0.00000

   0.00000       0.00000       0.00000       0.00000
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
        expected_charges = '   0.00000       0.00000       0.00000       0.00000\n'

        self.assertEqual(charges_string, expected_charges)

    @mock.patch('crystalpol.gaussian.subprocess.call', autospec=True, return_value=0)
    @mock.patch('crystalpol.gaussian.Gaussian.create_step_dir')
    @mock.patch('crystalpol.gaussian.Gaussian.make_gaussian_input')
    @mock.patch('crystalpol.gaussian.Gaussian.read_charges_from_gaussian_output')
    def test_run(self,
                 read_charges_from_gaussian_output_mock,
                 make_gaussian_input_mock,
                 create_step_dir_mock,
                 subprocess_call_mock):
        gaussian = Gaussian(
            Config(
                mem=1,
                level="b3lyp/aug-cc-pVDZ",
                n_atoms=10
            )
        )
        gaussian.run(1, self.create_crystal())

        self.assertTrue(read_charges_from_gaussian_output_mock.called)
        self.assertTrue(make_gaussian_input_mock.called)
        self.assertTrue(create_step_dir_mock.called)
        self.assertTrue(subprocess_call_mock.called)

    @mock.patch('crystalpol.gaussian.subprocess.call', autospec=True, return_value=1)
    @mock.patch('crystalpol.gaussian.Gaussian.create_step_dir')
    @mock.patch('crystalpol.gaussian.Gaussian.make_gaussian_input')
    @mock.patch('crystalpol.gaussian.Gaussian.read_charges_from_gaussian_output')
    def test_run_raises_exception(self,
                                  read_charges_from_gaussian_output_mock,
                                  make_gaussian_input_mock,
                                  create_step_dir_mock,
                                  subprocess_call_mock):
        gaussian = Gaussian(
            Config(
                mem=1,
                level="b3lyp/aug-cc-pVDZ",
                n_atoms=10
            )
        )

        with self.assertRaises(RuntimeError):
            gaussian.run(1, self.create_crystal())

    @mock.patch('crystalpol.gaussian.open')
    def test_read_charges_from_gaussian_output(self, open_mock):
        if Path('tests').exists():
            os.chdir('tests')

        gaussian_output_file = Path('test_files/gaussian_output_example.log')
        with open(gaussian_output_file) as output_file:
            open_mock.return_value\
                .__enter__.return_value\
                .readlines.return_value = output_file.readlines()

        gaussian = Gaussian(
            Config(
                mem=1,
                level="b3lyp/aug-cc-pVDZ",
                n_atoms=10
            )
        )

        charges = gaussian.read_charges_from_gaussian_output(1, 18)

        expected_charges = [-0.12115, -0.107139, -0.684426, -0.516473, 0.512777, -0.083045, 0.397921, 0.129877, -0.214313, 0.036208, 0.109865, -0.287406, 0.184608, 0.158182, 0.362283, 0.021345, 0.035903, 0.064983]

        self.assertEqual(charges, expected_charges)

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
                chg=0
            )
        )

        crystal.add_cell([molecule])
        crystal.add_cell([molecule])

        return crystal


if __name__ == '__main__':
    unittest.main()
