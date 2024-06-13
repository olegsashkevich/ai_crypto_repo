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
