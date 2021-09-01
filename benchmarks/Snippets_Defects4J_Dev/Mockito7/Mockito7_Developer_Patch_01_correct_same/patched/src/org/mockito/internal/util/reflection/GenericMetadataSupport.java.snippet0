private void readTypeVariables() {
            for (Type type : typeVariable.getBounds()) {
                registerTypeVariablesOn(type);
            }
            registerTypeParametersOn(new TypeVariable[] { typeVariable });
            registerTypeVariablesOn(getActualTypeArgumentFor(typeVariable));
        }