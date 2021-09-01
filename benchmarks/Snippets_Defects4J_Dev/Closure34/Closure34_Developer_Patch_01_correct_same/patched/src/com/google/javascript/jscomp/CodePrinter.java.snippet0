@Override
    void appendOp(String op, boolean binOp) {
      if (binOp) {
        if (getLastChar() != ' ' && op.charAt(0) != ',') {
          append(" ");
        }
        append(op);
        append(" ");
      } else {
        append(op);
      }
    }