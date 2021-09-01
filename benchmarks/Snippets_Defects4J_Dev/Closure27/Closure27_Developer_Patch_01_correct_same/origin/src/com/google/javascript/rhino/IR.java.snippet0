public static Node tryFinally(Node tryBody, Node finallyBody) {
    Preconditions.checkState(tryBody.isLabelName());
    Preconditions.checkState(finallyBody.isLabelName());
    Node catchBody = block().copyInformationFrom(tryBody);
    return new Node(Token.TRY, tryBody, catchBody, finallyBody);
  }