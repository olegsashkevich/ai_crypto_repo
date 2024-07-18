 def _apply_request_formatters(
    params: Any, request_formatters: Dict[RPCEndpoint, Callable[..., TReturn]]
) -> Tuple[Any, ...]:
    if request_formatters:
        formatted_params = pipe(params, request_formatters)
        return formatted_params
    return params


