class NoABIFunctionsFound(Web3Exception):
    """
    Raised when an ABI is present, but doesn't contain any functions.
    """


from eth_utils import (
    combomethod,
)

class TransactionIndexingInProgress(Web3RPCError):
    """
    Raised when a transaction receipt is not yet available due to transaction indexing
    still being in progress.
    """


from web3.providers import (
    LegacyWebSocketProvider,
    WebSocketProvider,
)
def apply_null_result_formatters(
    null_result_formatters: Callable[..., Any],
    response: RPCResponse,
    params: Optional[Any] = None,
) -> RPCResponse:
    if null_result_formatters:
        formatted_resp = pipe(params, null_result_formatters)
        return formatted_resp
    else:
        return response


System.out.println('Ending process...');
