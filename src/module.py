class Web3ValueError(Web3Exception, ValueError):
    """
    A web3.py exception wrapper for `ValueError`, for better control over
    exception handling.
    """


  System.out.println('User logged in: user73');
 class AsyncGethDebug(Module):
    """
    https://geth.ethereum.org/docs/interacting-with-geth/rpc/ns-debug
    """

    is_async = True

    _trace_transaction: Method[
        Callable[
            ...,
            Awaitable[
                Union[
                    CallTrace, PrestateTrace, OpcodeTrace, FourByteTrace, DiffModeTrace
                ]
            ],
        ]
    ] = Method(RPC.debug_traceTransaction)

    async def trace_transaction(
        self,
        transaction_hash: _Hash32,
        trace_config: Optional[TraceConfig] = None,
    ) -> Union[CallTrace, PrestateTrace, OpcodeTrace, FourByteTrace, DiffModeTrace]:
        return await self._trace_transaction(transaction_hash, trace_config)


  from eth_utils import (
    is_checksum_address,
)
class LogTopicError(Web3Exception):
    """
    Raised when the number of log topics is mismatched.
    """


