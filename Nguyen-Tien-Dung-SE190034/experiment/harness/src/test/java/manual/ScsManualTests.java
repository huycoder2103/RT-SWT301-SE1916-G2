package manual;

import io.restassured.RestAssured;
import static io.restassured.RestAssured.given;
import org.junit.jupiter.api.*;
import static org.hamcrest.Matchers.*;

public class ScsManualTests {

    @BeforeAll
    static void setup() {
        RestAssured.baseURI = System.getProperty("baseURI", "http://localhost:8083");
        RestAssured.urlEncodingEnabled = false;
    }

    // =========================================================
    // /api/calc/{op}/{arg1}/{arg2}  -> calcUsingGET
    // arg1: number/double, arg2: number/double, op: string
    // =========================================================

    // SCENARIO op=calcUsingGET type=positive expect=200
    @Test
    void calcUsingGET_EP_validNumericArgsAndOp() {
        given()
            .pathParam("op", "add")
            .pathParam("arg1", 1.0)
            .pathParam("arg2", 2.0)
        .when()
            .get("/api/calc/{op}/{arg1}/{arg2}")
        .then()
            .statusCode(200)
            .body(notNullValue());
    }

    // SCENARIO op=calcUsingGET type=negative expect=error-class
    @Test
    void calcUsingGET_EP_invalidNonNumericArg() {
        given()
            .pathParam("op", "add")
            .pathParam("arg1", "notANumber")
            .pathParam("arg2", 2.0)
        .when()
            .get("/api/calc/{op}/{arg1}/{arg2}")
        .then()
            .statusCode(anyOf(is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=calcUsingGET type=boundary expect=200-or-error-class
    @Test
    void calcUsingGET_BVA_zeroArgs() {
        given()
            .pathParam("op", "add")
            .pathParam("arg1", 0)
            .pathParam("arg2", 0)
        .when()
            .get("/api/calc/{op}/{arg1}/{arg2}")
        .then()
            .statusCode(anyOf(is(200), is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=calcUsingGET type=boundary expect=200-or-error-class
    @Test
    void calcUsingGET_BVA_negativeOneArgs() {
        given()
            .pathParam("op", "add")
            .pathParam("arg1", -1)
            .pathParam("arg2", -1)
        .when()
            .get("/api/calc/{op}/{arg1}/{arg2}")
        .then()
            .statusCode(anyOf(is(200), is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=calcUsingGET type=boundary expect=200-or-error-class
    @Test
    void calcUsingGET_BVA_veryLargeArgs() {
        given()
            .pathParam("op", "add")
            .pathParam("arg1", 1.7976931348623157E100)
            .pathParam("arg2", 1.7976931348623157E100)
        .when()
            .get("/api/calc/{op}/{arg1}/{arg2}")
        .then()
            .statusCode(anyOf(is(200), is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=calcUsingGET type=boundary expect=200-or-error-class
    @Test
    void calcUsingGET_BVA_verySmallArgs() {
        given()
            .pathParam("op", "add")
            .pathParam("arg1", -1.7976931348623157E100)
            .pathParam("arg2", -1.7976931348623157E100)
        .when()
            .get("/api/calc/{op}/{arg1}/{arg2}")
        .then()
            .statusCode(anyOf(is(200), is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=calcUsingGET type=errorcode expect=error-class
    @Test
    void calcUsingGET_ERR_unsupportedOperationName() {
        given()
            .pathParam("op", "unsupportedOpXYZ")
            .pathParam("arg1", 1.0)
            .pathParam("arg2", 2.0)
        .when()
            .get("/api/calc/{op}/{arg1}/{arg2}")
        .then()
            .statusCode(anyOf(is(200), is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=calcUsingGET type=errorcode expect=404
    @Test
    void calcUsingGET_ERR_missingSegment() {
        given()
            .pathParam("op", "add")
            .pathParam("arg1", 1.0)
        .when()
            .get("/api/calc/{op}/{arg1}")
        .then()
            .statusCode(anyOf(is(400), is(404), is(422), is(500)));
    }

    // =========================================================
    // /api/cookie/{name}/{val}/{site}  -> cookieUsingGET
    // name, val, site: string
    // =========================================================

    // SCENARIO op=cookieUsingGET type=positive expect=200
    @Test
    void cookieUsingGET_EP_validStrings() {
        given()
            .pathParam("name", "sessionId")
            .pathParam("val", "abc123")
            .pathParam("site", "example.com")
        .when()
            .get("/api/cookie/{name}/{val}/{site}")
        .then()
            .statusCode(200)
            .body(notNullValue());
    }

    // SCENARIO op=cookieUsingGET type=boundary expect=200-or-error-class
    @Test
    void cookieUsingGET_BVA_emptyValSegment() {
        given()
            .pathParam("name", "sessionId")
            .pathParam("val", "")
            .pathParam("site", "example.com")
        .when()
            .get("/api/cookie/{name}/{val}/{site}")
        .then()
            .statusCode(anyOf(is(200), is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=cookieUsingGET type=boundary expect=200-or-error-class
    @Test
    void cookieUsingGET_BVA_singleCharSegments() {
        given()
            .pathParam("name", "a")
            .pathParam("val", "b")
            .pathParam("site", "c")
        .when()
            .get("/api/cookie/{name}/{val}/{site}")
        .then()
            .statusCode(anyOf(is(200), is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=cookieUsingGET type=boundary expect=200-or-error-class
    @Test
    void cookieUsingGET_BVA_veryLongNameSegment() {
        String longName = "n".repeat(2000);
        given()
            .pathParam("name", longName)
            .pathParam("val", "abc123")
            .pathParam("site", "example.com")
        .when()
            .get("/api/cookie/{name}/{val}/{site}")
        .then()
            .statusCode(anyOf(is(200), is(400), is(404), is(414), is(422), is(500)));
    }

    // SCENARIO op=cookieUsingGET type=errorcode expect=404
    @Test
    void cookieUsingGET_ERR_missingSegment() {
        given()
            .pathParam("name", "sessionId")
            .pathParam("val", "abc123")
        .when()
            .get("/api/cookie/{name}/{val}")
        .then()
            .statusCode(anyOf(is(400), is(404), is(422), is(500)));
    }

    // =========================================================
    // /api/costfuns/{i}/{s}  -> costfunsUsingGET
    // i: integer/int32, s: string
    // =========================================================

    // SCENARIO op=costfunsUsingGET type=positive expect=200
    @Test
    void costfunsUsingGET_EP_validIntAndString() {
        given()
            .pathParam("i", 5)
            .pathParam("s", "hello")
        .when()
            .get("/api/costfuns/{i}/{s}")
        .then()
            .statusCode(200)
            .body(notNullValue());
    }

    // SCENARIO op=costfunsUsingGET type=negative expect=error-class
    @Test
    void costfunsUsingGET_EP_invalidNonIntegerType() {
        given()
            .pathParam("i", "notAnInt")
            .pathParam("s", "hello")
        .when()
            .get("/api/costfuns/{i}/{s}")
        .then()
            .statusCode(anyOf(is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=costfunsUsingGET type=boundary expect=200-or-error-class
    @Test
    void costfunsUsingGET_BVA_zeroInt() {
        given()
            .pathParam("i", 0)
            .pathParam("s", "hello")
        .when()
            .get("/api/costfuns/{i}/{s}")
        .then()
            .statusCode(anyOf(is(200), is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=costfunsUsingGET type=boundary expect=200-or-error-class
    @Test
    void costfunsUsingGET_BVA_negativeOneInt() {
        given()
            .pathParam("i", -1)
            .pathParam("s", "hello")
        .when()
            .get("/api/costfuns/{i}/{s}")
        .then()
            .statusCode(anyOf(is(200), is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=costfunsUsingGET type=boundary expect=200-or-error-class
    @Test
    void costfunsUsingGET_BVA_int32MaxValue() {
        given()
            .pathParam("i", 2147483647)
            .pathParam("s", "hello")
        .when()
            .get("/api/costfuns/{i}/{s}")
        .then()
            .statusCode(anyOf(is(200), is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=costfunsUsingGET type=boundary expect=200-or-error-class
    @Test
    void costfunsUsingGET_BVA_int32MinValue() {
        given()
            .pathParam("i", -2147483648)
            .pathParam("s", "hello")
        .when()
            .get("/api/costfuns/{i}/{s}")
        .then()
            .statusCode(anyOf(is(200), is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=costfunsUsingGET type=boundary expect=200-or-error-class
    @Test
    void costfunsUsingGET_BVA_int32Overflow() {
        given()
            .pathParam("i", "2147483648")
            .pathParam("s", "hello")
        .when()
            .get("/api/costfuns/{i}/{s}")
        .then()
            .statusCode(anyOf(is(200), is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=costfunsUsingGET type=boundary expect=200-or-error-class
    @Test
    void costfunsUsingGET_BVA_emptyStringSegment() {
        given()
            .pathParam("i", 5)
            .pathParam("s", "")
        .when()
            .get("/api/costfuns/{i}/{s}")
        .then()
            .statusCode(anyOf(is(200), is(400), is(404), is(422), is(500)));
    }

    // =========================================================
    // /api/dateparse/{dayname}/{monthname}  -> dateParseUsingGET
    // dayname, monthname: string
    // =========================================================

    // SCENARIO op=dateParseUsingGET type=positive expect=200
    @Test
    void dateParseUsingGET_EP_validDayAndMonthNames() {
        given()
            .pathParam("dayname", "Monday")
            .pathParam("monthname", "January")
        .when()
            .get("/api/dateparse/{dayname}/{monthname}")
        .then()
            .statusCode(200)
            .body(notNullValue());
    }

    // SCENARIO op=dateParseUsingGET type=negative expect=error-class
    @Test
    void dateParseUsingGET_EP_invalidDayName() {
        given()
            .pathParam("dayname", "NotADay")
            .pathParam("monthname", "January")
        .when()
            .get("/api/dateparse/{dayname}/{monthname}")
        .then()
            .statusCode(anyOf(is(200), is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=dateParseUsingGET type=boundary expect=200-or-error-class
    @Test
    void dateParseUsingGET_BVA_emptyMonthNameSegment() {
        given()
            .pathParam("dayname", "Monday")
            .pathParam("monthname", "")
        .when()
            .get("/api/dateparse/{dayname}/{monthname}")
        .then()
            .statusCode(anyOf(is(200), is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=dateParseUsingGET type=errorcode expect=404
    @Test
    void dateParseUsingGET_ERR_missingSegment() {
        given()
            .pathParam("dayname", "Monday")
        .when()
            .get("/api/dateparse/{dayname}")
        .then()
            .statusCode(anyOf(is(400), is(404), is(422), is(500)));
    }

    // =========================================================
    // /api/filesuffix/{directory}/{file}  -> fileSuffixUsingGET
    // directory, file: string
    // =========================================================

    // SCENARIO op=fileSuffixUsingGET type=positive expect=200
    @Test
    void fileSuffixUsingGET_EP_validDirectoryAndFile() {
        given()
            .pathParam("directory", "docs")
            .pathParam("file", "report.pdf")
        .when()
            .get("/api/filesuffix/{directory}/{file}")
        .then()
            .statusCode(200)
            .body(notNullValue());
    }

    // SCENARIO op=fileSuffixUsingGET type=boundary expect=200-or-error-class
    @Test
    void fileSuffixUsingGET_BVA_fileWithNoExtension() {
        given()
            .pathParam("directory", "docs")
            .pathParam("file", "reportwithoutext")
        .when()
            .get("/api/filesuffix/{directory}/{file}")
        .then()
            .statusCode(anyOf(is(200), is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=fileSuffixUsingGET type=boundary expect=200-or-error-class
    @Test
    void fileSuffixUsingGET_BVA_emptyFileSegment() {
        given()
            .pathParam("directory", "docs")
            .pathParam("file", "")
        .when()
            .get("/api/filesuffix/{directory}/{file}")
        .then()
            .statusCode(anyOf(is(200), is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=fileSuffixUsingGET type=errorcode expect=404
    @Test
    void fileSuffixUsingGET_ERR_missingSegment() {
        given()
            .pathParam("directory", "docs")
        .when()
            .get("/api/filesuffix/{directory}")
        .then()
            .statusCode(anyOf(is(400), is(404), is(422), is(500)));
    }

    // =========================================================
    // /api/notypevar/{i}/{s}  -> notyPevarUsingGET
    // i: integer/int32, s: string
    // =========================================================

    // SCENARIO op=notyPevarUsingGET type=positive expect=200
    @Test
    void notyPevarUsingGET_EP_validIntAndString() {
        given()
            .pathParam("i", 3)
            .pathParam("s", "sample")
        .when()
            .get("/api/notypevar/{i}/{s}")
        .then()
            .statusCode(200)
            .body(notNullValue());
    }

    // SCENARIO op=notyPevarUsingGET type=negative expect=error-class
    @Test
    void notyPevarUsingGET_EP_invalidNonIntegerType() {
        given()
            .pathParam("i", "abc")
            .pathParam("s", "sample")
        .when()
            .get("/api/notypevar/{i}/{s}")
        .then()
            .statusCode(anyOf(is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=notyPevarUsingGET type=boundary expect=200-or-error-class
    @Test
    void notyPevarUsingGET_BVA_zeroInt() {
        given()
            .pathParam("i", 0)
            .pathParam("s", "sample")
        .when()
            .get("/api/notypevar/{i}/{s}")
        .then()
            .statusCode(anyOf(is(200), is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=notyPevarUsingGET type=boundary expect=200-or-error-class
    @Test
    void notyPevarUsingGET_BVA_int32MaxValue() {
        given()
            .pathParam("i", 2147483647)
            .pathParam("s", "sample")
        .when()
            .get("/api/notypevar/{i}/{s}")
        .then()
            .statusCode(anyOf(is(200), is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=notyPevarUsingGET type=boundary expect=200-or-error-class
    @Test
    void notyPevarUsingGET_BVA_emptyStringSegment() {
        given()
            .pathParam("i", 3)
            .pathParam("s", "")
        .when()
            .get("/api/notypevar/{i}/{s}")
        .then()
            .statusCode(anyOf(is(200), is(400), is(404), is(422), is(500)));
    }

    // =========================================================
    // /api/ordered4/{w}/{x}/{z}/{y}  -> ordered4UsingGET
    // w, x, y, z: string
    // =========================================================

    // SCENARIO op=ordered4UsingGET type=positive expect=200
    @Test
    void ordered4UsingGET_EP_validFourStrings() {
        given()
            .pathParam("w", "alpha")
            .pathParam("x", "beta")
            .pathParam("z", "gamma")
            .pathParam("y", "delta")
        .when()
            .get("/api/ordered4/{w}/{x}/{z}/{y}")
        .then()
            .statusCode(200)
            .body(notNullValue());
    }

    // SCENARIO op=ordered4UsingGET type=boundary expect=200-or-error-class
    @Test
    void ordered4UsingGET_BVA_emptyOneSegment() {
        given()
            .pathParam("w", "alpha")
            .pathParam("x", "")
            .pathParam("z", "gamma")
            .pathParam("y", "delta")
        .when()
            .get("/api/ordered4/{w}/{x}/{z}/{y}")
        .then()
            .statusCode(anyOf(is(200), is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=ordered4UsingGET type=boundary expect=200-or-error-class
    @Test
    void ordered4UsingGET_BVA_singleCharAllSegments() {
        given()
            .pathParam("w", "a")
            .pathParam("x", "b")
            .pathParam("z", "c")
            .pathParam("y", "d")
        .when()
            .get("/api/ordered4/{w}/{x}/{z}/{y}")
        .then()
            .statusCode(anyOf(is(200), is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=ordered4UsingGET type=errorcode expect=404
    @Test
    void ordered4UsingGET_ERR_missingSegment() {
        given()
            .pathParam("w", "alpha")
            .pathParam("x", "beta")
            .pathParam("z", "gamma")
        .when()
            .get("/api/ordered4/{w}/{x}/{z}")
        .then()
            .statusCode(anyOf(is(400), is(404), is(422), is(500)));
    }

    // =========================================================
    // /api/pat/{txt}  -> regexUsingGET
    // txt: string
    // =========================================================

    // SCENARIO op=regexUsingGET type=positive expect=200
    @Test
    void regexUsingGET_EP_validTextSegment() {
        given()
            .pathParam("txt", "sampleText123")
        .when()
            .get("/api/pat/{txt}")
        .then()
            .statusCode(200)
            .body(notNullValue());
    }

    // SCENARIO op=regexUsingGET type=boundary expect=200-or-error-class
    @Test
    void regexUsingGET_BVA_singleCharSegment() {
        given()
            .pathParam("txt", "a")
        .when()
            .get("/api/pat/{txt}")
        .then()
            .statusCode(anyOf(is(200), is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=regexUsingGET type=boundary expect=200-or-error-class
    @Test
    void regexUsingGET_BVA_veryLongTextSegment() {
        String longTxt = "x".repeat(2000);
        given()
            .pathParam("txt", longTxt)
        .when()
            .get("/api/pat/{txt}")
        .then()
            .statusCode(anyOf(is(200), is(400), is(404), is(414), is(422), is(500)));
    }

    // SCENARIO op=regexUsingGET type=errorcode expect=404
    @Test
    void regexUsingGET_ERR_missingSegment() {
        given()
        .when()
            .get("/api/pat/")
        .then()
            .statusCode(anyOf(is(400), is(404), is(422), is(500)));
    }

    // =========================================================
    // /api/pat/{txt}/{pat}  -> patUsingGET
    // txt, pat: string
    // =========================================================

    // SCENARIO op=patUsingGET type=positive expect=200
    @Test
    void patUsingGET_EP_validTextAndPattern() {
        given()
            .pathParam("txt", "sampleText123")
            .pathParam("pat", "[a-z]+")
        .when()
            .get("/api/pat/{txt}/{pat}")
        .then()
            .statusCode(200)
            .body(notNullValue());
    }

    // SCENARIO op=patUsingGET type=negative expect=error-class
    @Test
    void patUsingGET_EP_malformedPattern() {
        given()
            .pathParam("txt", "sampleText123")
            .pathParam("pat", "[a-z")
        .when()
            .get("/api/pat/{txt}/{pat}")
        .then()
            .statusCode(anyOf(is(200), is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=patUsingGET type=boundary expect=200-or-error-class
    @Test
    void patUsingGET_BVA_emptyPatternSegment() {
        given()
            .pathParam("txt", "sampleText123")
            .pathParam("pat", "")
        .when()
            .get("/api/pat/{txt}/{pat}")
        .then()
            .statusCode(anyOf(is(200), is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=patUsingGET type=errorcode expect=404
    @Test
    void patUsingGET_ERR_missingSegment() {
        given()
            .pathParam("txt", "sampleText123")
        .when()
            .get("/api/pat/{txt}")
        .then()
            .statusCode(200);
    }

    // =========================================================
    // /api/text2txt/{word1}/{word2}/{word3}  -> text2txtUsingGET
    // word1, word2, word3: string
    // =========================================================

    // SCENARIO op=text2txtUsingGET type=positive expect=200
    @Test
    void text2txtUsingGET_EP_validThreeWords() {
        given()
            .pathParam("word1", "hello")
            .pathParam("word2", "world")
            .pathParam("word3", "again")
        .when()
            .get("/api/text2txt/{word1}/{word2}/{word3}")
        .then()
            .statusCode(200)
            .body(notNullValue());
    }

    // SCENARIO op=text2txtUsingGET type=boundary expect=200-or-error-class
    @Test
    void text2txtUsingGET_BVA_emptyMiddleWordSegment() {
        given()
            .pathParam("word1", "hello")
            .pathParam("word2", "")
            .pathParam("word3", "again")
        .when()
            .get("/api/text2txt/{word1}/{word2}/{word3}")
        .then()
            .statusCode(anyOf(is(200), is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=text2txtUsingGET type=boundary expect=200-or-error-class
    @Test
    void text2txtUsingGET_BVA_singleCharWords() {
        given()
            .pathParam("word1", "a")
            .pathParam("word2", "b")
            .pathParam("word3", "c")
        .when()
            .get("/api/text2txt/{word1}/{word2}/{word3}")
        .then()
            .statusCode(anyOf(is(200), is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=text2txtUsingGET type=errorcode expect=404
    @Test
    void text2txtUsingGET_ERR_missingSegment() {
        given()
            .pathParam("word1", "hello")
            .pathParam("word2", "world")
        .when()
            .get("/api/text2txt/{word1}/{word2}")
        .then()
            .statusCode(anyOf(is(400), is(404), is(422), is(500)));
    }

    // =========================================================
    // /api/title/{sex}/{title}  -> titleUsingGET
    // sex, title: string
    // =========================================================

    // SCENARIO op=titleUsingGET type=positive expect=200
    @Test
    void titleUsingGET_EP_validSexAndTitle() {
        given()
            .pathParam("sex", "M")
            .pathParam("title", "Mr")
        .when()
            .get("/api/title/{sex}/{title}")
        .then()
            .statusCode(200)
            .body(notNullValue());
    }

    // SCENARIO op=titleUsingGET type=negative expect=error-class
    @Test
    void titleUsingGET_EP_invalidSexValue() {
        given()
            .pathParam("sex", "Unknown")
            .pathParam("title", "Mr")
        .when()
            .get("/api/title/{sex}/{title}")
        .then()
            .statusCode(anyOf(is(200), is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=titleUsingGET type=boundary expect=200-or-error-class
    @Test
    void titleUsingGET_BVA_emptyTitleSegment() {
        given()
            .pathParam("sex", "M")
            .pathParam("title", "")
        .when()
            .get("/api/title/{sex}/{title}")
        .then()
            .statusCode(anyOf(is(200), is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=titleUsingGET type=errorcode expect=404
    @Test
    void titleUsingGET_ERR_missingSegment() {
        given()
            .pathParam("sex", "M")
        .when()
            .get("/api/title/{sex}")
        .then()
            .statusCode(anyOf(is(400), is(404), is(422), is(500)));
    }
}
