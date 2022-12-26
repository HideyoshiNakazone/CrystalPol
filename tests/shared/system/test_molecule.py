from crystalpol.shared.system.molecule import Molecule
from crystalpol.shared.system.atom import Atom

import io

import unittest


class TestMolecule(unittest.TestCase):
    def test_class_instantiation(self):
        molecule = Molecule("TEST")

        self.assertEqual(molecule.mol_name, "TEST")
        self.assertIsInstance(molecule, Molecule)

    def test_add_atom(self):
        molecule = Molecule("TEST")

        atom = Atom(
            na=1,
            rx=0,
            ry=0,
            rz=0,
        )

        molecule.add_atom(atom)

        self.assertEqual(len(molecule.atoms), 1)
        self.assertEqual(molecule.atoms[0], atom)

    def test_update_charges(self):
        molecule = Molecule("TEST")

        atom = Atom(
            na=1,
            rx=0,
            ry=0,
            rz=0,
        )

        molecule.add_atom(atom)

        molecule.update_charges([1])

        self.assertEqual(molecule.atoms[-1].chg, 1)

    def test_update_charges_raises_exception(self):
        molecule = Molecule("TEST")

        atom = Atom(
            na=1,
            rx=0,
            ry=0,
            rz=0,
        )

        molecule.add_atom(atom)

        with self.assertRaises(ValueError):
            molecule.update_charges([1, 1])

    def test_print_mol_info(self):
        molecule = Molecule("TEST")

        atom = Atom(
            na=1,
            rx=0,
            ry=0,
            rz=0,
        )

        molecule.add_atom(atom)

        with io.StringIO() as file:
            molecule.print_mol_info(file)

            file.seek(0)
            info_string = file.read()

        self.assertIsNotNone(info_string)
        self.assertTrue(len(info_string) > 0)
        self.assertTrue("Molecule Name: TEST" in info_string)
        self.assertTrue("H    r: [0, 0, 0]    charge: None" in info_string)


if __name__ == '__main__':
    unittest.main()
