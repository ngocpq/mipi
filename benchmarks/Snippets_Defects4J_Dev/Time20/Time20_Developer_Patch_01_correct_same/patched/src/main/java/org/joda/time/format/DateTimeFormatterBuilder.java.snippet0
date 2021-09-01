public int parseInto(DateTimeParserBucket bucket, String text, int position) {
            String str = text.substring(position);
            String best = null;
            for (String id : ALL_IDS) {
                if (str.startsWith(id)) {
                	if (best == null || id.length() > best.length()) {
                		best = id;
                	}
                }
            }
            if (best != null) {
                bucket.setZone(DateTimeZone.forID(best));
                return position + best.length();
            }
            return ~position;
        }