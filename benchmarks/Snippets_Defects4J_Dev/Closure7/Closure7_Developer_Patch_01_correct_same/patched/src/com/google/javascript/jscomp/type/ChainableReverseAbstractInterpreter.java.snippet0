@Override
    public JSType caseObjectType(ObjectType type) {
      if (value.equals("function")) {
        JSType ctorType = getNativeType(U2U_CONSTRUCTOR_TYPE);
        if (resultEqualsValue) {
          // Objects are restricted to "Function", subtypes are left
          return ctorType.getGreatestSubtype(type);
        } else {
          // Only filter out subtypes of "function"
          return type.isSubtype(ctorType) ? null : type;
        }
      }
      return matchesExpectation("object") ? type : null;
    }