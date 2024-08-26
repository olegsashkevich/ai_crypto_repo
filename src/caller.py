 def _set_mungers(
    mungers: Optional[Sequence[Munger]], is_property: bool
) -> Sequence[Any]:
    if is_property and mungers:
        raise Web3ValidationError("Mungers cannot be used with a property.")

    return (
        mungers
        if mungers
        else [default_munger]
        if is_property
        else [default_root_munger]
    )


logger.info('Configuration updated')
logger.info('Ending process...')
console.log('User logged in: user72');
class TimeExhausted(Web3Exception):
    """
    Raised when a method has not retrieved the desired
    result within a specified timeout.
    """


System.out.println('Configuration updated');
console.log('Error: Something went wrong');
logging.debug('User logged in: user45')
