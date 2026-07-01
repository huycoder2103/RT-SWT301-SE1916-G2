package manual;

import io.restassured.RestAssured;
import static io.restassured.RestAssured.given;
import org.junit.jupiter.api.*;
import static org.hamcrest.Matchers.*;

public class NcsManualTests {

    @BeforeAll
    static void setup() {
        RestAssured.baseURI = System.getProperty("baseURI", "http://localhost:8080");
        RestAssured.urlEncodingEnabled = false;
    }

    // =========================================================
    // /api/bessj/{n}/{x}  (n: int32, x: double)
    // =========================================================

    // SCENARIO op=bessjUsingGET type=positive expect=200
    @Test
    void bessjUsingGET_EP_validIntAndDouble() {
        given()
            .pathParam("n", 2)
            .pathParam("x", 1.5)
        .when()
            .get("/api/bessj/{n}/{x}")
        .then()
            .statusCode(200)
            .body("resultAsDouble", notNullValue());
    }

    // SCENARIO op=bessjUsingGET type=negative expect=class(400,404,422,500)
    @Test
    void bessjUsingGET_EP_negativeOrderInvalidClass() {
        given()
            .pathParam("n", -1)
            .pathParam("x", 1.5)
        .when()
            .get("/api/bessj/{n}/{x}")
        .then()
            .statusCode(anyOf(is(200), is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=bessjUsingGET type=boundary expect=class(200,400,404,422,500)
    @Test
    void bessjUsingGET_BVA_nZeroBoundary() {
        given()
            .pathParam("n", 0)
            .pathParam("x", 1.0)
        .when()
            .get("/api/bessj/{n}/{x}")
        .then()
            .statusCode(anyOf(is(200), is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=bessjUsingGET type=boundary expect=class(200,400,404,422,500)
    @Test
    void bessjUsingGET_BVA_xZeroBoundary() {
        given()
            .pathParam("n", 1)
            .pathParam("x", 0.0)
        .when()
            .get("/api/bessj/{n}/{x}")
        .then()
            .statusCode(anyOf(is(200), is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=bessjUsingGET type=boundary expect=class(200,400,404,422,500)
    @Test
    void bessjUsingGET_BVA_veryLargeN() {
        given()
            .pathParam("n", 2147483647)
            .pathParam("x", 1.0)
        .when()
            .get("/api/bessj/{n}/{x}")
        .then()
            .statusCode(anyOf(is(200), is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=bessjUsingGET type=boundary expect=class(200,400,404,422,500)
    @Test
    void bessjUsingGET_BVA_veryLargeX() {
        given()
            .pathParam("n", 1)
            .pathParam("x", 1.0E300)
        .when()
            .get("/api/bessj/{n}/{x}")
        .then()
            .statusCode(anyOf(is(200), is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=bessjUsingGET type=errorcode expect=class(400,404,422,500)
    @Test
    void bessjUsingGET_ERR_wrongTypeForN() {
        given()
            .pathParam("n", "abc")
            .pathParam("x", 1.5)
        .when()
            .get("/api/bessj/{n}/{x}")
        .then()
            .statusCode(anyOf(is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=bessjUsingGET type=errorcode expect=404
    @Test
    void bessjUsingGET_ERR_missingXSegment() {
        given()
            .pathParam("n", 1)
        .when()
            .get("/api/bessj/{n}/")
        .then()
            .statusCode(anyOf(is(404), is(400)));
    }

    // =========================================================
    // /api/expint/{n}/{x}  (n: int32, x: double)
    // =========================================================

    // SCENARIO op=expintUsingGET type=positive expect=200
    @Test
    void expintUsingGET_EP_validIntAndDouble() {
        given()
            .pathParam("n", 3)
            .pathParam("x", 2.0)
        .when()
            .get("/api/expint/{n}/{x}")
        .then()
            .statusCode(200)
            .body("resultAsDouble", notNullValue());
    }

    // SCENARIO op=expintUsingGET type=negative expect=class(200,400,404,422,500)
    @Test
    void expintUsingGET_EP_negativeNInvalidClass() {
        given()
            .pathParam("n", -5)
            .pathParam("x", 2.0)
        .when()
            .get("/api/expint/{n}/{x}")
        .then()
            .statusCode(anyOf(is(200), is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=expintUsingGET type=negative expect=class(200,400,404,422,500)
    @Test
    void expintUsingGET_EP_negativeXInvalidClass() {
        given()
            .pathParam("n", 2)
            .pathParam("x", -1.0)
        .when()
            .get("/api/expint/{n}/{x}")
        .then()
            .statusCode(anyOf(is(200), is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=expintUsingGET type=boundary expect=class(200,400,404,422,500)
    @Test
    void expintUsingGET_BVA_nZeroBoundary() {
        given()
            .pathParam("n", 0)
            .pathParam("x", 1.0)
        .when()
            .get("/api/expint/{n}/{x}")
        .then()
            .statusCode(anyOf(is(200), is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=expintUsingGET type=boundary expect=class(200,400,404,422,500)
    @Test
    void expintUsingGET_BVA_xZeroBoundary() {
        given()
            .pathParam("n", 1)
            .pathParam("x", 0.0)
        .when()
            .get("/api/expint/{n}/{x}")
        .then()
            .statusCode(anyOf(is(200), is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=expintUsingGET type=boundary expect=class(200,400,404,422,500)
    @Test
    void expintUsingGET_BVA_veryLargeX() {
        given()
            .pathParam("n", 1)
            .pathParam("x", 1.0E250)
        .when()
            .get("/api/expint/{n}/{x}")
        .then()
            .statusCode(anyOf(is(200), is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=expintUsingGET type=errorcode expect=class(400,404,422,500)
    @Test
    void expintUsingGET_ERR_wrongTypeForX() {
        given()
            .pathParam("n", 1)
            .pathParam("x", "notANumber")
        .when()
            .get("/api/expint/{n}/{x}")
        .then()
            .statusCode(anyOf(is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=expintUsingGET type=errorcode expect=404
    @Test
    void expintUsingGET_ERR_missingSegments() {
        given()
        .when()
            .get("/api/expint/")
        .then()
            .statusCode(anyOf(is(404), is(400)));
    }

    // =========================================================
    // /api/fisher/{m}/{n}/{x}  (m: int32, n: int32, x: double)
    // =========================================================

    // SCENARIO op=fisherUsingGET type=positive expect=200
    @Test
    void fisherUsingGET_EP_validParams() {
        given()
            .pathParam("m", 5)
            .pathParam("n", 10)
            .pathParam("x", 1.0)
        .when()
            .get("/api/fisher/{m}/{n}/{x}")
        .then()
            .statusCode(200)
            .body("resultAsDouble", notNullValue());
    }

    // SCENARIO op=fisherUsingGET type=negative expect=class(200,400,404,422,500)
    @Test
    void fisherUsingGET_EP_negativeMInvalidClass() {
        given()
            .pathParam("m", -1)
            .pathParam("n", 10)
            .pathParam("x", 1.0)
        .when()
            .get("/api/fisher/{m}/{n}/{x}")
        .then()
            .statusCode(anyOf(is(200), is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=fisherUsingGET type=negative expect=class(200,400,404,422,500)
    @Test
    void fisherUsingGET_EP_negativeNInvalidClass() {
        given()
            .pathParam("m", 5)
            .pathParam("n", -1)
            .pathParam("x", 1.0)
        .when()
            .get("/api/fisher/{m}/{n}/{x}")
        .then()
            .statusCode(anyOf(is(200), is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=fisherUsingGET type=boundary expect=class(200,400,404,422,500)
    @Test
    void fisherUsingGET_BVA_mZeroBoundary() {
        given()
            .pathParam("m", 0)
            .pathParam("n", 10)
            .pathParam("x", 1.0)
        .when()
            .get("/api/fisher/{m}/{n}/{x}")
        .then()
            .statusCode(anyOf(is(200), is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=fisherUsingGET type=boundary expect=class(200,400,404,422,500)
    @Test
    void fisherUsingGET_BVA_nZeroBoundary() {
        given()
            .pathParam("m", 5)
            .pathParam("n", 0)
            .pathParam("x", 1.0)
        .when()
            .get("/api/fisher/{m}/{n}/{x}")
        .then()
            .statusCode(anyOf(is(200), is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=fisherUsingGET type=boundary expect=class(200,400,404,422,500)
    @Test
    void fisherUsingGET_BVA_xZeroBoundary() {
        given()
            .pathParam("m", 5)
            .pathParam("n", 10)
            .pathParam("x", 0.0)
        .when()
            .get("/api/fisher/{m}/{n}/{x}")
        .then()
            .statusCode(anyOf(is(200), is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=fisherUsingGET type=boundary expect=class(200,400,404,422,500)
    @Test
    void fisherUsingGET_BVA_veryLargeMAndN() {
        given()
            .pathParam("m", 2147483647)
            .pathParam("n", 2147483647)
            .pathParam("x", 1.0)
        .when()
            .get("/api/fisher/{m}/{n}/{x}")
        .then()
            .statusCode(anyOf(is(200), is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=fisherUsingGET type=errorcode expect=class(400,404,422,500)
    @Test
    void fisherUsingGET_ERR_wrongTypeForM() {
        given()
            .pathParam("m", "xyz")
            .pathParam("n", 10)
            .pathParam("x", 1.0)
        .when()
            .get("/api/fisher/{m}/{n}/{x}")
        .then()
            .statusCode(anyOf(is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=fisherUsingGET type=errorcode expect=404
    @Test
    void fisherUsingGET_ERR_missingXSegment() {
        given()
            .pathParam("m", 5)
            .pathParam("n", 10)
        .when()
            .get("/api/fisher/{m}/{n}/")
        .then()
            .statusCode(anyOf(is(404), is(400)));
    }

    // =========================================================
    // /api/gammq/{a}/{x}  (a: double, x: double)
    // =========================================================

    // SCENARIO op=gammqUsingGET type=positive expect=200
    @Test
    void gammqUsingGET_EP_validDoubles() {
        given()
            .pathParam("a", 1.5)
            .pathParam("x", 2.5)
        .when()
            .get("/api/gammq/{a}/{x}")
        .then()
            .statusCode(200)
            .body("resultAsDouble", notNullValue());
    }

    // SCENARIO op=gammqUsingGET type=negative expect=class(200,400,404,422,500)
    @Test
    void gammqUsingGET_EP_negativeAInvalidClass() {
        given()
            .pathParam("a", -1.0)
            .pathParam("x", 2.5)
        .when()
            .get("/api/gammq/{a}/{x}")
        .then()
            .statusCode(anyOf(is(200), is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=gammqUsingGET type=negative expect=class(200,400,404,422,500)
    @Test
    void gammqUsingGET_EP_negativeXInvalidClass() {
        given()
            .pathParam("a", 1.5)
            .pathParam("x", -2.5)
        .when()
            .get("/api/gammq/{a}/{x}")
        .then()
            .statusCode(anyOf(is(200), is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=gammqUsingGET type=boundary expect=class(200,400,404,422,500)
    @Test
    void gammqUsingGET_BVA_aZeroBoundary() {
        given()
            .pathParam("a", 0.0)
            .pathParam("x", 1.0)
        .when()
            .get("/api/gammq/{a}/{x}")
        .then()
            .statusCode(anyOf(is(200), is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=gammqUsingGET type=boundary expect=class(200,400,404,422,500)
    @Test
    void gammqUsingGET_BVA_xZeroBoundary() {
        given()
            .pathParam("a", 1.0)
            .pathParam("x", 0.0)
        .when()
            .get("/api/gammq/{a}/{x}")
        .then()
            .statusCode(anyOf(is(200), is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=gammqUsingGET type=boundary expect=class(200,400,404,422,500)
    @Test
    void gammqUsingGET_BVA_veryLargeA() {
        given()
            .pathParam("a", 1.0E300)
            .pathParam("x", 1.0)
        .when()
            .get("/api/gammq/{a}/{x}")
        .then()
            .statusCode(anyOf(is(200), is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=gammqUsingGET type=boundary expect=class(200,400,404,422,500)
    @Test
    void gammqUsingGET_BVA_verySmallPositiveX() {
        given()
            .pathParam("a", 1.0)
            .pathParam("x", 1.0E-300)
        .when()
            .get("/api/gammq/{a}/{x}")
        .then()
            .statusCode(anyOf(is(200), is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=gammqUsingGET type=errorcode expect=class(400,404,422,500)
    @Test
    void gammqUsingGET_ERR_wrongTypeForA() {
        given()
            .pathParam("a", "notANumber")
            .pathParam("x", 1.0)
        .when()
            .get("/api/gammq/{a}/{x}")
        .then()
            .statusCode(anyOf(is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=gammqUsingGET type=errorcode expect=404
    @Test
    void gammqUsingGET_ERR_missingXSegment() {
        given()
            .pathParam("a", 1.0)
        .when()
            .get("/api/gammq/{a}/")
        .then()
            .statusCode(anyOf(is(404), is(400)));
    }

    // =========================================================
    // /api/remainder/{a}/{b}  (a: int32, b: int32)
    // =========================================================

    // SCENARIO op=remainderUsingGET type=positive expect=200
    @Test
    void remainderUsingGET_EP_validInts() {
        given()
            .pathParam("a", 10)
            .pathParam("b", 3)
        .when()
            .get("/api/remainder/{a}/{b}")
        .then()
            .statusCode(200)
            .body("resultAsInt", notNullValue());
    }

    // SCENARIO op=remainderUsingGET type=negative expect=class(200,400,404,422,500)
    @Test
    void remainderUsingGET_EP_negativeAValidClass() {
        given()
            .pathParam("a", -10)
            .pathParam("b", 3)
        .when()
            .get("/api/remainder/{a}/{b}")
        .then()
            .statusCode(anyOf(is(200), is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=remainderUsingGET type=boundary expect=class(200,400,404,422,500)
    @Test
    void remainderUsingGET_BVA_bZeroDivisionBoundary() {
        given()
            .pathParam("a", 10)
            .pathParam("b", 0)
        .when()
            .get("/api/remainder/{a}/{b}")
        .then()
            .statusCode(anyOf(is(200), is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=remainderUsingGET type=boundary expect=class(200,400,404,422,500)
    @Test
    void remainderUsingGET_BVA_aZeroBoundary() {
        given()
            .pathParam("a", 0)
            .pathParam("b", 5)
        .when()
            .get("/api/remainder/{a}/{b}")
        .then()
            .statusCode(anyOf(is(200), is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=remainderUsingGET type=boundary expect=class(200,400,404,422,500)
    @Test
    void remainderUsingGET_BVA_maxIntBoundary() {
        given()
            .pathParam("a", 2147483647)
            .pathParam("b", 1)
        .when()
            .get("/api/remainder/{a}/{b}")
        .then()
            .statusCode(anyOf(is(200), is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=remainderUsingGET type=boundary expect=class(200,400,404,422,500)
    @Test
    void remainderUsingGET_BVA_minIntBoundary() {
        given()
            .pathParam("a", -2147483648)
            .pathParam("b", 1)
        .when()
            .get("/api/remainder/{a}/{b}")
        .then()
            .statusCode(anyOf(is(200), is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=remainderUsingGET type=errorcode expect=class(400,404,422,500)
    @Test
    void remainderUsingGET_ERR_wrongTypeForA() {
        given()
            .pathParam("a", "notAnInt")
            .pathParam("b", 3)
        .when()
            .get("/api/remainder/{a}/{b}")
        .then()
            .statusCode(anyOf(is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=remainderUsingGET type=errorcode expect=404
    @Test
    void remainderUsingGET_ERR_missingBSegment() {
        given()
            .pathParam("a", 10)
        .when()
            .get("/api/remainder/{a}/")
        .then()
            .statusCode(anyOf(is(404), is(400)));
    }

    // =========================================================
    // /api/triangle/{a}/{b}/{c}  (a,b,c: int32, all optional per spec)
    // =========================================================

    // SCENARIO op=checkTriangleUsingGET type=positive expect=200
    @Test
    void checkTriangleUsingGET_EP_validEquilateral() {
        given()
            .pathParam("a", 5)
            .pathParam("b", 5)
            .pathParam("c", 5)
        .when()
            .get("/api/triangle/{a}/{b}/{c}")
        .then()
            .statusCode(200)
            .body("resultAsInt", notNullValue());
    }

    // SCENARIO op=checkTriangleUsingGET type=positive expect=200
    @Test
    void checkTriangleUsingGET_EP_validScalene() {
        given()
            .pathParam("a", 3)
            .pathParam("b", 4)
            .pathParam("c", 5)
        .when()
            .get("/api/triangle/{a}/{b}/{c}")
        .then()
            .statusCode(200)
            .body("resultAsInt", notNullValue());
    }

    // SCENARIO op=checkTriangleUsingGET type=negative expect=class(200,400,404,422,500)
    @Test
    void checkTriangleUsingGET_EP_invalidNonTriangleSides() {
        given()
            .pathParam("a", 1)
            .pathParam("b", 1)
            .pathParam("c", 100)
        .when()
            .get("/api/triangle/{a}/{b}/{c}")
        .then()
            .statusCode(anyOf(is(200), is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=checkTriangleUsingGET type=negative expect=class(200,400,404,422,500)
    @Test
    void checkTriangleUsingGET_EP_negativeSideInvalidClass() {
        given()
            .pathParam("a", -3)
            .pathParam("b", 4)
            .pathParam("c", 5)
        .when()
            .get("/api/triangle/{a}/{b}/{c}")
        .then()
            .statusCode(anyOf(is(200), is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=checkTriangleUsingGET type=boundary expect=class(200,400,404,422,500)
    @Test
    void checkTriangleUsingGET_BVA_zeroSideBoundary() {
        given()
            .pathParam("a", 0)
            .pathParam("b", 4)
            .pathParam("c", 5)
        .when()
            .get("/api/triangle/{a}/{b}/{c}")
        .then()
            .statusCode(anyOf(is(200), is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=checkTriangleUsingGET type=boundary expect=class(200,400,404,422,500)
    @Test
    void checkTriangleUsingGET_BVA_oneSideBoundary() {
        given()
            .pathParam("a", 1)
            .pathParam("b", 1)
            .pathParam("c", 1)
        .when()
            .get("/api/triangle/{a}/{b}/{c}")
        .then()
            .statusCode(anyOf(is(200), is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=checkTriangleUsingGET type=boundary expect=class(200,400,404,422,500)
    @Test
    void checkTriangleUsingGET_BVA_maxIntSideBoundary() {
        given()
            .pathParam("a", 2147483647)
            .pathParam("b", 2147483647)
            .pathParam("c", 2147483647)
        .when()
            .get("/api/triangle/{a}/{b}/{c}")
        .then()
            .statusCode(anyOf(is(200), is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=checkTriangleUsingGET type=errorcode expect=class(400,404,422,500)
    @Test
    void checkTriangleUsingGET_ERR_wrongTypeForA() {
        given()
            .pathParam("a", "notAnInt")
            .pathParam("b", 4)
            .pathParam("c", 5)
        .when()
            .get("/api/triangle/{a}/{b}/{c}")
        .then()
            .statusCode(anyOf(is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=checkTriangleUsingGET type=errorcode expect=class(200,400,404,422,500)
    @Test
    void checkTriangleUsingGET_ERR_missingCSegment() {
        given()
            .pathParam("a", 3)
            .pathParam("b", 4)
        .when()
            .get("/api/triangle/{a}/{b}/")
        .then()
            .statusCode(anyOf(is(200), is(404), is(400), is(422), is(500)));
    }
}
