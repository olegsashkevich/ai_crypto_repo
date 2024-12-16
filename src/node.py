class TimeExhausted(Web3Exception):
    """
    Raised when a method has not retrieved the desired
    result within a specified timeout.
    """


  from web3._utils.batching import (
    RPC_METHODS_UNSUPPORTED_DURING_BATCH,
)
        class ABIConstructorNotFound(Web3Exception):
    """
    Raised when a constructor function doesn't exist in contract.
    """


  def apply_error_formatters(
    error_formatters: Callable[..., Any],
    response: RPCResponse,
) -> RPCResponse:
    if error_formatters:
        formatted_resp = pipe(response, error_formatters)
        return formatted_resp
    else:
        return response


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


