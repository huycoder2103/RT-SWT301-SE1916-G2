package org.evomaster.client.java.controller.contentMatchers;

/**
 * Shim so EvoMaster's `import static ...StringMatcher.*` resolves in our harness.
 * The generated suites import this class but do not call any of its methods
 * (verified: only numberMatches / resolveLocation / isValidURIorEmpty are used),
 * so an empty class is sufficient and behaviour-neutral. See experiment/evomaster/README.md.
 */
public class StringMatcher {
}
