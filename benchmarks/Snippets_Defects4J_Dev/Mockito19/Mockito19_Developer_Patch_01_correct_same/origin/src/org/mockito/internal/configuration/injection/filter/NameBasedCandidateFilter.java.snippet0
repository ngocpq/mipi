public OngoingInjecter filterCandidate(Collection<Object> mocks,
			Field field, Object fieldInstance) {
		List<Object> mockNameMatches = new ArrayList<Object>();
		if (mocks.size() > 1) {
			for (Object mock : mocks) {
				if (field.getName().equals(mockUtil.getMockName(mock).toString())) {
					mockNameMatches.add(mock);
				}
			}
			return next.filterCandidate(mockNameMatches, field,
					fieldInstance);
			/*
			 * In this case we have to check whether we have conflicting naming
			 * fields. E.g. 2 fields of the same type, but we have to make sure
			 * we match on the correct name.
			 * 
			 * Therefore we have to go through all other fields and make sure
			 * whenever we find a field that does match its name with the mock
			 * name, we should take that field instead.
			 */
		}
		return next.filterCandidate(mocks, field, fieldInstance);
	}