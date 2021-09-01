@Override
    public void applyAlias() {
      String typeName = typeReference.getString();
      String aliasExpanded =
          Preconditions.checkNotNull(aliasDefinition.getQualifiedName());
      Preconditions.checkState(typeName.startsWith(aliasName));
      typeReference.setString(typeName.replaceFirst(aliasName, aliasExpanded));
    }