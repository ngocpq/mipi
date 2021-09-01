public int read(byte[] b, final int off, final int len) throws IOException {
        int toRead = len;
        final int ret = this.input.read(b, off, toRead);
        offset += (ret > 0 ? ret : 0);
        return ret;
    }