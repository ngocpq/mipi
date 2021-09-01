private int _skipWSOrEnd() throws IOException
    {
        final int[] codes = _icWS;
        while ((_inputPtr < _inputEnd) || loadMore()) {
            final int i = _inputBuffer[_inputPtr++] & 0xFF;
            switch (codes[i]) {
            case 0: // done!
                return i;
            case 1: // skip
                continue;
            case 2: // 2-byte UTF
                _skipUtf8_2(i);
                break;
            case 3: // 3-byte UTF
                _skipUtf8_3(i);
                break;
            case 4: // 4-byte UTF
                _skipUtf8_4(i);
                break;
            case INT_LF:
                ++_currInputRow;
                _currInputRowStart = _inputPtr;
                break;
            case INT_CR:
                _skipCR();
                break;
            case '/':
                _skipComment();
                break;
            case '#':
                if (!_skipYAMLComment()) {
                    return i;
                }
                break;
            default: // e.g. -1
                if (i < 32) {
                    _throwInvalidSpace(i);
                }
                _reportInvalidChar(i);
            }
        }
        // We ran out of input...
        _handleEOF();
        return -1;
    }