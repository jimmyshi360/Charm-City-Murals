from tensorflow.python.tools import inspect_checkpoint as inch
inch.print_tensors_in_checkpoint_file(CHECKPOINTS_DIR + "/model.ckpt", '', True)
from tensorflow.contrib.framework.python.framework import load_checkpoint
ckpt = load_checkpoint(CHECKPOINTS_DIR + "/model.ckpt")

variables = {}
for op in g.get_operations():
  if op.op_def and op.op_def.name=='VariableV2':
      print(op.name)
      variables[op.name] = ckpt.get_tensor(op.name)
