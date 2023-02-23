import sys

from crystalpol.shared.config import Config

import logging

from crystalpol.shared.utils import weekday_date_time


class Log:
    @staticmethod
    def make_header(version: str, config_dict: dict):
        logging.info(
            f"##########################################################################################\n"
            f"##############             Welcome to CRYSTALPOL version {version}             ##############\n"
            f"##########################################################################################\n"
        )
        logging.info(f"Your python version is {sys.version}\n")
        logging.info(f"Program started on {weekday_date_time()}\n")

        logging.info("------------------------------------------------------------------------------------------")
        logging.info("                   CRYSTALPOL variables being used in this run:                           ")
        logging.info("------------------------------------------------------------------------------------------\n")
        for key, value in config_dict.items():
            logging.info(f"\t{key} = {(key if key else 'Not set')}")

        logging.info("------------------------------------------------------------------------------------------")
        logging.info(f"                                      RUN Results:                                       ")
        logging.info("------------------------------------------------------------------------------------------\n")

    @staticmethod
    def make_run(cycle, max_charge_diff, charge_diff, crystal):
        logging.info(f"cycle: {cycle}")
        logging.info(f"\nMax charge diff: {max_charge_diff}")
        logging.info(f"Charge Diff: {charge_diff}\n")

        logging.info("------------------------------------------------------------------------------------------")
        logging.info(f"             S             rx             ry             rz             chg              ")
        logging.info("------------------------------------------------------------------------------------------")
        for atom in crystal[0][0]:
            logging.info(f"             {atom.symbol}        {atom.rx}        {atom.ry}        {atom.rz}        {atom.chg}    ")

        logging.info("\n------------------------------------------------------------------------------------------\n")


