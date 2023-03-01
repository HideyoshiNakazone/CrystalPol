from crystalpol.shared.utils import weekday_date_time

import logging
import sys


class Log:
    @staticmethod
    def make_header(version: str, config_dict: dict, logger=None):

        if logger is None:
            logger = logging.getLogger()

        logger.info(
            f"##########################################################################################\n"
            f"##############             Welcome to CRYSTALPOL version {version}             ##############\n"
            f"##########################################################################################\n"
        )
        logger.info(f"Your python version is {sys.version}\n")
        logger.info(f"Program started on {weekday_date_time()}\n")

        logger.info("------------------------------------------------------------------------------------------")
        logger.info("                   CRYSTALPOL variables being used in this run:                           ")
        logger.info("------------------------------------------------------------------------------------------\n")
        for key, value in config_dict.items():
            logger.info(f"\t{key} = {(value if value else 'Not set')}")

        logger.info("------------------------------------------------------------------------------------------")
        logger.info(f"                                      RUN Results:                                       ")
        logger.info("------------------------------------------------------------------------------------------\n")

    @staticmethod
    def make_run(cycle, max_charge_diff, charge_diff, crystal, logger=None):

        if logger is None:
            logger = logging.getLogger()

        logger.info(f"cycle: {cycle}")
        logger.info(f"\nMax charge diff: {max_charge_diff:.5f}")
        logger.info(f"Charge Diff: {charge_diff}\n")

        logger.info(f"------------------------------------------------------------------------------------------")
        logger.info(f"             S             rx             ry             rz             chg               ")
        logger.info(f"------------------------------------------------------------------------------------------")
        for atom in crystal[0][0]:
            logger.info(
                f"             {atom.symbol.rjust(2)}         {float(atom.rx):.6f}       {float(atom.ry):.6f}       {float(atom.rz):.6f}       {float(atom.chg):.6f}             ")

        logger.info("\n------------------------------------------------------------------------------------------\n")
