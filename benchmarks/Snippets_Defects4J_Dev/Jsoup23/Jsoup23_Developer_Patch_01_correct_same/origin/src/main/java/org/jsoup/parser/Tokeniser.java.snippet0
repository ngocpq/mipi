Character consumeCharacterReference(Character additionalAllowedCharacter, boolean inAttribute) {
        if (reader.isEmpty())
            return null;
        if (additionalAllowedCharacter != null && additionalAllowedCharacter == reader.current())
            return null;
        if (reader.matchesAny('\t', '\n', '\f', ' ', '<', '&'))
            return null;

        reader.mark();
        if (reader.matchConsume("#")) { // numbered
            boolean isHexMode = reader.matchConsumeIgnoreCase("X");
            String numRef = isHexMode ? reader.consumeHexSequence() : reader.consumeDigitSequence();
            if (numRef.length() == 0) { // didn't match anything
                characterReferenceError("numeric reference with no numerals");
                reader.rewindToMark();
                return null;
            }
            if (!reader.matchConsume(";"))
                characterReferenceError("missing semicolon"); // missing semi
            int charval = -1;
            try {
                int base = isHexMode ? 16 : 10;
                charval = Integer.valueOf(numRef, base);
            } catch (NumberFormatException e) {
            } // skip
            if (charval == -1 || (charval >= 0xD800 && charval <= 0xDFFF) || charval > 0x10FFFF) {
                characterReferenceError("character outside of valid range");
                return replacementChar;
            } else {
                // todo: implement number replacement table
                // todo: check for extra illegal unicode points as parse errors
                return (char) charval;
            }
        } else { // named
            // get as many letters as possible, and look for matching entities. unconsume backwards till a match is found
            String nameRef = reader.consumeLetterSequence();
            String origNameRef = new String(nameRef); // for error reporting. nameRef gets chomped looking for matches
            boolean looksLegit = reader.matches(';');
            boolean found = false;
            while (nameRef.length() > 0 && !found) {
                if (Entities.isNamedEntity(nameRef))
                    found = true;
                else {
                    nameRef = nameRef.substring(0, nameRef.length()-1);
                    reader.unconsume();
                }
            }
            if (!found) {
                if (looksLegit) // named with semicolon
                    characterReferenceError(String.format("invalid named referenece '%s'", origNameRef));
                reader.rewindToMark();
                return null;
            }
            if (inAttribute && (reader.matchesLetter() || reader.matchesDigit() || reader.matchesAny('=', '-', '_'))) {
                // don't want that to match
                reader.rewindToMark();
                return null;
            }
            if (!reader.matchConsume(";"))
                characterReferenceError("missing semicolon"); // missing semi
            return Entities.getCharacterByName(nameRef);
        }
    }