from argparse import Namespace

ARGS = Namespace(
    epic=False,
    v=2,
    command="a",
    rpc="infura-mainnet",
    rpctls=False,
    infura_id=None,
    solc_json=None,
    solc_args=None,
    solv=None,
    code=None,
    codefile=None,
    address=None,
    bin_runtime=False,
    outform="text",
    solidity_files=[],
    graph=None,
    statespace_json=None,
    modules=None,
    max_depth=128,
    call_depth_limit=3,
    strategy="bfs",
    transaction_sequences=None,
    beam_search=None,
    loop_bound=3,
    transaction_count=2,
    execution_timeout=20,
    solver_timeout=25000,
    create_timeout=30,
    parallel_solving=False,
    solver_log=None,
    no_onchain_data=False,
    pruning_factor=None,
    unconstrained_storage=False,
    phrack=False,
    enable_physics=False,
    query_signature=False,
    disable_iprof=False,
    disable_dependency_pruning=False,
    disable_coverage_strategy=False,
    disable_mutation_pruner=False,
    enable_state_merging=False,
    enable_summaries=False,
    custom_modules_directory=None,
    attacker_address=None,
    creator_address=None,
)
