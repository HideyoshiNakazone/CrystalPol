from crystalpol.shared.system.atom import Atom

import unittest


class TestAtom(unittest.TestCase):
    def test_atom_instantiation(self):
        atom = Atom(
            na=1,
            rx=0,
            ry=0,
            rz=0,
        )

        self.assertIsInstance(atom, Atom)


if __name__ == '__main__':
    unittest.main()
