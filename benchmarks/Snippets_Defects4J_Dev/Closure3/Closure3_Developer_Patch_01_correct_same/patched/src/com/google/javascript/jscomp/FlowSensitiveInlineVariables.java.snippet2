@Override
              public boolean apply(Node input) {
                switch (input.getType()) {
                  case Token.GETELEM:
                  case Token.GETPROP:
                  case Token.ARRAYLIT:
                  case Token.OBJECTLIT:
                  case Token.REGEXP:
                  case Token.NEW:
                    return true;
                  case Token.NAME:
                    Var var = scope.getOwnSlot(input.getString());
                    if (var != null
                        && var.getParentNode().isCatch()) {
                      return true;
                    }
                }
                return false;
              }