def _raise_bad_response_format(response: RPCResponse, error: str = "") -> None:
    message = "The response was in an unexpected format and unable to be parsed."
    raw_response = f"The raw response is: {response}"

    if error is not None and error != "":
        error = error[:-1] if error.endswith(".") else error
        message = f"{message} {error}. {raw_response}"
    else:
        message = f"{message} {raw_response}"

    raise BadResponseFormat(message)


from web3.types import (
    BlockIdentifier,
    BlockTrace,
    FilterTrace,
    TraceFilterParams,
    TraceMode,
    TxParams,
    _Hash32,
)


