from crystalpol.shared.system.molecule import Molecule

from typing import List


class Crystal:
    """
    This class represents a crystal, it will be organized in a list structure.
    Each element is a unitary cell in the crystal. And this unitary cell will have
    Molecules in it.
    """

    def __init__(self, structure: List[List[str]]):
        self.structure = structure

        self.cells = []

    def __iter__(self):
        for cell in self.cells:
            yield cell

    def __len__(self):
        return len(self.cells)

    def __getitem__(self, index):
        return self.cells[index]

    def add_cell(self, cell: List[Molecule]) -> None:
        valid = self._is_valid_cell(cell)
        if not valid:
            raise ValueError(
                "This cell does not obey the declared format for this Crystal."
            )
        else:
            self.cells.append(cell)

    def get_number_of_charges(self):
        return len(self.cells[0][0])

    def _is_valid_cell(self, cell: List[Molecule]) -> bool:
        if len(cell) == len(self.structure):
            for i, molecule in enumerate(cell):
                if len(molecule.atoms) == len(self.structure[i]) \
                        and all(atom.symbol == self.structure[i][j] for j, atom in enumerate(molecule.atoms)):
                    return True
        return False
