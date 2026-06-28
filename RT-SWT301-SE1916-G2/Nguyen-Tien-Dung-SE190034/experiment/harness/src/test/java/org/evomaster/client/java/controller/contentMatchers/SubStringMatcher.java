package org.evomaster.client.java.controller.contentMatchers;

/**
 * Shim so EvoMaster's `import static ...SubStringMatcher.*` resolves in our harness.
 * Imported by the generated suites but no method is called (only numberMatches /
 * resolveLocation / isValidURIorEmpty are used), so an empty class is behaviour-neutral.
 */
public class SubStringMatcher {
}
