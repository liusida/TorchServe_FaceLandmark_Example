import argparse
import torch
from torch import nn

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--path", help="path to store the dummy model.")
args = parser.parse_args()

class DummyModel(torch.jit.ScriptModule):
    pass


torch.jit.save(DummyModel(), args.path)
