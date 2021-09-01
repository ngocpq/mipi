public long add(long instant, long value) {
            if (instant >= iCutover) {
                instant = iGregorianField.add(instant, value);
                if (instant < iCutover) {
                    // Only adjust if gap fully crossed.
                    if (instant + iGapDuration < iCutover) {
                        if (iConvertByWeekyear) {
                            int wyear = iGregorianChronology.weekyear().get(instant);
                            if (wyear <= 0) {
                                instant = iGregorianChronology.weekyear().add(instant, -1);
                            }
                        } else {
                            int year = iGregorianChronology.year().get(instant);
                            if (year <= 0) {
                                instant = iGregorianChronology.year().add(instant, -1);
                            }
                        }
                        instant = gregorianToJulian(instant);
                    }
                }
            } else {
                instant = iJulianField.add(instant, value);
                if (instant >= iCutover) {
                    // Only adjust if gap fully crossed.
                    if (instant - iGapDuration >= iCutover) {
                        // no special handling for year zero as cutover always after year zero
                        instant = julianToGregorian(instant);
                    }
                }
            }
            return instant;
        }