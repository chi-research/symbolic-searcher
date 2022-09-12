CONTRACT_ADDR=0xa4004b352fcbb913f0ddaba2454e7ff9cb64bdf6

# SYMBOLIC
hevm symbolic \
  --rpc $ETH_RPC_URL \
  --address $CONTRACT_ADDR \
  --sig "get()"\
  --get-models \
  --show-tree \
  --storage-model ConcreteS \
  --code $(cat BytecodeInjectorOutput.bin-runtime) \
  --block 10741412 \
