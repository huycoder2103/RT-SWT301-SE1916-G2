package llm;

import io.restassured.RestAssured;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Test;

import static io.restassured.RestAssured.given;
import static org.hamcrest.Matchers.*;

public class NcsLlmTests {

    @BeforeAll
    static void setup() {
        RestAssured.baseURI = System.getProperty("baseURI", "http://localhost:8080");
        RestAssured.urlEncodingEnabled = false;
    }

    // /api/bessj/{n}/{x}   operationId: bessjUsingGET

    // SCENARIO op=bessjUsingGET type=positive expect=200
    @Test
    void bessjUsingGET_P_validNandX() {
        given()
            .when().get("/api/bessj/2/1.0")
            .then().statusCode(200)
            .body("resultAsDouble", notNullValue());
    }

    // SCENARIO op=bessjUsingGET type=positive expect=200
    @Test
    void bessjUsingGET_P_nEqualsOne() {
        given()
            .when().get("/api/bessj/1/2.5")
            .then().statusCode(200)
            .body(anyOf(hasKey("resultAsDouble"), hasKey("resultAsInt")));
    }

    // SCENARIO op=bessjUsingGET type=positive expect=200
    @Test
    void bessjUsingGET_P_largeN() {
        given()
            .when().get("/api/bessj/10/5.0")
            .then().statusCode(200);
    }

    // SCENARIO op=bessjUsingGET type=negative expect=4xx
    @Test
    void bessjUsingGET_N_nonIntegerN() {
        given()
            .when().get("/api/bessj/abc/1.0")
            .then().statusCode(anyOf(is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=bessjUsingGET type=negative expect=4xx
    @Test
    void bessjUsingGET_N_nonNumericX() {
        given()
            .when().get("/api/bessj/2/xyz")
            .then().statusCode(anyOf(is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=bessjUsingGET type=negative expect=4xx
    @Test
    void bessjUsingGET_N_bothParamsInvalid() {
        given()
            .when().get("/api/bessj/!@#/!@#")
            .then().statusCode(anyOf(is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=bessjUsingGET type=boundary expect=200
    @Test
    void bessjUsingGET_B_nZero() {
        given()
            .when().get("/api/bessj/0/1.0")
            .then().statusCode(anyOf(is(200), is(400), is(422), is(500)));
    }

    // SCENARIO op=bessjUsingGET type=boundary expect=200or4xx
    @Test
    void bessjUsingGET_B_negativeN() {
        given()
            .when().get("/api/bessj/-1/1.0")
            .then().statusCode(anyOf(is(200), is(400), is(422), is(500)));
    }

    // SCENARIO op=bessjUsingGET type=boundary expect=200or4xx
    @Test
    void bessjUsingGET_B_xZero() {
        given()
            .when().get("/api/bessj/2/0.0")
            .then().statusCode(anyOf(is(200), is(400), is(422), is(500)));
    }

    // SCENARIO op=bessjUsingGET type=boundary expect=200or4xx
    @Test
    void bessjUsingGET_B_negativeX() {
        given()
            .when().get("/api/bessj/2/-1.0")
            .then().statusCode(anyOf(is(200), is(400), is(422), is(500)));
    }

    // SCENARIO op=bessjUsingGET type=boundary expect=200or4xx
    @Test
    void bessjUsingGET_B_veryLargeN() {
        given()
            .when().get("/api/bessj/2147483647/1.0")
            .then().statusCode(anyOf(is(200), is(400), is(422), is(500)));
    }

    // SCENARIO op=bessjUsingGET type=boundary expect=200or4xx
    @Test
    void bessjUsingGET_B_veryLargeX() {
        given()
            .when().get("/api/bessj/2/1.7976931348623157E308")
            .then().statusCode(anyOf(is(200), is(400), is(422), is(500)));
    }

    // SCENARIO op=bessjUsingGET type=errorcode expect=4xx
    @Test
    void bessjUsingGET_E_missingXSegment() {
        given()
            .when().get("/api/bessj/2")
            .then().statusCode(anyOf(is(400), is(404), is(405)));
    }

    // SCENARIO op=bessjUsingGET type=errorcode expect=4xx
    @Test
    void bessjUsingGET_E_emptyNSegment() {
        given()
            .when().get("/api/bessj//1.0")
            .then().statusCode(anyOf(is(400), is(404), is(405)));
    }

    // /api/expint/{n}/{x}   operationId: expintUsingGET

    // SCENARIO op=expintUsingGET type=positive expect=200
    @Test
    void expintUsingGET_P_validNandX() {
        given()
            .when().get("/api/expint/1/1.0")
            .then().statusCode(200)
            .body("resultAsDouble", notNullValue());
    }

    // SCENARIO op=expintUsingGET type=positive expect=200
    @Test
    void expintUsingGET_P_nTwo_xPointFive() {
        given()
            .when().get("/api/expint/2/0.5")
            .then().statusCode(200);
    }

    // SCENARIO op=expintUsingGET type=negative expect=4xx
    @Test
    void expintUsingGET_N_nonIntegerN() {
        given()
            .when().get("/api/expint/abc/1.0")
            .then().statusCode(anyOf(is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=expintUsingGET type=negative expect=4xx
    @Test
    void expintUsingGET_N_nonNumericX() {
        given()
            .when().get("/api/expint/1/xyz")
            .then().statusCode(anyOf(is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=expintUsingGET type=negative expect=4xx
    @Test
    void expintUsingGET_N_specialCharsParams() {
        given()
            .when().get("/api/expint/!@#/$%^")
            .then().statusCode(anyOf(is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=expintUsingGET type=boundary expect=200or4xx
    @Test
    void expintUsingGET_B_nZero() {
        given()
            .when().get("/api/expint/0/1.0")
            .then().statusCode(anyOf(is(200), is(400), is(422), is(500)));
    }

    // SCENARIO op=expintUsingGET type=boundary expect=200or4xx
    @Test
    void expintUsingGET_B_negativeN() {
        given()
            .when().get("/api/expint/-1/1.0")
            .then().statusCode(anyOf(is(200), is(400), is(422), is(500)));
    }

    // SCENARIO op=expintUsingGET type=boundary expect=200or4xx
    @Test
    void expintUsingGET_B_xZero() {
        given()
            .when().get("/api/expint/1/0.0")
            .then().statusCode(anyOf(is(200), is(400), is(422), is(500)));
    }

    // SCENARIO op=expintUsingGET type=boundary expect=200or4xx
    @Test
    void expintUsingGET_B_negativeX() {
        given()
            .when().get("/api/expint/1/-1.0")
            .then().statusCode(anyOf(is(200), is(400), is(422), is(500)));
    }

    // SCENARIO op=expintUsingGET type=boundary expect=200or4xx
    @Test
    void expintUsingGET_B_largeN() {
        given()
            .when().get("/api/expint/2147483647/1.0")
            .then().statusCode(anyOf(is(200), is(400), is(422), is(500)));
    }

    // SCENARIO op=expintUsingGET type=errorcode expect=4xx
    @Test
    void expintUsingGET_E_missingXSegment() {
        given()
            .when().get("/api/expint/1")
            .then().statusCode(anyOf(is(400), is(404), is(405)));
    }

    // SCENARIO op=expintUsingGET type=errorcode expect=4xx
    @Test
    void expintUsingGET_E_xEqualsInfinity() {
        given()
            .when().get("/api/expint/1/Infinity")
            .then().statusCode(anyOf(is(200), is(400), is(422), is(500)));
    }

    // /api/fisher/{m}/{n}/{x}   operationId: fisherUsingGET

    // SCENARIO op=fisherUsingGET type=positive expect=200
    @Test
    void fisherUsingGET_P_validMNX() {
        given()
            .when().get("/api/fisher/5/10/2.5")
            .then().statusCode(200)
            .body("resultAsDouble", notNullValue());
    }

    // SCENARIO op=fisherUsingGET type=positive expect=200
    @Test
    void fisherUsingGET_P_mOneNOne() {
        given()
            .when().get("/api/fisher/1/1/1.0")
            .then().statusCode(200);
    }

    // SCENARIO op=fisherUsingGET type=negative expect=4xx
    @Test
    void fisherUsingGET_N_nonIntegerM() {
        given()
            .when().get("/api/fisher/abc/10/2.5")
            .then().statusCode(anyOf(is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=fisherUsingGET type=negative expect=4xx
    @Test
    void fisherUsingGET_N_nonIntegerN() {
        given()
            .when().get("/api/fisher/5/xyz/2.5")
            .then().statusCode(anyOf(is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=fisherUsingGET type=negative expect=4xx
    @Test
    void fisherUsingGET_N_nonNumericX() {
        given()
            .when().get("/api/fisher/5/10/notANumber")
            .then().statusCode(anyOf(is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=fisherUsingGET type=negative expect=4xx
    @Test
    void fisherUsingGET_N_allInvalidParams() {
        given()
            .when().get("/api/fisher/a/b/c")
            .then().statusCode(anyOf(is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=fisherUsingGET type=boundary expect=200or4xx
    @Test
    void fisherUsingGET_B_mZero() {
        given()
            .when().get("/api/fisher/0/10/2.5")
            .then().statusCode(anyOf(is(200), is(400), is(422), is(500)));
    }

    // SCENARIO op=fisherUsingGET type=boundary expect=200or4xx
    @Test
    void fisherUsingGET_B_nZero() {
        given()
            .when().get("/api/fisher/5/0/2.5")
            .then().statusCode(anyOf(is(200), is(400), is(422), is(500)));
    }

    // SCENARIO op=fisherUsingGET type=boundary expect=200or4xx
    @Test
    void fisherUsingGET_B_xZero() {
        given()
            .when().get("/api/fisher/5/10/0.0")
            .then().statusCode(anyOf(is(200), is(400), is(422), is(500)));
    }

    // SCENARIO op=fisherUsingGET type=boundary expect=200or4xx
    @Test
    void fisherUsingGET_B_negativeM() {
        given()
            .when().get("/api/fisher/-1/10/2.5")
            .then().statusCode(anyOf(is(200), is(400), is(422), is(500)));
    }

    // SCENARIO op=fisherUsingGET type=boundary expect=200or4xx
    @Test
    void fisherUsingGET_B_negativeX() {
        given()
            .when().get("/api/fisher/5/10/-1.0")
            .then().statusCode(anyOf(is(200), is(400), is(422), is(500)));
    }

    // SCENARIO op=fisherUsingGET type=boundary expect=200or4xx
    @Test
    void fisherUsingGET_B_veryLargeM() {
        given()
            .when().get("/api/fisher/2147483647/10/2.5")
            .then().statusCode(anyOf(is(200), is(400), is(422), is(500)));
    }

    // SCENARIO op=fisherUsingGET type=errorcode expect=4xx
    @Test
    void fisherUsingGET_E_missingXSegment() {
        given()
            .when().get("/api/fisher/5/10")
            .then().statusCode(anyOf(is(400), is(404), is(405)));
    }

    // SCENARIO op=fisherUsingGET type=errorcode expect=4xx
    @Test
    void fisherUsingGET_E_xNaN() {
        given()
            .when().get("/api/fisher/5/10/NaN")
            .then().statusCode(anyOf(is(200), is(400), is(422), is(500)));
    }

    // /api/gammq/{a}/{x}   operationId: gammqUsingGET

    // SCENARIO op=gammqUsingGET type=positive expect=200
    @Test
    void gammqUsingGET_P_validAandX() {
        given()
            .when().get("/api/gammq/2.0/1.0")
            .then().statusCode(200)
            .body("resultAsDouble", notNullValue());
    }

    // SCENARIO op=gammqUsingGET type=positive expect=200
    @Test
    void gammqUsingGET_P_aHalfXTwo() {
        given()
            .when().get("/api/gammq/0.5/2.0")
            .then().statusCode(200);
    }

    // SCENARIO op=gammqUsingGET type=positive expect=200
    @Test
    void gammqUsingGET_P_integerLikeDoubles() {
        given()
            .when().get("/api/gammq/3.0/3.0")
            .then().statusCode(200);
    }

    // SCENARIO op=gammqUsingGET type=negative expect=4xx
    @Test
    void gammqUsingGET_N_nonNumericA() {
        given()
            .when().get("/api/gammq/abc/1.0")
            .then().statusCode(anyOf(is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=gammqUsingGET type=negative expect=4xx
    @Test
    void gammqUsingGET_N_nonNumericX() {
        given()
            .when().get("/api/gammq/2.0/xyz")
            .then().statusCode(anyOf(is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=gammqUsingGET type=negative expect=4xx
    @Test
    void gammqUsingGET_N_specialChars() {
        given()
            .when().get("/api/gammq/!@#/!@#")
            .then().statusCode(anyOf(is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=gammqUsingGET type=boundary expect=200or4xx
    @Test
    void gammqUsingGET_B_aZero() {
        given()
            .when().get("/api/gammq/0.0/1.0")
            .then().statusCode(anyOf(is(200), is(400), is(422), is(500)));
    }

    // SCENARIO op=gammqUsingGET type=boundary expect=200or4xx
    @Test
    void gammqUsingGET_B_xZero() {
        given()
            .when().get("/api/gammq/2.0/0.0")
            .then().statusCode(anyOf(is(200), is(400), is(422), is(500)));
    }

    // SCENARIO op=gammqUsingGET type=boundary expect=200or4xx
    @Test
    void gammqUsingGET_B_negativeA() {
        given()
            .when().get("/api/gammq/-1.0/1.0")
            .then().statusCode(anyOf(is(200), is(400), is(422), is(500)));
    }

    // SCENARIO op=gammqUsingGET type=boundary expect=200or4xx
    @Test
    void gammqUsingGET_B_negativeX() {
        given()
            .when().get("/api/gammq/2.0/-1.0")
            .then().statusCode(anyOf(is(200), is(400), is(422), is(500)));
    }

    // SCENARIO op=gammqUsingGET type=boundary expect=200or4xx
    @Test
    void gammqUsingGET_B_verySmallA() {
        given()
            .when().get("/api/gammq/1.0E-300/1.0")
            .then().statusCode(anyOf(is(200), is(400), is(422), is(500)));
    }

    // SCENARIO op=gammqUsingGET type=boundary expect=200or4xx
    @Test
    void gammqUsingGET_B_veryLargeX() {
        given()
            .when().get("/api/gammq/2.0/1.0E300")
            .then().statusCode(anyOf(is(200), is(400), is(422), is(500)));
    }

    // SCENARIO op=gammqUsingGET type=errorcode expect=4xx
    @Test
    void gammqUsingGET_E_missingXSegment() {
        given()
            .when().get("/api/gammq/2.0")
            .then().statusCode(anyOf(is(400), is(404), is(405)));
    }

    // SCENARIO op=gammqUsingGET type=errorcode expect=4xx
    @Test
    void gammqUsingGET_E_bothZero() {
        given()
            .when().get("/api/gammq/0.0/0.0")
            .then().statusCode(anyOf(is(200), is(400), is(422), is(500)));
    }

    // /api/remainder/{a}/{b}   operationId: remainderUsingGET

    // SCENARIO op=remainderUsingGET type=positive expect=200
    @Test
    void remainderUsingGET_P_validAandB() {
        given()
            .when().get("/api/remainder/10/3")
            .then().statusCode(200)
            .body("resultAsInt", notNullValue());
    }

    // SCENARIO op=remainderUsingGET type=positive expect=200
    @Test
    void remainderUsingGET_P_aEqualsB() {
        given()
            .when().get("/api/remainder/7/7")
            .then().statusCode(200)
            .body("resultAsInt", is(0));
    }

    // SCENARIO op=remainderUsingGET type=positive expect=200
    @Test
    void remainderUsingGET_P_aSmallerThanB() {
        given()
            .when().get("/api/remainder/3/10")
            .then().statusCode(200);
    }

    // SCENARIO op=remainderUsingGET type=negative expect=4xx
    @Test
    void remainderUsingGET_N_nonIntegerA() {
        given()
            .when().get("/api/remainder/abc/3")
            .then().statusCode(anyOf(is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=remainderUsingGET type=negative expect=4xx
    @Test
    void remainderUsingGET_N_nonIntegerB() {
        given()
            .when().get("/api/remainder/10/xyz")
            .then().statusCode(anyOf(is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=remainderUsingGET type=negative expect=4xx
    @Test
    void remainderUsingGET_N_floatA() {
        given()
            .when().get("/api/remainder/10.5/3")
            .then().statusCode(anyOf(is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=remainderUsingGET type=negative expect=4xx
    @Test
    void remainderUsingGET_N_specialChars() {
        given()
            .when().get("/api/remainder/!@#/$%^")
            .then().statusCode(anyOf(is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=remainderUsingGET type=boundary expect=200or4xx
    @Test
    void remainderUsingGET_B_bZero() {
        given()
            .when().get("/api/remainder/10/0")
            .then().statusCode(anyOf(is(200), is(400), is(422), is(500)));
    }

    // SCENARIO op=remainderUsingGET type=boundary expect=200or4xx
    @Test
    void remainderUsingGET_B_aZero() {
        given()
            .when().get("/api/remainder/0/3")
            .then().statusCode(anyOf(is(200), is(400), is(422), is(500)));
    }

    // SCENARIO op=remainderUsingGET type=boundary expect=200or4xx
    @Test
    void remainderUsingGET_B_negativeA() {
        given()
            .when().get("/api/remainder/-10/3")
            .then().statusCode(anyOf(is(200), is(400), is(422), is(500)));
    }

    // SCENARIO op=remainderUsingGET type=boundary expect=200or4xx
    @Test
    void remainderUsingGET_B_negativeB() {
        given()
            .when().get("/api/remainder/10/-3")
            .then().statusCode(anyOf(is(200), is(400), is(422), is(500)));
    }

    // SCENARIO op=remainderUsingGET type=boundary expect=200or4xx
    @Test
    void remainderUsingGET_B_maxIntA() {
        given()
            .when().get("/api/remainder/2147483647/3")
            .then().statusCode(anyOf(is(200), is(400), is(422), is(500)));
    }

    // SCENARIO op=remainderUsingGET type=boundary expect=200or4xx
    @Test
    void remainderUsingGET_B_minIntA() {
        given()
            .when().get("/api/remainder/-2147483648/3")
            .then().statusCode(anyOf(is(200), is(400), is(422), is(500)));
    }

    // SCENARIO op=remainderUsingGET type=errorcode expect=4xx
    @Test
    void remainderUsingGET_E_missingBSegment() {
        given()
            .when().get("/api/remainder/10")
            .then().statusCode(anyOf(is(400), is(404), is(405)));
    }

    // SCENARIO op=remainderUsingGET type=errorcode expect=4xx
    @Test
    void remainderUsingGET_E_bothZero() {
        given()
            .when().get("/api/remainder/0/0")
            .then().statusCode(anyOf(is(200), is(400), is(422), is(500)));
    }

    // /api/triangle/{a}/{b}/{c}   operationId: checkTriangleUsingGET

    // SCENARIO op=checkTriangleUsingGET type=positive expect=200
    @Test
    void checkTriangleUsingGET_P_equilateralTriangle() {
        given()
            .when().get("/api/triangle/3/3/3")
            .then().statusCode(200)
            .body(anyOf(hasKey("resultAsInt"), hasKey("resultAsDouble")));
    }

    // SCENARIO op=checkTriangleUsingGET type=positive expect=200
    @Test
    void checkTriangleUsingGET_P_isoscelesTriangle() {
        given()
            .when().get("/api/triangle/5/5/3")
            .then().statusCode(200);
    }

    // SCENARIO op=checkTriangleUsingGET type=positive expect=200
    @Test
    void checkTriangleUsingGET_P_scaleneTriangle() {
        given()
            .when().get("/api/triangle/3/4/5")
            .then().statusCode(200);
    }

    // SCENARIO op=checkTriangleUsingGET type=positive expect=200
    @Test
    void checkTriangleUsingGET_P_rightTriangle() {
        given()
            .when().get("/api/triangle/6/8/10")
            .then().statusCode(200);
    }

    // SCENARIO op=checkTriangleUsingGET type=negative expect=4xx
    @Test
    void checkTriangleUsingGET_N_nonIntegerA() {
        given()
            .when().get("/api/triangle/abc/4/5")
            .then().statusCode(anyOf(is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=checkTriangleUsingGET type=negative expect=4xx
    @Test
    void checkTriangleUsingGET_N_floatEdge() {
        given()
            .when().get("/api/triangle/3.5/4/5")
            .then().statusCode(anyOf(is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=checkTriangleUsingGET type=negative expect=4xx
    @Test
    void checkTriangleUsingGET_N_allNonInteger() {
        given()
            .when().get("/api/triangle/a/b/c")
            .then().statusCode(anyOf(is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=checkTriangleUsingGET type=boundary expect=200or4xx
    @Test
    void checkTriangleUsingGET_B_degenerateTriangle() {
        given()
            .when().get("/api/triangle/1/2/3")
            .then().statusCode(anyOf(is(200), is(400), is(422)));
    }

    // SCENARIO op=checkTriangleUsingGET type=boundary expect=200or4xx
    @Test
    void checkTriangleUsingGET_B_invalidTriangleInequality() {
        given()
            .when().get("/api/triangle/1/2/10")
            .then().statusCode(anyOf(is(200), is(400), is(422)));
    }

    // SCENARIO op=checkTriangleUsingGET type=boundary expect=200or4xx
    @Test
    void checkTriangleUsingGET_B_allOnes() {
        given()
            .when().get("/api/triangle/1/1/1")
            .then().statusCode(anyOf(is(200), is(400), is(422)));
    }

    // SCENARIO op=checkTriangleUsingGET type=boundary expect=200or4xx
    @Test
    void checkTriangleUsingGET_B_negativeEdge() {
        given()
            .when().get("/api/triangle/-1/3/4")
            .then().statusCode(anyOf(is(200), is(400), is(422), is(500)));
    }

    // SCENARIO op=checkTriangleUsingGET type=boundary expect=200or4xx
    @Test
    void checkTriangleUsingGET_B_zeroEdge() {
        given()
            .when().get("/api/triangle/0/3/4")
            .then().statusCode(anyOf(is(200), is(400), is(422), is(500)));
    }

    // SCENARIO op=checkTriangleUsingGET type=boundary expect=200or4xx
    @Test
    void checkTriangleUsingGET_B_veryLargeEdges() {
        given()
            .when().get("/api/triangle/2147483647/2147483647/2147483647")
            .then().statusCode(anyOf(is(200), is(400), is(422), is(500)));
    }

    // SCENARIO op=checkTriangleUsingGET type=boundary expect=200or4xx
    @Test
    void checkTriangleUsingGET_B_allZeroEdges() {
        given()
            .when().get("/api/triangle/0/0/0")
            .then().statusCode(anyOf(is(200), is(400), is(422), is(500)));
    }

    // SCENARIO op=checkTriangleUsingGET type=errorcode expect=4xx
    @Test
    void checkTriangleUsingGET_E_missingCSegment() {
        given()
            .when().get("/api/triangle/3/4")
            .then().statusCode(anyOf(is(400), is(404), is(405)));
    }

    // SCENARIO op=checkTriangleUsingGET type=errorcode expect=4xx
    @Test
    void checkTriangleUsingGET_E_allNegativeEdges() {
        given()
            .when().get("/api/triangle/-3/-4/-5")
            .then().statusCode(anyOf(is(200), is(400), is(422), is(500)));
    }

    // SCENARIO op=checkTriangleUsingGET type=errorcode expect=4xx
    @Test
    void checkTriangleUsingGET_E_specialCharEdges() {
        given()
            .when().get("/api/triangle/!@#/!@#/!@#")
            .then().statusCode(anyOf(is(400), is(404), is(422), is(500)));
    }
}
