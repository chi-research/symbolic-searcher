TXHASH=0x93b1a493e9d871b9d3f553996653c4d2f50bf6a2c744ce31e8de89956472863e

# EXEC DEBUGGER 
hevm exec  \
  --caller $(seth tx $TXHASH from) \
  --address $(seth tx $TXHASH to) \
  --calldata 0x6d4ce63c \
  --rpc $ETH_RPC_URL \
  --block 10741412 \
  --gas 1000000000 \
  --code $(cat BytecodeInjectorOutput.bin-runtime) \
  --debug
