/**
     * Add an option to the command line.  The values of 
     * the option are stored.
     *
     * @param opt the processed option
     */
void addOption(Option opt){
	hashcodeMap.put(new Integer(opt.hashCode()), opt);
	String key = opt.getKey();
	if (key == null){
		key = opt.getLongOpt();
	} else {
		names.put(opt.getLongOpt(), key);
	}
	options.put(key, opt);
}
