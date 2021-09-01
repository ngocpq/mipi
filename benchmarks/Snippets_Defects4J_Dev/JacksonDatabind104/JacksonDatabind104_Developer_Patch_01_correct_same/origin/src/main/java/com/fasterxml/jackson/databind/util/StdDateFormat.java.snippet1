private static void pad4(StringBuffer buffer, int value) {
        int h = value / 100;
        if (h == 0) {
            buffer.append('0').append('0');
        } else {
                pad2(buffer, h);
            value -= (100 * h);
        }
        pad2(buffer, value);
    }