package org.evomaster.client.java.controller;

/**
 * Shim marker type so EvoMaster's `import org.evomaster.client.java.controller.SutHandler`
 * resolves in our harness. It is a white-box lifecycle handle that black-box generated suites
 * import but never use, so an empty interface is behaviour-neutral.
 */
public interface SutHandler {
}
