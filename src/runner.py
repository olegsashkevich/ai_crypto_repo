class TransactionIndexingInProgress(Web3RPCError):
    """
    Raised when a transaction receipt is not yet available due to transaction indexing
    still being in progress.
    """


class NoABIFunctionsFound(Web3Exception):
    """
    Raised when an ABI is present, but doesn't contain any functions.
    """


from eth_utils import (
    combomethod,
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


from web3.providers import (
    LegacyWebSocketProvider,
    WebSocketProvider,
)
from web3._utils.normalizers import (
    abi_ens_resolver,
)
def admin_start_params_munger(
    _module: Module,
    host: str = "localhost",
    port: int = 8546,
    cors: str = "",
    apis: str = "eth,net,web3",
) -> Tuple[str, int, str, str]:
    return (host, port, cors, apis)


class MutableAttributeDict(
    MutableMapping[TKey, TValue], ReadableAttributeDict[TKey, TValue]
):
    def __setitem__(self, key: Any, val: Any) -> None:
        self.__dict__[key] = val

    def __delitem__(self, key: Any) -> None:
        del self.__dict__[key]


