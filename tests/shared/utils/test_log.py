from crystalpol.shared.system.molecule import Molecule
from crystalpol.shared.system.crystal import Crystal
from crystalpol.shared.system.atom import Atom
from crystalpol.shared.config import Config
from crystalpol.shared.utils.log import Log

from io import StringIO
import logging

from unittest import TestCase, mock


class TestLog(TestCase):

    def setUp(self):

        self.log_stream = StringIO()
        logging.basicConfig(
            stream=self.log_stream,
            format='%(message)s',
            level=logging.INFO
        )
        self.logger = logging.getLogger()

    def tearDown(self):
        logging.getLogger().removeHandler(
            logging.getLogger().handlers[0]
        )
        del self.logger
        del self.log_stream

    @mock.patch('crystalpol.shared.utils.log.sys')
    @mock.patch('crystalpol.shared.utils.log.weekday_date_time')
    def test_make_header(self, weekday_date_time_mock, sys_mock):
        weekday_date_time_mock.return_value = 'Test Day'
        sys_mock.version = 'Test Version'

        config = Config(
            mem=1,
            level="b3lyp/aug-cc-pVDZ",
            n_atoms=10
        )
        Log.make_header('test', config.to_dict(), logger=self.logger)

        expected_log_stream = [
            '##########################################################################################\n',
            '##############             Welcome to CRYSTALPOL version test             ##############\n',
            '##########################################################################################\n', '\n',
            'Your python version is Test Version\n', '\n',
            'Program started on Test Day\n', '\n',
            '------------------------------------------------------------------------------------------\n',
            '                   CRYSTALPOL variables being used in this run:                           \n',
            '------------------------------------------------------------------------------------------\n', '\n',
            '\tmem = 1\n',
            '\tlevel = b3lyp/aug-cc-pVDZ\n',
            '\tn_atoms = 10\n',
            '\tn_procs = 1\n',
            '\tpop = chelpg\n',
            '\tcomment = crystalpol\n',
            '\tmult = [0, 1]\n',
            '------------------------------------------------------------------------------------------\n',
            '                                      RUN Results:                                       \n',
            '------------------------------------------------------------------------------------------\n', '\n'
        ]

        self.log_stream.seek(0)

        self.assertEqual(self.log_stream.readlines(), expected_log_stream)

    def test_make_run(self):

        Log.make_run(1, 0.000000, [], self.create_crystal(), logger=self.logger)

        expected_log_stream = [
            'cycle: 1\n', '\n',
            'Max charge diff: 0.00000\n',
            'Charge Diff: []\n', '\n',
            '------------------------------------------------------------------------------------------\n',
            '             S             rx             ry             rz             chg               \n',
            '------------------------------------------------------------------------------------------\n',
            '             H          0.000000       0.000000       0.000000       0.000000             \n', '\n',
            '------------------------------------------------------------------------------------------\n', '\n'
        ]

        self.log_stream.seek(0)

        self.assertEqual(self.log_stream.readlines(), expected_log_stream)

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
                rx=0.000000,
                ry=0.000000,
                rz=0.000000,
                chg=0.000000
            )
        )

        crystal.add_cell([molecule])
        crystal.add_cell([molecule])

        return crystal
