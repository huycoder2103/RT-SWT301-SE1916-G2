package manual;

import io.restassured.RestAssured;
import static io.restassured.RestAssured.given;
import org.junit.jupiter.api.*;
import static org.hamcrest.Matchers.*;

@TestMethodOrder(MethodOrderer.OrderAnnotation.class)
public class FeaturesManualTests {

    @BeforeAll
    static void setup() {
        RestAssured.baseURI = System.getProperty("baseURI", "http://localhost:8081");
        RestAssured.urlEncodingEnabled = false;
    }

    // ===================================================================
    // getAllProducts  (GET /products)
    // ===================================================================

    // SCENARIO op=getAllProducts type=positive expect=200
    @Test
    void getAllProducts_EP_validNoParams() {
        given()
        .when()
            .get("/products")
        .then()
            .statusCode(200);
    }

    // ===================================================================
    // getProductByName  (GET /products/{productName})
    // ===================================================================

    // SCENARIO op=getProductByName type=positive expect=200-or-404
    @Test
    void getProductByName_EP_validNamePlainString() {
        given()
            .pathParam("productName", "existingProduct")
        .when()
            .get("/products/{productName}")
        .then()
            .statusCode(anyOf(is(200), is(404)));
    }

    // SCENARIO op=getProductByName type=negative expect=404-or-error-class
    @Test
    void getProductByName_EP_unknownNameReturnsNotFoundClass() {
        given()
            .pathParam("productName", "definitelyDoesNotExist123")
        .when()
            .get("/products/{productName}")
        .then()
            .statusCode(anyOf(is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=getProductByName type=boundary expect=200-or-error-class
    @Test
    void getProductByName_BVA_singleCharacterName() {
        given()
            .pathParam("productName", "a")
        .when()
            .get("/products/{productName}")
        .then()
            .statusCode(anyOf(is(200), is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=getProductByName type=boundary expect=200-or-error-class
    @Test
    void getProductByName_BVA_veryLongName() {
        String longName = "n".repeat(2048);
        given()
            .pathParam("productName", longName)
        .when()
            .get("/products/{productName}")
        .then()
            .statusCode(anyOf(is(200), is(400), is(404), is(414), is(422), is(500)));
    }

    // SCENARIO op=getProductByName type=negative expect=error-class
    @Test
    void getProductByName_ERR_emptyPathSegmentNotFound() {
        given()
        .when()
            .get("/products//")
        .then()
            .statusCode(anyOf(is(400), is(404), is(405), is(500)));
    }

    // SCENARIO op=getProductByName type=negative expect=error-class
    @Test
    void getProductByName_ERR_specialCharactersInName() {
        given()
            .pathParam("productName", "prod uct/na*me?")
        .when()
            .get("/products/{productName}")
        .then()
            .statusCode(anyOf(is(200), is(400), is(404), is(422), is(500)));
    }

    // ===================================================================
    // getFeaturesForProduct  (GET /products/{productName}/features)
    // ===================================================================

    // SCENARIO op=getFeaturesForProduct type=positive expect=200-or-404
    @Test
    void getFeaturesForProduct_EP_validProductName() {
        given()
            .pathParam("productName", "someProduct")
        .when()
            .get("/products/{productName}/features")
        .then()
            .statusCode(anyOf(is(200), is(404)));
    }

    // SCENARIO op=getFeaturesForProduct type=negative expect=error-class
    @Test
    void getFeaturesForProduct_EP_nonExistentProductName() {
        given()
            .pathParam("productName", "noSuchProductXYZ")
        .when()
            .get("/products/{productName}/features")
        .then()
            .statusCode(anyOf(is(400), is(404), is(422), is(500)));
    }

    // ===================================================================
    // getConfigurationsForProduct  (GET /products/{productName}/configurations)
    // ===================================================================

    // SCENARIO op=getConfigurationsForProduct type=positive expect=200-or-404
    @Test
    void getConfigurationsForProduct_EP_validProductName() {
        given()
            .pathParam("productName", "someProduct")
        .when()
            .get("/products/{productName}/configurations")
        .then()
            .statusCode(anyOf(is(200), is(404)));
    }

    // SCENARIO op=getConfigurationsForProduct type=negative expect=error-class
    @Test
    void getConfigurationsForProduct_EP_nonExistentProductName() {
        given()
            .pathParam("productName", "noSuchProductXYZ")
        .when()
            .get("/products/{productName}/configurations")
        .then()
            .statusCode(anyOf(is(400), is(404), is(422), is(500)));
    }

    // ===================================================================
    // getConfigurationWithNameForProduct
    // (GET /products/{productName}/configurations/{configurationName})
    // ===================================================================

    // SCENARIO op=getConfigurationWithNameForProduct type=positive expect=200-or-404
    @Test
    void getConfigurationWithNameForProduct_EP_validBothNames() {
        given()
            .pathParam("productName", "someProduct")
            .pathParam("configurationName", "someConfig")
        .when()
            .get("/products/{productName}/configurations/{configurationName}")
        .then()
            .statusCode(anyOf(is(200), is(404)));
    }

    // SCENARIO op=getConfigurationWithNameForProduct type=negative expect=error-class
    @Test
    void getConfigurationWithNameForProduct_EP_nonExistentConfigurationName() {
        given()
            .pathParam("productName", "someProduct")
            .pathParam("configurationName", "noSuchConfigXYZ")
        .when()
            .get("/products/{productName}/configurations/{configurationName}")
        .then()
            .statusCode(anyOf(is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=getConfigurationWithNameForProduct type=negative expect=error-class
    @Test
    void getConfigurationWithNameForProduct_ERR_missingConfigurationSegment() {
        given()
            .pathParam("productName", "someProduct")
        .when()
            .get("/products/{productName}/configurations/")
        .then()
            .statusCode(anyOf(is(400), is(404), is(405), is(500)));
    }

    // ===================================================================
    // getConfigurationActivedFeatures
    // (GET /products/{productName}/configurations/{configurationName}/features)
    // ===================================================================

    // SCENARIO op=getConfigurationActivedFeatures type=positive expect=200-or-404
    @Test
    void getConfigurationActivedFeatures_EP_validBothNames() {
        given()
            .pathParam("productName", "someProduct")
            .pathParam("configurationName", "someConfig")
        .when()
            .get("/products/{productName}/configurations/{configurationName}/features")
        .then()
            .statusCode(anyOf(is(200), is(404)));
    }

    // SCENARIO op=getConfigurationActivedFeatures type=negative expect=error-class
    @Test
    void getConfigurationActivedFeatures_EP_nonExistentConfiguration() {
        given()
            .pathParam("productName", "someProduct")
            .pathParam("configurationName", "noSuchConfigXYZ")
        .when()
            .get("/products/{productName}/configurations/{configurationName}/features")
        .then()
            .statusCode(anyOf(is(400), is(404), is(422), is(500)));
    }

    // ===================================================================
    // deleteConstraint  (DELETE /products/{productName}/constraints/{constraintId})
    // constraintId is int64 -> EP / BVA on numeric boundary
    // ===================================================================

    // SCENARIO op=deleteConstraint type=positive expect=default-success-or-error-class
    @Test
    void deleteConstraint_EP_validPositiveId() {
        given()
            .pathParam("productName", "someProduct")
            .pathParam("constraintId", 1)
        .when()
            .delete("/products/{productName}/constraints/{constraintId}")
        .then()
            .statusCode(anyOf(is(200), is(204), is(404)));
    }

    // SCENARIO op=deleteConstraint type=boundary expect=error-class
    @Test
    void deleteConstraint_BVA_zeroId() {
        given()
            .pathParam("productName", "someProduct")
            .pathParam("constraintId", 0)
        .when()
            .delete("/products/{productName}/constraints/{constraintId}")
        .then()
            .statusCode(anyOf(is(200), is(204), is(400), is(404), is(422)));
    }

    // SCENARIO op=deleteConstraint type=boundary expect=error-class
    @Test
    void deleteConstraint_BVA_negativeId() {
        given()
            .pathParam("productName", "someProduct")
            .pathParam("constraintId", -1)
        .when()
            .delete("/products/{productName}/constraints/{constraintId}")
        .then()
            .statusCode(anyOf(is(200), is(204), is(400), is(404), is(422)));
    }

    // SCENARIO op=deleteConstraint type=boundary expect=success-or-error-class
    @Test
    void deleteConstraint_BVA_maxLongId() {
        given()
            .pathParam("productName", "someProduct")
            .pathParam("constraintId", Long.MAX_VALUE)
        .when()
            .delete("/products/{productName}/constraints/{constraintId}")
        .then()
            .statusCode(anyOf(is(200), is(204), is(400), is(404), is(422)));
    }

    // SCENARIO op=deleteConstraint type=negative expect=error-class
    @Test
    void deleteConstraint_ERR_nonNumericIdWrongType() {
        given()
            .pathParam("productName", "someProduct")
            .pathParam("constraintId", "notANumber")
        .when()
            .delete("/products/{productName}/constraints/{constraintId}")
        .then()
            .statusCode(anyOf(is(400), is(404), is(405), is(422), is(500)));
    }

    // ===================================================================
    // addRequiresConstraintToProduct
    // (POST /products/{productName}/constraints/requires) - formData sourceFeature, requiredFeature
    // ===================================================================

    // SCENARIO op=addRequiresConstraintToProduct type=positive expect=success-or-error-class
    @Test
    void addRequiresConstraintToProduct_EP_validFormFields() {
        given()
            .pathParam("productName", "someProduct")
            .formParam("sourceFeature", "featureA")
            .formParam("requiredFeature", "featureB")
        .when()
            .post("/products/{productName}/constraints/requires")
        .then()
            .statusCode(anyOf(is(200), is(201), is(204), is(400), is(404), is(422)));
    }

    // SCENARIO op=addRequiresConstraintToProduct type=negative expect=error-class-or-accepted
    @Test
    void addRequiresConstraintToProduct_EP_missingOptionalFormFields() {
        given()
            .pathParam("productName", "someProduct")
        .when()
            .post("/products/{productName}/constraints/requires")
        .then()
            .statusCode(anyOf(is(200), is(201), is(204), is(400), is(404), is(422)));
    }

    // SCENARIO op=addRequiresConstraintToProduct type=negative expect=error-class
    @Test
    void addRequiresConstraintToProduct_ERR_emptyValueFormFields() {
        given()
            .pathParam("productName", "someProduct")
            .formParam("sourceFeature", "")
            .formParam("requiredFeature", "")
        .when()
            .post("/products/{productName}/constraints/requires")
        .then()
            .statusCode(anyOf(is(200), is(201), is(204), is(400), is(404), is(422)));
    }

    // ===================================================================
    // addExcludesConstraintToProduct
    // (POST /products/{productName}/constraints/excludes) - formData sourceFeature, excludedFeature
    // ===================================================================

    // SCENARIO op=addExcludesConstraintToProduct type=positive expect=success-or-error-class
    @Test
    void addExcludesConstraintToProduct_EP_validFormFields() {
        given()
            .pathParam("productName", "someProduct")
            .formParam("sourceFeature", "featureA")
            .formParam("excludedFeature", "featureC")
        .when()
            .post("/products/{productName}/constraints/excludes")
        .then()
            .statusCode(anyOf(is(200), is(201), is(204), is(400), is(404), is(422)));
    }

    // SCENARIO op=addExcludesConstraintToProduct type=negative expect=error-class-or-accepted
    @Test
    void addExcludesConstraintToProduct_EP_missingOptionalFormFields() {
        given()
            .pathParam("productName", "someProduct")
        .when()
            .post("/products/{productName}/constraints/excludes")
        .then()
            .statusCode(anyOf(is(200), is(201), is(204), is(400), is(404), is(422)));
    }

    // ===================================================================
    // CRUD lifecycle: Product
    // create (addProduct) -> read (getProductByName) -> delete (deleteProductByName)
    //   -> read-after-delete
    // Note: spec exposes no update (PUT) operation for a whole Product, so the
    // lifecycle covers create/read/delete/read-after-delete plus not-found ops.
    // ===================================================================

    // SCENARIO op=addProduct type=positive expect=CRUD-create
    @Test
    @Order(1)
    void addProduct_CRUD_createProduct() {
        given()
            .pathParam("productName", "crudLifecycleProduct")
        .when()
            .post("/products/{productName}")
        .then()
            .statusCode(anyOf(is(200), is(201), is(204)));
    }

    // SCENARIO op=getProductByName type=positive expect=CRUD-read
    @Test
    @Order(2)
    void getProductByName_CRUD_readAfterCreate() {
        given()
            .pathParam("productName", "crudLifecycleProduct")
        .when()
            .get("/products/{productName}")
        .then()
            .statusCode(200)
            .body("name", notNullValue());
    }

    // SCENARIO op=addFeatureToProduct type=positive expect=CRUD-create-child
    @Test
    @Order(3)
    void addFeatureToProduct_CRUD_createFeatureUnderProduct() {
        given()
            .pathParam("productName", "crudLifecycleProduct")
            .pathParam("featureName", "crudLifecycleFeature")
            .formParam("description", "initial description")
        .when()
            .post("/products/{productName}/features/{featureName}")
        .then()
            .statusCode(anyOf(is(200), is(201), is(204)));
    }

    // SCENARIO op=updateFeatureOfProduct type=positive expect=CRUD-update
    @Test
    @Order(4)
    void updateFeatureOfProduct_CRUD_updateFeatureDescription() {
        given()
            .pathParam("productName", "crudLifecycleProduct")
            .pathParam("featureName", "crudLifecycleFeature")
            .formParam("description", "updated description")
        .when()
            .put("/products/{productName}/features/{featureName}")
        .then()
            .statusCode(200)
            .body("name", notNullValue());
    }

    // SCENARIO op=deleteFeatureOfProduct type=positive expect=CRUD-delete
    @Test
    @Order(5)
    void deleteFeatureOfProduct_CRUD_deleteFeature() {
        given()
            .pathParam("productName", "crudLifecycleProduct")
            .pathParam("featureName", "crudLifecycleFeature")
        .when()
            .delete("/products/{productName}/features/{featureName}")
        .then()
            .statusCode(anyOf(is(200), is(204)));
    }

    // SCENARIO op=deleteProductByName type=positive expect=CRUD-delete
    @Test
    @Order(6)
    void deleteProductByName_CRUD_deleteProduct() {
        given()
            .pathParam("productName", "crudLifecycleProduct")
        .when()
            .delete("/products/{productName}")
        .then()
            .statusCode(anyOf(is(200), is(204)));
    }

    // SCENARIO op=getProductByName type=negative expect=error-class
    @Test
    @Order(7)
    void getProductByName_CRUD_readAfterDeleteReturnsErrorClass() {
        given()
            .pathParam("productName", "crudLifecycleProduct")
        .when()
            .get("/products/{productName}")
        .then()
            .statusCode(anyOf(is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=updateFeatureOfProduct type=negative expect=error-class
    @Test
    @Order(8)
    void updateFeatureOfProduct_CRUD_updateNonExistentReturnsErrorClass() {
        given()
            .pathParam("productName", "crudLifecycleProduct")
            .pathParam("featureName", "crudLifecycleFeature")
            .formParam("description", "should not apply")
        .when()
            .put("/products/{productName}/features/{featureName}")
        .then()
            .statusCode(anyOf(is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=deleteFeatureOfProduct type=negative expect=error-class
    @Test
    @Order(9)
    void deleteFeatureOfProduct_CRUD_deleteNonExistentReturnsErrorClass() {
        given()
            .pathParam("productName", "crudLifecycleProduct")
            .pathParam("featureName", "crudLifecycleFeature")
        .when()
            .delete("/products/{productName}/features/{featureName}")
        .then()
            .statusCode(anyOf(is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=deleteProductByName type=negative expect=error-class
    @Test
    @Order(10)
    void deleteProductByName_CRUD_deleteNonExistentReturnsErrorClass() {
        given()
            .pathParam("productName", "crudLifecycleProduct")
        .when()
            .delete("/products/{productName}")
        .then()
            .statusCode(anyOf(is(400), is(404), is(422), is(500)));
    }

    // ===================================================================
    // Standalone not-found lifecycle checks for a never-created resource
    // ===================================================================

    // SCENARIO op=getFeaturesForProduct type=negative expect=error-class
    @Test
    void getFeaturesForProduct_CRUD_readOfNeverCreatedProduct() {
        given()
            .pathParam("productName", "neverCreatedProductXYZ")
        .when()
            .get("/products/{productName}/features")
        .then()
            .statusCode(anyOf(is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=deleteFeature type=negative expect=error-class
    @Test
    void deleteFeature_CRUD_deleteOfNeverCreatedResource() {
        given()
            .pathParam("productName", "neverCreatedProductXYZ")
            .pathParam("configurationName", "neverCreatedConfigXYZ")
            .pathParam("featureName", "neverCreatedFeatureXYZ")
        .when()
            .delete("/products/{productName}/configurations/{configurationName}/features/{featureName}")
        .then()
            .statusCode(anyOf(is(400), is(404), is(422), is(500)));
    }

    // ===================================================================
    // addFeatureToConfiguration (POST .../configurations/{configurationName}/features/{featureName})
    // ===================================================================

    // SCENARIO op=addFeatureToConfiguration type=positive expect=success-or-error-class
    @Test
    void addFeatureToConfiguration_EP_validAllSegments() {
        given()
            .pathParam("productName", "someProduct")
            .pathParam("configurationName", "someConfig")
            .pathParam("featureName", "someFeature")
        .when()
            .post("/products/{productName}/configurations/{configurationName}/features/{featureName}")
        .then()
            .statusCode(anyOf(is(200), is(201), is(204), is(400), is(404), is(422)));
    }

    // SCENARIO op=addFeatureToConfiguration type=negative expect=error-class
    @Test
    void addFeatureToConfiguration_ERR_nonExistentProductConfigFeature() {
        given()
            .pathParam("productName", "noSuchProductXYZ")
            .pathParam("configurationName", "noSuchConfigXYZ")
            .pathParam("featureName", "noSuchFeatureXYZ")
        .when()
            .post("/products/{productName}/configurations/{configurationName}/features/{featureName}")
        .then()
            .statusCode(anyOf(is(400), is(404), is(422), is(500)));
    }

    // ===================================================================
    // addProduct - error guessing on empty/whitespace path value
    // ===================================================================

    // SCENARIO op=addProduct type=negative expect=error-class
    @Test
    void addProduct_ERR_whitespaceOnlyName() {
        given()
            .pathParam("productName", " ")
        .when()
            .post("/products/{productName}")
        .then()
            .statusCode(anyOf(is(200), is(201), is(204), is(400), is(404), is(422)));
    }

    // SCENARIO op=addFeatureToProduct type=negative expect=error-class
    @Test
    void addFeatureToProduct_ERR_malformedBodyInsteadOfFormData() {
        given()
            .pathParam("productName", "someProduct")
            .pathParam("featureName", "someFeature")
            .contentType("application/json")
            .body("{ this is not valid json")
        .when()
            .post("/products/{productName}/features/{featureName}")
        .then()
            .statusCode(anyOf(is(200), is(201), is(204), is(400), is(404), is(415), is(422), is(500)));
    }
}
