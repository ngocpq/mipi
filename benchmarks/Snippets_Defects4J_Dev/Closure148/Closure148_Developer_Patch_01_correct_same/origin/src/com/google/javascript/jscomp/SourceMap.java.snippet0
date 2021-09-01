private int findLastLine() {
    int maxLine = 0;
    for (Mapping mapping : mappings) {
      int endPositionLine = mapping.endPosition.getLineNumber();
      maxLine = Math.max(maxLine, endPositionLine);
    }
    return maxLine + prefixPosition.getLineNumber();
  }