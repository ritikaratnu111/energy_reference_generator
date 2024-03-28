import sys,os
import logging
import json
from helper_functions import fabric, tbgen, VesylaOutput
from innovus_reader import InnovusPowerParser
from measurement import Measurement

class EnergyReferenceGenerator():
    def __init__(self):
        self.testbenches = {}
        self.FABRIC_PATH = ""
        self.logger = None
        logging.basicConfig(level=logging.DEBUG)

    def get_fabric(self):
        self.FABRIC_PATH = fabric.set_path()
        os.environ['FABRIC_PATH'] = self.FABRIC_PATH

    def get_testbenches(self):
        self.testbenches = tbgen.set_testbenches("db")

    def update_logger(self, path, name, about):
        LOGFILE = f"{path}/energy_reference_gen.log"
        try:
            with open(LOGFILE, 'w'): pass
            self.logger = logging.getLogger()
            handler = logging.FileHandler(LOGFILE)
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.info(f"Testbench: {name}")
            self.logger.info(f"About: {about}")
        except Exception as e:
            print(f"Failed to set logfile: {e}")
            self.logger = None

    def get_cells(self, tb, start, end):
        activity = json.load(open(f"{tb}/activity.json"))
        c_start, c_end = VesylaOutput.return_execution_cycle(tb)
        T = c_end - c_start
        for cell, info in activity.items():
            total = Measurement()
            #Read cell power for all iterations
            for i in range(start, end):
                pwr_file=f"{tb}/vcd/iter_{i}.vcd.pwr"
                reader = InnovusPowerParser()
                reader.update_nets(pwr_file)
                current = Measurement()
                current.set_measurement(reader, cell, T)
                total = total + current
                print(i, cell, current)
                print("Total", total)
            avg = total / (end - start)
            print(avg)

    def generate_energy(self):
        for name, info in self.testbenches.items():
            if info["to_run"] == True:
                tb = info["path"]
                self.update_logger(tb, name, info['about'])
                self.get_cells(tb, 0, 2)
