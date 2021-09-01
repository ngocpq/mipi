protected String getLanguage() {
        Object n = node;
        while (n != null) {
            if (n instanceof Element) {
                Element e = (Element) n;
                String attr =
                    e.getAttributeValue("lang", Namespace.XML_NAMESPACE);
                if (attr != null && !attr.equals("")) {
                    return attr;
                }
            }
            n = nodeParent(n);
        }
        return null;
    }