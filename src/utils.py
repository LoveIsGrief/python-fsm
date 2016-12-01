import pygraphviz as pgv

from fsm import State, MealyMachine


def get_graph(fsm, title=None):
    """Generate a DOT graph with pygraphviz."""

    if title is None:
        title = fsm.name
    elif title is False:
        title = ''

    fsm_graph = pgv.AGraph(title=title, **fsm.DOT_ATTRS)
    fsm_graph.node_attr.update(State.DOT_ATTRS)

    for state in [fsm.init_state] + fsm.states:
        shape = State.DOT_ATTRS['shape']
        if hasattr(fsm, 'accepting_states'):
            if id(state) in [id(s) for s in fsm.accepting_states]:
                shape = state.DOT_ACCEPTING
        fsm_graph.add_node(n=state.name, shape=shape)

    fsm_graph.add_node('null', shape='plaintext', label=' ')
    fsm_graph.add_edge('null', fsm.init_state.name)

    for src, input_value, dst in fsm.all_transitions:
        label = str(input_value)
        if isinstance(fsm, MealyMachine):
            label += ' / %s' % dict(src.output_values).get(input_value)
        fsm_graph.add_edge(src.name, dst.name, label=label)
    for state in fsm.states:
        if state.default_transition is not None:
            fsm_graph.add_edge(state.name, state.default_transition.name,
                               label='else')
    return fsm_graph
