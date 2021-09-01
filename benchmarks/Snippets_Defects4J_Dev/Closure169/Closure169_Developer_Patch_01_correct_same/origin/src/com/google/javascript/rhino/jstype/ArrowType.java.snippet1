boolean checkArrowEquivalenceHelper(
      ArrowType that, boolean tolerateUnknowns) {
    // Please keep this method in sync with the hashCode() method below.
    if (!returnType.checkEquivalenceHelper(that.returnType, tolerateUnknowns)) {
      return false;
    }
    return hasEqualParameters(that, tolerateUnknowns);
  }