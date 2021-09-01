private Node computeFollowing(Node n) {
    Node next = ControlFlowAnalysis.computeFollowNode(n);
    while (next != null && next.getType() == Token.BLOCK) {
      if (next.hasChildren()) {
        next = next.getFirstChild();
      } else {
        next = computeFollowing(next);
      }
    }
    return next;
  }