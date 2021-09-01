public <T> void resetMock(T mock) {
        MockHandlerInterface<T> oldMockHandler = getMockHandler(mock);
        MethodInterceptorFilter newFilter = newMethodInterceptorFilter(oldMockHandler.getMockSettings());
        ((Factory) mock).setCallback(0, newFilter);
    }