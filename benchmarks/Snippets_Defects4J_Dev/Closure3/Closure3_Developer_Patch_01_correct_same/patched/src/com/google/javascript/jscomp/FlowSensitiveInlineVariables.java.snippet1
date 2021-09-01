@Override
  public void enterScope(NodeTraversal t) {

    if (t.inGlobalScope()) {
      return; // Don't even brother. All global variables are likely escaped.
    }

    if (LiveVariablesAnalysis.MAX_VARIABLES_TO_ANALYZE <
        t.getScope().getVarCount()) {
      return;
    }

    // Compute the forward reaching definition.
    ControlFlowAnalysis cfa = new ControlFlowAnalysis(compiler, false, true);
    // Process the body of the function.
    Preconditions.checkState(t.getScopeRoot().isFunction());
    cfa.process(null, t.getScopeRoot().getLastChild());
    cfg = cfa.getCfg();
    reachingDef = new MustBeReachingVariableDef(cfg, t.getScope(), compiler);
    reachingDef.analyze();
    candidates = Lists.newLinkedList();

    // Using the forward reaching definition search to find all the inline
    // candidates
    new NodeTraversal(compiler, new GatherCandiates()).traverse(
        t.getScopeRoot().getLastChild());

    // Compute the backward reaching use. The CFG can be reused.
    reachingUses = new MaybeReachingVariableUse(cfg, t.getScope(), compiler);
    reachingUses.analyze();
    for (Candidate c : candidates) {
      if (c.canInline(t.getScope())) {
        c.inlineVariable();

        // If definition c has dependencies, then inlining it may have
        // introduced new dependencies for our other inlining candidates.
        //
        // MustBeReachingVariableDef uses this dependency graph in its
        // analysis, so some of these candidates may no longer be valid.
        // We keep track of when the variable dependency graph changed
        // so that we can back off appropriately.
        if (!c.defMetadata.depends.isEmpty()) {
          inlinedNewDependencies.add(t.getScope().getVar(c.varName));
        }
      }
    }
  }