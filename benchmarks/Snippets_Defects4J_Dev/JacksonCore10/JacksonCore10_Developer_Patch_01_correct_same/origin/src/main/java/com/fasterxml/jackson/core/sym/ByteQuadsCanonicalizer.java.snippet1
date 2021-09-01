public int calcHash(int q1)
    {
        int hash = q1 ^ _seed;
        /* 29-Mar-2015, tatu: Earlier used 15 + 9 right shifts, which worked ok
         *    except for one specific problem case: numbers. So needed to make sure
         *    that all 4 least-significant bits participate in hash. Couple of ways
         *    to work it out, but this is the simplest, fast and seems to do ok.
         */
        hash += (hash >>> 16); // to xor hi- and low- 16-bits
        hash ^= (hash >>> 12);
        return hash;
    }