from crystalpol.shared.system.atom import Atom
from crystalpol.shared.utils.ptable import atom_symbol

from typing import Final, List, TextIO
import math


""" Constants of unit conversion """
BOHR2ANG: Final[float] = 0.52917721092
ANG2BOHR: Final[float] = 1 / BOHR2ANG


class Molecule:
    """
    Molecule class declaration. This class is used throughout the DicePlayer program to represent molecules.

    Atributes:
        molname (str): The name of the represented molecule
        atom (List[Atom]): List of atoms of the represented molecule
        position (NDArray[Any, Any]): The position relative to the internal atoms of the represented molecule
        energy (NDArray[Any, Any]): The energy of the represented molecule
        gradient (NDArray[Any, Any]): The first derivative of the energy relative to the position
        hessian (NDArray[Any, Any]): The second derivative of the energy relative to the position
        total_mass (int): The total mass of the molecule
        com (NDArray[Any, Any]): The center of mass of the molecule
    """

    __slots__ = (
        'mol_name',
        'atoms',
        'position'
    )

    def __init__(self, mol_name: str) -> None:
        """
        The constructor function __init__ is used to create new instances of the Molecule class.

        Args:
            mol_name (str): Molecule name
        """
        self.mol_name: str = mol_name

        self.atoms: List[Atom] = []

    def __iter__(self):
        for atom in self.atoms:
            yield atom

    def __len__(self):
        return len(self.atoms)

    def add_atom(self, a: Atom) -> None:
        """
        Adds Atom instance to the molecule.

        Args:
            a (Atom): Atom instance to be added to atom list.
        """

        self.atoms.append(a)

    def update_charges(self, charges: List[float]) -> None:

        if len(charges) != len(self.atoms):
            raise ValueError(
                f"The number of charges ({len(charges)}) does not match the number of atoms ({len(self.atoms)})"
            )

        for i, atom in enumerate(self.atoms):
            atom.chg = charges[i]

    def print_mol_info(self, fh: TextIO) -> None:
        """
        Prints the Molecule information into a Output File

        Args:
            fh (TextIO): Output File
        """

        fh.write("-"*80)
        fh.write(f"Molecule Name: {self.mol_name}\n")

        fh.write("\n")

        for atom in self.atoms:
            fh.write(f"{atom_symbol[atom.na]}   r: [{atom.rx}, {atom.ry}, {atom.rz}]    charge: {atom.chg}")
