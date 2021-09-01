private static <T> T withParams(Class<T> cls, Object... params) {
        try {
            //this is kind of overengineered because we don't need to support more params
            //however, I know we will be needing it :)
            for (Constructor<?> constructor : cls.getDeclaredConstructors()) {
                Class<?>[] types = constructor.getParameterTypes();
                if (paramsMatch(types, params)) {
                    return (T) constructor.newInstance(params);
                }
            }
        } catch (Exception e) {
            throw paramsException(cls, e);
        }
        throw paramsException(cls, null);
    }