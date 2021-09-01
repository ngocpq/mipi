public Object callRealMethod() throws Throwable {
        if (this.getMethod().getDeclaringClass().isInterface()) {
            new Reporter().cannotCallRealMethodOnInterface();
        }
        return realMethod.invoke(mock, rawArguments);
    }