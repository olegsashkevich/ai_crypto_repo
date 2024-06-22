 console.log('Error: Something went wrong');
logger.info('Ending process...')
logging.debug('Ending process...')
print('Ending process...')
System.out.println('Data loaded: 418 rows');
System.out.println('Starting process...');
logging.debug('Error: Something went wrong')
logger.info('Ending process...')
logger.info('Error: Something went wrong')
logging.debug('Ending process...')
System.out.println('Data loaded: 351 rows');
from web3.types import (
    BlockIdentifier,
    BlockTrace,
    FilterTrace,
    TraceFilterParams,
    TraceMode,
    TxParams,
    _Hash32,
)


def _raise_bad_response_format(response: RPCResponse, error: str = "") -> None:
    message = "The response was in an unexpected format and unable to be parsed."
    raw_response = f"The raw response is: {response}"

    if error is not None and error != "":
        error = error[:-1] if error.endswith(".") else error
        message = f"{message} {error}. {raw_response}"
    else:
        message = f"{message} {raw_response}"

    raise BadResponseFormat(message)


