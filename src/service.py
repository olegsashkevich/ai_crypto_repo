from eth_utils.toolz import (
    assoc,
)

class GethDebug(Module):
    """
    https://geth.ethereum.org/docs/interacting-with-geth/rpc/ns-debug
    """

    def trace_transaction_munger(
        self,
        transaction_hash: _Hash32,
        trace_config: Optional[TraceConfig] = None,
    ) -> Tuple[_Hash32, TraceConfig]:
        return (transaction_hash, trace_config)

    trace_transaction: Method[
        Callable[
            ...,
            Union[CallTrace, PrestateTrace, OpcodeTrace, DiffModeTrace, FourByteTrace],
        ]
    ] = Method(
        RPC.debug_traceTransaction,
        mungers=[trace_transaction_munger],
    )


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


class Module:
    is_async = False

    def __init__(self, w3: Union["AsyncWeb3", "Web3"]) -> None:
        if self.is_async:
            self.retrieve_caller_fn = retrieve_async_method_call_fn(w3, self)
        else:
            self.retrieve_caller_fn = retrieve_blocking_method_call_fn(w3, self)
        self.retrieve_request_information = retrieve_request_information_for_batching(
            w3, self
        )
        self.w3 = w3

    @property
    def codec(self) -> ABICodec:
        # use codec set on the Web3 instance
        return self.w3.codec

    def attach_methods(
        self,
        methods: Dict[str, Method[Callable[..., Any]]],
    ) -> None:
        for method_name, method_class in methods.items():
            klass = (
                method_class.__get__(module=self)()
                if method_class.is_property
                else method_class.__get__(module=self)
            )
            setattr(self, method_name, klass)class AsyncGethAdmin(Module):
    """
    https://geth.ethereum.org/docs/interacting-with-geth/rpc/ns-admin
    """

    is_async = True

    _add_peer: Method[Callable[[EnodeURI], Awaitable[bool]]] = Method(
        RPC.admin_addPeer,
        mungers=[default_root_munger],
    )

    async def add_peer(self, node_url: EnodeURI) -> bool:
        return await self._add_peer(node_url)

    _datadir: Method[Callable[[], Awaitable[str]]] = Method(
        RPC.admin_datadir,
        is_property=True,
    )

    async def datadir(self) -> str:
        return await self._datadir()

    _node_info: Method[Callable[[], Awaitable[NodeInfo]]] = Method(
        RPC.admin_nodeInfo,
        is_property=True,
    )

    async def node_info(self) -> NodeInfo:
        return await self._node_info()

    _peers: Method[Callable[[], Awaitable[List[Peer]]]] = Method(
        RPC.admin_peers,
        is_property=True,
    )

    async def peers(self) -> List[Peer]:
        return await self._peers()

    # start_http and stop_http

    _start_http: Method[Callable[[str, int, str, str], Awaitable[bool]]] = Method(
        RPC.admin_startHTTP,
        mungers=[admin_start_params_munger],
    )

    _stop_http: Method[Callable[[], Awaitable[bool]]] = Method(
        RPC.admin_stopHTTP,
        is_property=True,
    )

    async def start_http(
        self,
        host: str = "localhost",
        port: int = 8546,
        cors: str = "",
        apis: str = "eth,net,web3",
    ) -> bool:
        return await self._start_http(host, port, cors, apis)

    async def stop_http(self) -> bool:
        return await self._stop_http()

    # start_ws and stop_ws

    _start_ws: Method[Callable[[str, int, str, str], Awaitable[bool]]] = Method(
        RPC.admin_startWS,
        mungers=[admin_start_params_munger],
    )

    _stop_ws: Method[Callable[[], Awaitable[bool]]] = Method(
        RPC.admin_stopWS,
        is_property=True,
    )

    async def start_ws(
        self,
        host: str = "localhost",
        port: int = 8546,
        cors: str = "",
        apis: str = "eth,net,web3",
    ) -> bool:
        return await self._start_ws(host, port, cors, apis)

    async def stop_ws(self) -> bool:
        return await self._stop_ws()


class Method(Generic[TFunc]):
    """
    Method object for web3 module methods

    Calls to the Method go through these steps:

    1. input munging - includes normalization, parameter checking, early parameter
    formatting. Any processing on the input parameters that need to happen before
    json_rpc method string selection occurs.

            A note about mungers: The first (root) munger should reflect the desired
        api function arguments. In other words, if the api function wants to
        behave as: `get_balance(account, block_identifier=None)`, the root munger
        should accept these same arguments, with the addition of the module as
        the first argument e.g.:

        ```
        def get_balance_root_munger(module, account, block_identifier=None):
            if block_identifier is None:
                block_identifier = DEFAULT_BLOCK
            return module, [account, block_identifier]
        ```

        all mungers should return an argument list.

        if no munger is provided, a default munger expecting no method arguments
        will be used.

    2. method selection - The json_rpc_method argument can be method string or a
    function that returns a method string. If a callable is provided the processed
    method inputs are passed to the method selection function, and the returned
    method string is used.

    3. request and response formatters are set - formatters are retrieved
    using the json rpc method string.

    4. After the parameter processing from steps 1-3 the request is made using
    the calling function returned by the module attribute ``retrieve_caller_fn``
    and the response formatters are applied to the output.
    """

    def __init__(
        self,
        json_rpc_method: Optional[RPCEndpoint] = None,
        mungers: Optional[Sequence[Munger]] = None,
        request_formatters: Optional[Callable[..., TReturn]] = None,
        result_formatters: Optional[Callable[..., TReturn]] = None,
        null_result_formatters: Optional[Callable[..., TReturn]] = None,
        method_choice_depends_on_args: Optional[Callable[..., RPCEndpoint]] = None,
        is_property: bool = False,
    ):
        self.json_rpc_method = json_rpc_method
        self.mungers = _set_mungers(mungers, is_property)
        self.request_formatters = request_formatters or get_request_formatters
        self.result_formatters = result_formatters or get_result_formatters
        self.null_result_formatters = (
            null_result_formatters or get_null_result_formatters
        )
        self.method_choice_depends_on_args = method_choice_depends_on_args
        self.is_property = is_property

    def __get__(
        self,
        module: Optional["Module"] = None,
        _type: Optional[Type["Module"]] = None,
    ) -> TFunc:
        self._module = module
        if module is None:
            raise Web3TypeError(
                "Direct calls to methods are not supported. "
                "Methods must be called from a module instance, "
                "usually attached to a web3 instance."
            )

        provider = module.w3.provider
        if hasattr(provider, "_is_batching") and provider._is_batching:
            if self.json_rpc_method in RPC_METHODS_UNSUPPORTED_DURING_BATCH:
                raise MethodNotSupported(
                    f"Method `{self.json_rpc_method}` is not supported within a batch "
                    "request."
                )
            return module.retrieve_request_information(self)
        else:
            return module.retrieve_caller_fn(self)

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        return self.__get__(self._module)(*args, **kwargs)

    @property
    def method_selector_fn(
        self,
    ) -> Callable[..., Union[RPCEndpoint, Callable[..., RPCEndpoint]]]:
        """Gets the method selector from the config."""
        if callable(self.json_rpc_method):
            return self.json_rpc_method
        elif isinstance(self.json_rpc_method, (str,)):
            return lambda *_: self.json_rpc_method
        raise Web3ValueError(
            "``json_rpc_method`` config invalid.  May be a string or function"
        )

    def input_munger(self, module: "Module", args: Any, kwargs: Any) -> List[Any]:
        # This function takes the input parameters and munges them.
        # See the test_process_params test in ``tests/core/method-class/test_method.py``
        # for an example with multiple mungers.
        return functools.reduce(
            lambda args, munger: munger(module, *args, **kwargs), self.mungers, args
        )

    def process_params(
        self, module: "Module", *args: Any, **kwargs: Any
    ) -> Tuple[
        Tuple[Union[RPCEndpoint, Callable[..., RPCEndpoint]], Tuple[Any, ...]],
        Tuple[
            Union[TReturn, Dict[str, Callable[..., Any]]],
            Callable[..., Any],
            Union[TReturn, Callable[..., Any]],
        ],
    ]:
        params = self.input_munger(module, args, kwargs)

        if self.method_choice_depends_on_args:
            # If the method choice depends on the args that get passed in,
            # the first parameter determines which method needs to be called
            self.json_rpc_method = self.method_choice_depends_on_args(value=params[0])

            pending_or_latest_filter_methods = [
                RPC.eth_newPendingTransactionFilter,
                RPC.eth_newBlockFilter,
            ]
            if self.json_rpc_method in pending_or_latest_filter_methods:
                # For pending or latest filter methods, use params to determine
                # which method to call, but don't pass them through with the request
                params = []

        method = self.method_selector_fn()
        response_formatters = (
            self.result_formatters(method, module),
            get_error_formatters(method),
            self.null_result_formatters(method),
        )
        request = (
            method,
            _apply_request_formatters(params, self.request_formatters(method)),
        )
        return request, response_formatters


def _apply_request_formatters(
    params: Any, request_formatters: Dict[RPCEndpoint, Callable[..., TReturn]]
) -> Tuple[Any, ...]:
    if request_formatters:
        formatted_params = pipe(params, request_formatters)
        return formatted_params
    return params


def _apply_request_formatters(
    params: Any, request_formatters: Dict[RPCEndpoint, Callable[..., TReturn]]
) -> Tuple[Any, ...]:
    if request_formatters:
        formatted_params = pipe(params, request_formatters)
        return formatted_params
    return params


class GethAdmin(Module):
    """
    https://geth.ethereum.org/docs/interacting-with-geth/rpc/ns-admin
    """

    is_async = False

    add_peer: Method[Callable[[EnodeURI], bool]] = Method(
        RPC.admin_addPeer,
        mungers=[default_root_munger],
    )

    datadir: Method[Callable[[], str]] = Method(
        RPC.admin_datadir,
        is_property=True,
    )

    node_info: Method[Callable[[], NodeInfo]] = Method(
        RPC.admin_nodeInfo,
        is_property=True,
    )

    peers: Method[Callable[[], List[Peer]]] = Method(
        RPC.admin_peers,
        is_property=True,
    )

    start_http: Method[ServerConnection] = Method(
        RPC.admin_startHTTP,
        mungers=[admin_start_params_munger],
    )

    start_ws: Method[ServerConnection] = Method(
        RPC.admin_startWS,
        mungers=[admin_start_params_munger],
    )

    stop_http: Method[Callable[[], bool]] = Method(
        RPC.admin_stopHTTP,
        is_property=True,
    )

    stop_ws: Method[Callable[[], bool]] = Method(
        RPC.admin_stopWS,
        is_property=True,
    )


from web3._utils.filters import (
    AsyncLogFilter,
    LogFilter,
    _UseExistingFilter,
)
from web3.method import (
    Method,
)
