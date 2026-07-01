package org.evomaster.client.java.controller.contentMatchers;

import org.hamcrest.BaseMatcher;
import org.hamcrest.Description;
import org.hamcrest.Matcher;

/**
 * Faithful re-implementation of EvoMaster's NumberMatcher.numberMatches, used so that
 * EvoMaster's generated regression assertions compile and run inside our common harness
 * WITHOUT pulling EvoMaster's shaded fat-jar onto the classpath. Semantics preserved:
 * a JSON numeric value matches iff it is numerically equal to the recorded expected value
 * (NaN-aware, with a tiny relative epsilon for double formatting). See experiment/evomaster/README.md.
 */
public class NumberMatcher {

    public static Matcher<Object> numberMatches(double expected) { return make(expected); }
    public static Matcher<Object> numberMatches(long expected) { return make((double) expected); }
    public static Matcher<Object> numberMatches(int expected) { return make((double) expected); }

    private static Matcher<Object> make(final double expected) {
        return new BaseMatcher<Object>() {
            @Override public boolean matches(Object actual) {
                if (actual == null) return false;
                double a;
                try {
                    a = (actual instanceof Number) ? ((Number) actual).doubleValue()
                                                   : Double.parseDouble(actual.toString());
                } catch (NumberFormatException e) {
                    return false;
                }
                if (Double.isNaN(expected)) return Double.isNaN(a);
                if (Double.isInfinite(expected)) return a == expected;
                if (a == expected) return true;
                return Math.abs(a - expected) <= 1e-9 * Math.max(1.0, Math.abs(expected));
            }
            @Override public void describeTo(Description d) { d.appendText("a number equal to " + expected); }
        };
    }
}
