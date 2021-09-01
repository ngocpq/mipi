private void processFlagFile(PrintStream err)
            throws CmdLineException, IOException {
    List<String> argsInFile = Lists.newArrayList();
    File flagFileInput = new File(flags.flag_file);
    StringTokenizer tokenizer = new StringTokenizer(
        Files.toString(flagFileInput, Charset.defaultCharset()));

    while (tokenizer.hasMoreTokens()) {
        argsInFile.add(tokenizer.nextToken());
    }

    flags.flag_file = "";
    List<String> processedFileArgs
        = processArgs(argsInFile.toArray(new String[] {}));
    CmdLineParser parserFileArgs = new CmdLineParser(flags);
    parserFileArgs.parseArgument(processedFileArgs.toArray(new String[] {}));

    // Currently we are not supporting this (prevent direct/indirect loops)
    if (!flags.flag_file.equals("")) {
      err.println("ERROR - Arguments in the file cannot contain "
          + "--flagfile option.");
      isConfigValid = false;
    }
  }