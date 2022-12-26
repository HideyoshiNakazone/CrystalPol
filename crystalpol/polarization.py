import os

from crystalpol.shared.system.molecule import Molecule
from crystalpol.shared.system.crystal import Crystal
from crystalpol.shared.system.atom import Atom
from crystalpol.shared.config import Config
from crystalpol.gaussian import Gaussian

from typing import List


class Polarization:
    __slots__ = ('geom_file', 'outfile', 'config', 'gaussian', 'crystal')

    def __init__(self, geom_file: str, outfile: str, config: Config) -> None:
        self.crystal = None

        self.geom_file = geom_file
        self.outfile = outfile
        self.config = config

        self.gaussian = Gaussian(config)

    def run(self):

        self.read_crystal()

        self.gaussian.run(1, self.crystal)

    def read_crystal(self) -> None:
        with open(self.geom_file, 'r') as geom_file:
            lines = geom_file.readlines()

        molecules = self._get_molecules_from_lines(lines)
        structure = self._get_crystal_structure(molecules[0])

        self.crystal = Crystal([structure])
        for molecule in molecules:
            self.crystal.add_cell([molecule])

    def _get_molecules_from_lines(self, lines: List[str]) -> List[Molecule]:
        if (len(lines) % self.config.n_atoms) == 0:
            molecules: List[Molecule] = []

            for index, molecule in enumerate(split(lines, self.config.n_atoms)):
                mol = Molecule(f"Molecule-{index}")
                for atom_line in molecule:
                    symbol, rx, ry, rz = tuple(atom_line.split())
                    mol.add_atom(
                        Atom(
                            rx, ry, rz,
                            symbol=symbol.ljust(2),
                        )
                    )
                molecules.append(mol)

            return molecules

        else:
            raise RuntimeError(
                "Invalid Geom File, the number of atoms doesn't match the number of lines."
            )

    @staticmethod
    def _get_crystal_structure(molecule: Molecule) -> List[str]:
        structure: List[str] = []
        for atom in molecule:
            structure.append(atom.symbol)
        return structure


def split(array: List, partitions: int):
    for i in range(0, len(array), partitions):
        yield array[i: i + partitions]
