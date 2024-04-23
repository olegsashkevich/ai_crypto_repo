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


from eth_utils.toolz import (
    assoc,
)

