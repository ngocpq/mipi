public <T> T mock(Class<T> classToMock, MockSettings mockSettings, boolean shouldResetOngoingStubbing) {
        mockingProgress.validateState();
        if (shouldResetOngoingStubbing) {
            mockingProgress.resetOngoingStubbing();
        }
        return mockUtil.createMock(classToMock, (MockSettingsImpl) mockSettings);
    }