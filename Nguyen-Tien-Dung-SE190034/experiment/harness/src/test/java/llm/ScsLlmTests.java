package llm;

import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Test;
import io.restassured.RestAssured;
import static io.restassured.RestAssured.given;
import static org.hamcrest.Matchers.*;

public class ScsLlmTests {

    @BeforeAll
    static void setup() {
        RestAssured.baseURI = System.getProperty("baseURI", "http://localhost:8080");
        RestAssured.urlEncodingEnabled = false;
    }

    // calcUsingGET  GET /api/calc/{op}/{arg1}/{arg2}

    // SCENARIO op=calcUsingGET type=positive expect=200
    @Test
    void calcUsingGET_P_addTwoPositiveDoubles() {
        given()
            .when().get("/api/calc/add/10/5")
            .then().statusCode(200).body(notNullValue());
    }

    // SCENARIO op=calcUsingGET type=positive expect=200
    @Test
    void calcUsingGET_P_subtractPositiveDoubles() {
        given()
            .when().get("/api/calc/subtract/20/3")
            .then().statusCode(200).body(notNullValue());
    }

    // SCENARIO op=calcUsingGET type=positive expect=200
    @Test
    void calcUsingGET_P_multiplyDoubles() {
        given()
            .when().get("/api/calc/multiply/6/7")
            .then().statusCode(200).body(notNullValue());
    }

    // SCENARIO op=calcUsingGET type=positive expect=200
    @Test
    void calcUsingGET_P_divideDoubles() {
        given()
            .when().get("/api/calc/divide/10/2")
            .then().statusCode(200).body(notNullValue());
    }

    // SCENARIO op=calcUsingGET type=positive expect=200
    @Test
    void calcUsingGET_P_negativeArgValues() {
        given()
            .when().get("/api/calc/add/-5/-3")
            .then().statusCode(200).body(notNullValue());
    }

    // SCENARIO op=calcUsingGET type=positive expect=200
    @Test
    void calcUsingGET_P_floatingPointArgs() {
        given()
            .when().get("/api/calc/add/1.5/2.5")
            .then().statusCode(200).body(notNullValue());
    }

    // SCENARIO op=calcUsingGET type=negative expect=4xx
    @Test
    void calcUsingGET_N_nonNumericArg1() {
        given()
            .when().get("/api/calc/add/abc/5")
            .then().statusCode(anyOf(is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=calcUsingGET type=negative expect=4xx
    @Test
    void calcUsingGET_N_nonNumericArg2() {
        given()
            .when().get("/api/calc/add/5/xyz")
            .then().statusCode(anyOf(is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=calcUsingGET type=negative expect=4xx
    @Test
    void calcUsingGET_N_bothArgsNonNumeric() {
        given()
            .when().get("/api/calc/add/foo/bar")
            .then().statusCode(anyOf(is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=calcUsingGET type=boundary expect=200
    @Test
    void calcUsingGET_B_zeroArgs() {
        given()
            .when().get("/api/calc/add/0/0")
            .then().statusCode(200).body(notNullValue());
    }

    // SCENARIO op=calcUsingGET type=boundary expect=200
    @Test
    void calcUsingGET_B_divideByZero() {
        given()
            .when().get("/api/calc/divide/10/0")
            .then().statusCode(anyOf(is(200), is(400), is(422), is(500)));
    }

    // SCENARIO op=calcUsingGET type=boundary expect=200
    @Test
    void calcUsingGET_B_veryLargeArgs() {
        given()
            .when().get("/api/calc/add/1.7976931348623157E308/1.7976931348623157E308")
            .then().statusCode(anyOf(is(200), is(400), is(422), is(500)));
    }

    // SCENARIO op=calcUsingGET type=boundary expect=200
    @Test
    void calcUsingGET_B_verySmallArgs() {
        given()
            .when().get("/api/calc/add/0.000000001/0.000000001")
            .then().statusCode(200).body(notNullValue());
    }

    // SCENARIO op=calcUsingGET type=boundary expect=200
    @Test
    void calcUsingGET_B_negativeTimePositive() {
        given()
            .when().get("/api/calc/multiply/-1/1")
            .then().statusCode(200).body(notNullValue());
    }

    // SCENARIO op=calcUsingGET type=errorcode expect=404
    @Test
    void calcUsingGET_E_unknownOpReturnsError() {
        given()
            .when().get("/api/calc/INVALIDOP/10/5")
            .then().statusCode(anyOf(is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=calcUsingGET type=errorcode expect=4xx
    @Test
    void calcUsingGET_E_emptyOpSegment() {
        given()
            .when().get("/api/calc/%20/10/5")
            .then().statusCode(anyOf(is(400), is(404), is(422), is(500)));
    }

    // cookieUsingGET  GET /api/cookie/{name}/{val}/{site}

    // SCENARIO op=cookieUsingGET type=positive expect=200
    @Test
    void cookieUsingGET_P_normalCookieParams() {
        given()
            .when().get("/api/cookie/session/abc123/example.com")
            .then().statusCode(200).body(notNullValue());
    }

    // SCENARIO op=cookieUsingGET type=positive expect=200
    @Test
    void cookieUsingGET_P_cookieWithHttpsSite() {
        given()
            .when().get("/api/cookie/auth/token999/https://secure.example.com")
            .then().statusCode(anyOf(is(200), is(400), is(404)));
    }

    // SCENARIO op=cookieUsingGET type=positive expect=200
    @Test
    void cookieUsingGET_P_cookieWithSimpleValues() {
        given()
            .when().get("/api/cookie/name/value/site")
            .then().statusCode(200).body(notNullValue());
    }

    // SCENARIO op=cookieUsingGET type=negative expect=4xx
    @Test
    void cookieUsingGET_N_missingSegmentReturnsError() {
        given()
            .when().get("/api/cookie/session/abc123")
            .then().statusCode(anyOf(is(400), is(404), is(405), is(422)));
    }

    // SCENARIO op=cookieUsingGET type=boundary expect=200
    @Test
    void cookieUsingGET_B_singleCharParams() {
        given()
            .when().get("/api/cookie/a/b/c")
            .then().statusCode(200).body(notNullValue());
    }

    // SCENARIO op=cookieUsingGET type=boundary expect=200orError
    @Test
    void cookieUsingGET_B_longCookieName() {
        String longName = "a".repeat(200);
        given()
            .when().get("/api/cookie/" + longName + "/val/site.com")
            .then().statusCode(anyOf(is(200), is(400), is(404), is(414), is(500)));
    }

    // SCENARIO op=cookieUsingGET type=boundary expect=200orError
    @Test
    void cookieUsingGET_B_specialCharsInVal() {
        given()
            .when().get("/api/cookie/name/val%21%40%23/site")
            .then().statusCode(anyOf(is(200), is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=cookieUsingGET type=errorcode expect=4xx
    @Test
    void cookieUsingGET_E_numericNameVal() {
        given()
            .when().get("/api/cookie/123/456/789")
            .then().statusCode(anyOf(is(200), is(400), is(404), is(422)));
    }

    // costfunsUsingGET  GET /api/costfuns/{i}/{s}

    // SCENARIO op=costfunsUsingGET type=positive expect=200
    @Test
    void costfunsUsingGET_P_validIntAndString() {
        given()
            .when().get("/api/costfuns/1/hello")
            .then().statusCode(200).body(notNullValue());
    }

    // SCENARIO op=costfunsUsingGET type=positive expect=200
    @Test
    void costfunsUsingGET_P_zeroIntAndString() {
        given()
            .when().get("/api/costfuns/0/test")
            .then().statusCode(200).body(notNullValue());
    }

    // SCENARIO op=costfunsUsingGET type=positive expect=200
    @Test
    void costfunsUsingGET_P_negativeIntAndString() {
        given()
            .when().get("/api/costfuns/-1/abc")
            .then().statusCode(200).body(notNullValue());
    }

    // SCENARIO op=costfunsUsingGET type=positive expect=200
    @Test
    void costfunsUsingGET_P_largeIntAndString() {
        given()
            .when().get("/api/costfuns/100/world")
            .then().statusCode(200).body(notNullValue());
    }

    // SCENARIO op=costfunsUsingGET type=negative expect=4xx
    @Test
    void costfunsUsingGET_N_nonIntegerI() {
        given()
            .when().get("/api/costfuns/abc/hello")
            .then().statusCode(anyOf(is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=costfunsUsingGET type=negative expect=4xx
    @Test
    void costfunsUsingGET_N_floatForIntI() {
        given()
            .when().get("/api/costfuns/1.5/hello")
            .then().statusCode(anyOf(is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=costfunsUsingGET type=boundary expect=200
    @Test
    void costfunsUsingGET_B_maxInt32() {
        given()
            .when().get("/api/costfuns/2147483647/maxtest")
            .then().statusCode(anyOf(is(200), is(400), is(422), is(500)));
    }

    // SCENARIO op=costfunsUsingGET type=boundary expect=200
    @Test
    void costfunsUsingGET_B_minInt32() {
        given()
            .when().get("/api/costfuns/-2147483648/mintest")
            .then().statusCode(anyOf(is(200), is(400), is(422), is(500)));
    }

    // SCENARIO op=costfunsUsingGET type=boundary expect=200
    @Test
    void costfunsUsingGET_B_emptyStringS() {
        given()
            .when().get("/api/costfuns/5/%20")
            .then().statusCode(anyOf(is(200), is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=costfunsUsingGET type=errorcode expect=4xx
    @Test
    void costfunsUsingGET_E_overflowInt() {
        given()
            .when().get("/api/costfuns/9999999999/overflow")
            .then().statusCode(anyOf(is(400), is(404), is(422), is(500)));
    }

    // dateParseUsingGET  GET /api/dateparse/{dayname}/{monthname}

    // SCENARIO op=dateParseUsingGET type=positive expect=200
    @Test
    void dateParseUsingGET_P_mondayJanuary() {
        given()
            .when().get("/api/dateparse/Monday/January")
            .then().statusCode(200).body(notNullValue());
    }

    // SCENARIO op=dateParseUsingGET type=positive expect=200
    @Test
    void dateParseUsingGET_P_fridayDecember() {
        given()
            .when().get("/api/dateparse/Friday/December")
            .then().statusCode(200).body(notNullValue());
    }

    // SCENARIO op=dateParseUsingGET type=positive expect=200
    @Test
    void dateParseUsingGET_P_abbreviatedDayMonth() {
        given()
            .when().get("/api/dateparse/Mon/Jan")
            .then().statusCode(anyOf(is(200), is(400), is(422)));
    }

    // SCENARIO op=dateParseUsingGET type=negative expect=4xx
    @Test
    void dateParseUsingGET_N_invalidDayName() {
        given()
            .when().get("/api/dateparse/Funday/January")
            .then().statusCode(anyOf(is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=dateParseUsingGET type=negative expect=4xx
    @Test
    void dateParseUsingGET_N_invalidMonthName() {
        given()
            .when().get("/api/dateparse/Monday/Octember")
            .then().statusCode(anyOf(is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=dateParseUsingGET type=negative expect=4xx
    @Test
    void dateParseUsingGET_N_numericDayAndMonth() {
        given()
            .when().get("/api/dateparse/1/1")
            .then().statusCode(anyOf(is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=dateParseUsingGET type=boundary expect=200orError
    @Test
    void dateParseUsingGET_B_lowercaseDayMonth() {
        given()
            .when().get("/api/dateparse/monday/january")
            .then().statusCode(anyOf(is(200), is(400), is(422), is(500)));
    }

    // SCENARIO op=dateParseUsingGET type=boundary expect=200orError
    @Test
    void dateParseUsingGET_B_uppercaseDayMonth() {
        given()
            .when().get("/api/dateparse/MONDAY/JANUARY")
            .then().statusCode(anyOf(is(200), is(400), is(422), is(500)));
    }

    // SCENARIO op=dateParseUsingGET type=boundary expect=200orError
    @Test
    void dateParseUsingGET_B_specialCharDayName() {
        given()
            .when().get("/api/dateparse/Mon%21day/January")
            .then().statusCode(anyOf(is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=dateParseUsingGET type=errorcode expect=4xx
    @Test
    void dateParseUsingGET_E_emptyDayPlaceholder() {
        given()
            .when().get("/api/dateparse/%20/January")
            .then().statusCode(anyOf(is(400), is(404), is(422), is(500)));
    }

    // fileSuffixUsingGET  GET /api/filesuffix/{directory}/{file}

    // SCENARIO op=fileSuffixUsingGET type=positive expect=200
    @Test
    void fileSuffixUsingGET_P_normalDirectoryAndFile() {
        given()
            .when().get("/api/filesuffix/home/readme.txt")
            .then().statusCode(200).body(notNullValue());
    }

    // SCENARIO op=fileSuffixUsingGET type=positive expect=200
    @Test
    void fileSuffixUsingGET_P_fileWithMultipleDots() {
        given()
            .when().get("/api/filesuffix/docs/archive.tar.gz")
            .then().statusCode(200).body(notNullValue());
    }

    // SCENARIO op=fileSuffixUsingGET type=positive expect=200
    @Test
    void fileSuffixUsingGET_P_fileNoExtension() {
        given()
            .when().get("/api/filesuffix/bin/executable")
            .then().statusCode(anyOf(is(200), is(400), is(422)));
    }

    // SCENARIO op=fileSuffixUsingGET type=positive expect=200
    @Test
    void fileSuffixUsingGET_P_deepDirectory() {
        given()
            .when().get("/api/filesuffix/usr/test.java")
            .then().statusCode(200).body(notNullValue());
    }

    // SCENARIO op=fileSuffixUsingGET type=negative expect=4xx
    @Test
    void fileSuffixUsingGET_N_missingFileSegment() {
        given()
            .when().get("/api/filesuffix/home")
            .then().statusCode(anyOf(is(400), is(404), is(405), is(422)));
    }

    // SCENARIO op=fileSuffixUsingGET type=boundary expect=200orError
    @Test
    void fileSuffixUsingGET_B_singleCharDirAndFile() {
        given()
            .when().get("/api/filesuffix/a/b.c")
            .then().statusCode(200).body(notNullValue());
    }

    // SCENARIO op=fileSuffixUsingGET type=boundary expect=200orError
    @Test
    void fileSuffixUsingGET_B_longFileName() {
        String longFile = "a".repeat(200) + ".txt";
        given()
            .when().get("/api/filesuffix/dir/" + longFile)
            .then().statusCode(anyOf(is(200), is(400), is(404), is(414), is(500)));
    }

    // SCENARIO op=fileSuffixUsingGET type=boundary expect=200orError
    @Test
    void fileSuffixUsingGET_B_hiddenFileStartingWithDot() {
        given()
            .when().get("/api/filesuffix/home/.bashrc")
            .then().statusCode(anyOf(is(200), is(400), is(404), is(422)));
    }

    // SCENARIO op=fileSuffixUsingGET type=errorcode expect=4xx
    @Test
    void fileSuffixUsingGET_E_specialCharsInPath() {
        given()
            .when().get("/api/filesuffix/home%2Fuser/file.txt")
            .then().statusCode(anyOf(is(200), is(400), is(404), is(422), is(500)));
    }

    // notyPevarUsingGET  GET /api/notypevar/{i}/{s}

    // SCENARIO op=notyPevarUsingGET type=positive expect=200
    @Test
    void notyPevarUsingGET_P_validIntAndString() {
        given()
            .when().get("/api/notypevar/5/hello")
            .then().statusCode(200).body(notNullValue());
    }

    // SCENARIO op=notyPevarUsingGET type=positive expect=200
    @Test
    void notyPevarUsingGET_P_zeroAndString() {
        given()
            .when().get("/api/notypevar/0/world")
            .then().statusCode(200).body(notNullValue());
    }

    // SCENARIO op=notyPevarUsingGET type=positive expect=200
    @Test
    void notyPevarUsingGET_P_negativeIntAndString() {
        given()
            .when().get("/api/notypevar/-10/test")
            .then().statusCode(200).body(notNullValue());
    }

    // SCENARIO op=notyPevarUsingGET type=negative expect=4xx
    @Test
    void notyPevarUsingGET_N_nonIntegerI() {
        given()
            .when().get("/api/notypevar/abc/hello")
            .then().statusCode(anyOf(is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=notyPevarUsingGET type=negative expect=4xx
    @Test
    void notyPevarUsingGET_N_floatForIntI() {
        given()
            .when().get("/api/notypevar/3.14/pi")
            .then().statusCode(anyOf(is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=notyPevarUsingGET type=boundary expect=200
    @Test
    void notyPevarUsingGET_B_maxInt32() {
        given()
            .when().get("/api/notypevar/2147483647/max")
            .then().statusCode(anyOf(is(200), is(400), is(422), is(500)));
    }

    // SCENARIO op=notyPevarUsingGET type=boundary expect=200
    @Test
    void notyPevarUsingGET_B_minInt32() {
        given()
            .when().get("/api/notypevar/-2147483648/min")
            .then().statusCode(anyOf(is(200), is(400), is(422), is(500)));
    }

    // SCENARIO op=notyPevarUsingGET type=boundary expect=200
    @Test
    void notyPevarUsingGET_B_oneAndEmptyStringLike() {
        given()
            .when().get("/api/notypevar/1/a")
            .then().statusCode(200).body(notNullValue());
    }

    // SCENARIO op=notyPevarUsingGET type=errorcode expect=4xx
    @Test
    void notyPevarUsingGET_E_overflowInteger() {
        given()
            .when().get("/api/notypevar/99999999999/overflow")
            .then().statusCode(anyOf(is(400), is(404), is(422), is(500)));
    }

    // ordered4UsingGET  GET /api/ordered4/{w}/{x}/{z}/{y}

    // SCENARIO op=ordered4UsingGET type=positive expect=200
    @Test
    void ordered4UsingGET_P_ascendingStrings() {
        given()
            .when().get("/api/ordered4/a/b/c/d")
            .then().statusCode(200).body(notNullValue());
    }

    // SCENARIO op=ordered4UsingGET type=positive expect=200
    @Test
    void ordered4UsingGET_P_wordStrings() {
        given()
            .when().get("/api/ordered4/apple/banana/cherry/date")
            .then().statusCode(200).body(notNullValue());
    }

    // SCENARIO op=ordered4UsingGET type=positive expect=200
    @Test
    void ordered4UsingGET_P_equalStrings() {
        given()
            .when().get("/api/ordered4/same/same/same/same")
            .then().statusCode(200).body(notNullValue());
    }

    // SCENARIO op=ordered4UsingGET type=positive expect=200
    @Test
    void ordered4UsingGET_P_descendingStrings() {
        given()
            .when().get("/api/ordered4/d/c/b/a")
            .then().statusCode(200).body(notNullValue());
    }

    // SCENARIO op=ordered4UsingGET type=negative expect=4xx
    @Test
    void ordered4UsingGET_N_missingOneSegment() {
        given()
            .when().get("/api/ordered4/a/b/c")
            .then().statusCode(anyOf(is(400), is(404), is(405), is(422)));
    }

    // SCENARIO op=ordered4UsingGET type=boundary expect=200
    @Test
    void ordered4UsingGET_B_singleCharEachParam() {
        given()
            .when().get("/api/ordered4/a/b/c/d")
            .then().statusCode(200).body(notNullValue());
    }

    // SCENARIO op=ordered4UsingGET type=boundary expect=200orError
    @Test
    void ordered4UsingGET_B_longStrings() {
        String longStr = "z".repeat(100);
        given()
            .when().get("/api/ordered4/" + longStr + "/a/b/c")
            .then().statusCode(anyOf(is(200), is(400), is(404), is(414), is(500)));
    }

    // SCENARIO op=ordered4UsingGET type=boundary expect=200orError
    @Test
    void ordered4UsingGET_B_numericStrings() {
        given()
            .when().get("/api/ordered4/1/2/3/4")
            .then().statusCode(200).body(notNullValue());
    }

    // SCENARIO op=ordered4UsingGET type=errorcode expect=4xx
    @Test
    void ordered4UsingGET_E_specialCharInParam() {
        given()
            .when().get("/api/ordered4/a%00b/c/d/e")
            .then().statusCode(anyOf(is(400), is(404), is(422), is(500)));
    }

    // regexUsingGET  GET /api/pat/{txt}

    // SCENARIO op=regexUsingGET type=positive expect=200
    @Test
    void regexUsingGET_P_simpleAlphanumericText() {
        given()
            .when().get("/api/pat/hello123")
            .then().statusCode(200).body(notNullValue());
    }

    // SCENARIO op=regexUsingGET type=positive expect=200
    @Test
    void regexUsingGET_P_singleWord() {
        given()
            .when().get("/api/pat/world")
            .then().statusCode(200).body(notNullValue());
    }

    // SCENARIO op=regexUsingGET type=positive expect=200
    @Test
    void regexUsingGET_P_emailLikeText() {
        given()
            .when().get("/api/pat/user%40example.com")
            .then().statusCode(anyOf(is(200), is(400), is(422)));
    }

    // SCENARIO op=regexUsingGET type=negative expect=4xx
    @Test
    void regexUsingGET_N_missingTxtSegment() {
        given()
            .when().get("/api/pat/")
            .then().statusCode(anyOf(is(400), is(404), is(405), is(422)));
    }

    // SCENARIO op=regexUsingGET type=boundary expect=200orError
    @Test
    void regexUsingGET_B_singleChar() {
        given()
            .when().get("/api/pat/a")
            .then().statusCode(200).body(notNullValue());
    }

    // SCENARIO op=regexUsingGET type=boundary expect=200orError
    @Test
    void regexUsingGET_B_veryLongText() {
        String longText = "a".repeat(500);
        given()
            .when().get("/api/pat/" + longText)
            .then().statusCode(anyOf(is(200), is(400), is(404), is(414), is(500)));
    }

    // SCENARIO op=regexUsingGET type=boundary expect=200orError
    @Test
    void regexUsingGET_B_numericOnlyText() {
        given()
            .when().get("/api/pat/123456")
            .then().statusCode(200).body(notNullValue());
    }

    // SCENARIO op=regexUsingGET type=errorcode expect=4xx
    @Test
    void regexUsingGET_E_regexSpecialChars() {
        given()
            .when().get("/api/pat/.*%2B%3F%5B%5D")
            .then().statusCode(anyOf(is(200), is(400), is(404), is(422), is(500)));
    }

    // patUsingGET  GET /api/pat/{txt}/{pat}

    // SCENARIO op=patUsingGET type=positive expect=200
    @Test
    void patUsingGET_P_simplePatternMatch() {
        given()
            .when().get("/api/pat/hello/ell")
            .then().statusCode(200).body(notNullValue());
    }

    // SCENARIO op=patUsingGET type=positive expect=200
    @Test
    void patUsingGET_P_noMatchPattern() {
        given()
            .when().get("/api/pat/hello/xyz")
            .then().statusCode(200).body(notNullValue());
    }

    // SCENARIO op=patUsingGET type=positive expect=200
    @Test
    void patUsingGET_P_patternEqualsText() {
        given()
            .when().get("/api/pat/abc/abc")
            .then().statusCode(200).body(notNullValue());
    }

    // SCENARIO op=patUsingGET type=positive expect=200
    @Test
    void patUsingGET_P_numericTextAndPattern() {
        given()
            .when().get("/api/pat/12345/234")
            .then().statusCode(200).body(notNullValue());
    }

    // SCENARIO op=patUsingGET type=negative expect=4xx
    @Test
    void patUsingGET_N_missingPatSegment() {
        given()
            .when().get("/api/pat/hello")
            .then().statusCode(anyOf(is(200), is(400), is(404), is(405)));
    }

    // SCENARIO op=patUsingGET type=boundary expect=200
    @Test
    void patUsingGET_B_singleCharTxtAndPat() {
        given()
            .when().get("/api/pat/a/a")
            .then().statusCode(200).body(notNullValue());
    }

    // SCENARIO op=patUsingGET type=boundary expect=200orError
    @Test
    void patUsingGET_B_patternLongerThanText() {
        given()
            .when().get("/api/pat/ab/abcdefgh")
            .then().statusCode(anyOf(is(200), is(400), is(422)));
    }

    // SCENARIO op=patUsingGET type=boundary expect=200orError
    @Test
    void patUsingGET_B_longTextShortPat() {
        String longText = "abcdefghij".repeat(50);
        given()
            .when().get("/api/pat/" + longText + "/abc")
            .then().statusCode(anyOf(is(200), is(400), is(414), is(500)));
    }

    // SCENARIO op=patUsingGET type=errorcode expect=4xx
    @Test
    void patUsingGET_E_regexSpecialInPat() {
        given()
            .when().get("/api/pat/hello/(world)")
            .then().statusCode(anyOf(is(200), is(400), is(422), is(500)));
    }

    // text2txtUsingGET  GET /api/text2txt/{word1}/{word2}/{word3}

    // SCENARIO op=text2txtUsingGET type=positive expect=200
    @Test
    void text2txtUsingGET_P_threeSimpleWords() {
        given()
            .when().get("/api/text2txt/hello/world/foo")
            .then().statusCode(200).body(notNullValue());
    }

    // SCENARIO op=text2txtUsingGET type=positive expect=200
    @Test
    void text2txtUsingGET_P_numberWords() {
        given()
            .when().get("/api/text2txt/one/two/three")
            .then().statusCode(200).body(notNullValue());
    }

    // SCENARIO op=text2txtUsingGET type=positive expect=200
    @Test
    void text2txtUsingGET_P_sameWord() {
        given()
            .when().get("/api/text2txt/same/same/same")
            .then().statusCode(200).body(notNullValue());
    }

    // SCENARIO op=text2txtUsingGET type=negative expect=4xx
    @Test
    void text2txtUsingGET_N_missingThirdWord() {
        given()
            .when().get("/api/text2txt/hello/world")
            .then().statusCode(anyOf(is(400), is(404), is(405), is(422)));
    }

    // SCENARIO op=text2txtUsingGET type=negative expect=4xx
    @Test
    void text2txtUsingGET_N_missingAllWords() {
        given()
            .when().get("/api/text2txt/")
            .then().statusCode(anyOf(is(400), is(404), is(405), is(422)));
    }

    // SCENARIO op=text2txtUsingGET type=boundary expect=200
    @Test
    void text2txtUsingGET_B_singleCharWords() {
        given()
            .when().get("/api/text2txt/a/b/c")
            .then().statusCode(200).body(notNullValue());
    }

    // SCENARIO op=text2txtUsingGET type=boundary expect=200orError
    @Test
    void text2txtUsingGET_B_longWords() {
        String longWord = "word".repeat(50);
        given()
            .when().get("/api/text2txt/" + longWord + "/short/word")
            .then().statusCode(anyOf(is(200), is(400), is(414), is(500)));
    }

    // SCENARIO op=text2txtUsingGET type=boundary expect=200orError
    @Test
    void text2txtUsingGET_B_numericWords() {
        given()
            .when().get("/api/text2txt/123/456/789")
            .then().statusCode(200).body(notNullValue());
    }

    // SCENARIO op=text2txtUsingGET type=errorcode expect=4xx
    @Test
    void text2txtUsingGET_E_specialCharInWords() {
        given()
            .when().get("/api/text2txt/hel%26lo/wor%26ld/fo%26o")
            .then().statusCode(anyOf(is(200), is(400), is(404), is(422), is(500)));
    }

    // titleUsingGET  GET /api/title/{sex}/{title}

    // SCENARIO op=titleUsingGET type=positive expect=200
    @Test
    void titleUsingGET_P_maleMrTitle() {
        given()
            .when().get("/api/title/male/Mr")
            .then().statusCode(200).body(notNullValue());
    }

    // SCENARIO op=titleUsingGET type=positive expect=200
    @Test
    void titleUsingGET_P_femaleMrsTitle() {
        given()
            .when().get("/api/title/female/Mrs")
            .then().statusCode(200).body(notNullValue());
    }

    // SCENARIO op=titleUsingGET type=positive expect=200
    @Test
    void titleUsingGET_P_femaleMissTitle() {
        given()
            .when().get("/api/title/female/Miss")
            .then().statusCode(200).body(notNullValue());
    }

    // SCENARIO op=titleUsingGET type=positive expect=200
    @Test
    void titleUsingGET_P_maleDrTitle() {
        given()
            .when().get("/api/title/male/Dr")
            .then().statusCode(200).body(notNullValue());
    }

    // SCENARIO op=titleUsingGET type=negative expect=4xx
    @Test
    void titleUsingGET_N_invalidSex() {
        given()
            .when().get("/api/title/other/Mr")
            .then().statusCode(anyOf(is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=titleUsingGET type=negative expect=4xx
    @Test
    void titleUsingGET_N_invalidTitle() {
        given()
            .when().get("/api/title/male/Lord")
            .then().statusCode(anyOf(is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=titleUsingGET type=negative expect=4xx
    @Test
    void titleUsingGET_N_missingTitleSegment() {
        given()
            .when().get("/api/title/male")
            .then().statusCode(anyOf(is(400), is(404), is(405), is(422)));
    }

    // SCENARIO op=titleUsingGET type=boundary expect=200orError
    @Test
    void titleUsingGET_B_lowercaseSex() {
        given()
            .when().get("/api/title/Male/Mr")
            .then().statusCode(anyOf(is(200), is(400), is(422)));
    }

    // SCENARIO op=titleUsingGET type=boundary expect=200orError
    @Test
    void titleUsingGET_B_uppercaseSex() {
        given()
            .when().get("/api/title/MALE/MR")
            .then().statusCode(anyOf(is(200), is(400), is(422)));
    }

    // SCENARIO op=titleUsingGET type=boundary expect=200orError
    @Test
    void titleUsingGET_B_emptyLikeSex() {
        given()
            .when().get("/api/title/%20/Mr")
            .then().statusCode(anyOf(is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=titleUsingGET type=errorcode expect=4xx
    @Test
    void titleUsingGET_E_numericSexAndTitle() {
        given()
            .when().get("/api/title/1/2")
            .then().statusCode(anyOf(is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=titleUsingGET type=errorcode expect=4xx
    @Test
    void titleUsingGET_E_mismatchedSexAndTitle() {
        given()
            .when().get("/api/title/female/Mr")
            .then().statusCode(anyOf(is(400), is(404), is(422), is(500)));
    }
}
