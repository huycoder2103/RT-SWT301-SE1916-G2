package org.evomaster.test.utils;

import java.net.URI;

/**
 * Faithful re-implementation of the two EvoMaster EMTestUtils helpers actually used by the
 * generated black-box suites: resolveLocation(...) and isValidURIorEmpty(...). Lets EvoMaster's
 * tests compile/run in our harness without its fat-jar. See experiment/evomaster/README.md.
 */
public class EMTestUtils {

    /** Returns the actual Location header if present/usable, otherwise the recorded fallback URL. */
    public static String resolveLocation(String location, String expectedTemplate) {
        if (location == null || location.trim().isEmpty()) return expectedTemplate;
        location = location.trim();
        if (location.startsWith("http://") || location.startsWith("https://")) return location;
        // relative path: graft onto the scheme+authority of the fallback
        try {
            URI t = URI.create(expectedTemplate);
            String base = t.getScheme() + "://" + t.getAuthority();
            return base + (location.startsWith("/") ? location : "/" + location);
        } catch (Exception e) {
            return expectedTemplate;
        }
    }

    /** True if the string is empty/null or a syntactically valid URI (EvoMaster's lenient check). */
    public static boolean isValidURIorEmpty(String location) {
        if (location == null || location.trim().isEmpty()) return true;
        try { URI.create(location.trim()); return true; } catch (Exception e) { return false; }
    }
}
