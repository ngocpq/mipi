@SuppressWarnings("deprecation")
    public void process(Class<?> context, Object testClass) {
        Field[] fields = context.getDeclaredFields();
        for (Field field : fields) {
            if (field.isAnnotationPresent(Spy.class)) {
                assertNoAnnotations(Spy.class, field, Mock.class, org.mockito.MockitoAnnotations.Mock.class, Captor.class);
                boolean wasAccessible = field.isAccessible();
                field.setAccessible(true);
                try {
                    Object instance = field.get(testClass);
                    if (instance == null) {
                        throw new MockitoException("Cannot create a @Spy for '" + field.getName() + "' field because the *instance* is missing\n" +
                        		  "The instance must be created *before* initMocks();\n" +
                                  "Example of correct usage of @Spy:\n" +
                            	  "   @Spy List mock = new LinkedList();\n" +
                            	  "   //also, don't forget about MockitoAnnotations.initMocks();");

                    }
                    if (new MockUtil().isMock(instance)) { 
                        // instance has been spied earlier
                        Mockito.reset(instance);
                    } else {
                        field.set(testClass, Mockito.spy(instance));
                    }
                } catch (IllegalAccessException e) {
                    throw new MockitoException("Problems initiating spied field " + field.getName(), e);
                } finally {
                    field.setAccessible(wasAccessible);
                }
            }
        }
    }