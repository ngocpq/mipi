public void processValues(final WriteableCommandLine commandLine,
                              final ListIterator arguments,
                              final Option option)
        throws OptionException {
        // count of arguments processed for this option.
        int argumentCount = 0;

        while (arguments.hasNext() && (argumentCount < maximum)) {
            final String allValuesQuoted = (String) arguments.next();
            final String allValues = stripBoundaryQuotes(allValuesQuoted);

            // should we ignore things that look like options?
            if (allValuesQuoted.equals(consumeRemaining)) {
                while (arguments.hasNext() && (argumentCount < maximum)) {
                    ++argumentCount;
                    commandLine.addValue(option, arguments.next());
                }
            }
            // does it look like an option?
            else if (commandLine.looksLikeOption(allValuesQuoted)) {
                arguments.previous();

                break;
            }
            // should we split the string up?
            else if (subsequentSplit) {
                final StringTokenizer values =
                    new StringTokenizer(allValues, String.valueOf(subsequentSeparator));

                arguments.remove();

                while (values.hasMoreTokens() && (argumentCount < maximum)) {
                    ++argumentCount;

                    final String token = values.nextToken();
                    commandLine.addValue(option, token);
                    arguments.add(token);
                }

                if (values.hasMoreTokens()) {
                    throw new OptionException(option, ResourceConstants.ARGUMENT_UNEXPECTED_VALUE,
                                              values.nextToken());
                }
            }
            // it must be a value as it is
            else {
                ++argumentCount;
                commandLine.addValue(option, allValues);
            }
        }
    }