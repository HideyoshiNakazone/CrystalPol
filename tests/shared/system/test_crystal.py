import unittest

from crystalpol.shared.system.atom import Atom
from crystalpol.shared.system.crystal import Crystal
from crystalpol.shared.system.molecule import Molecule


class TestCrystal(unittest.TestCase):
    def test_class_instantiation(self):
        # Note that this is not a valid crystal
        crystal_structure = [
            ['H']
        ]

        crystal = Crystal(crystal_structure)

        self.assertIsInstance(crystal, Crystal)

    def test_is_valid_cell(self):
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

        self.assertTrue(crystal._is_valid_cell([molecule]))

        molecule.add_atom(
            Atom(
                na=1,
                rx=0,
                ry=0,
                rz=0,
            )
        )

        self.assertFalse(crystal._is_valid_cell([molecule]))

    def test_add_cell(self):
        # Note that this is not a valid crystal
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

        self.assertIsInstance(crystal, Crystal)

    def test_add_cell_raises_exception(self):
        # Note that this is not a valid crystal
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
        molecule.add_atom(
            Atom(
                na=1,
                rx=0,
                ry=0,
                rz=0,
            )
        )

        with self.assertRaises(ValueError):
            crystal.add_cell([molecule])


if __name__ == '__main__':
    unittest.main()
