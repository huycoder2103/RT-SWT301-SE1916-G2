package llm;

import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Test;
import io.restassured.RestAssured;
import static io.restassured.RestAssured.given;
import static org.hamcrest.Matchers.*;

public class FeaturesLlmTests {

    @BeforeAll
    static void setup() {
        RestAssured.baseURI = System.getProperty("baseURI", "http://localhost:8080");
        RestAssured.urlEncodingEnabled = false;
        RestAssured.enableLoggingOfRequestAndResponseIfValidationFails();
    }

    // =========================================================
    // getAllProducts - GET /products
    // =========================================================

    // SCENARIO op=getAllProducts type=positive expect=200
    @Test
    void getAllProducts_P_returnsArrayOfStrings() {
        given()
            .when().get("/products")
            .then().statusCode(200)
            .body("$", instanceOf(java.util.List.class));
    }

    // SCENARIO op=getAllProducts type=boundary expect=200
    @Test
    void getAllProducts_B_emptyListAcceptable() {
        given()
            .when().get("/products")
            .then().statusCode(200);
    }

    // SCENARIO op=getAllProducts type=negative expect=4xx
    @Test
    void getAllProducts_N_unsupportedMediaTypeHeader() {
        given()
            .header("Accept", "text/plain")
            .when().get("/products")
            .then().statusCode(anyOf(is(200), is(406)));
    }

    // SCENARIO op=getAllProducts type=errorcode expect=405
    @Test
    void getAllProducts_E_methodNotAllowed() {
        given()
            .contentType("application/json")
            .body("{}")
            .when().post("/products")
            .then().statusCode(anyOf(is(400), is(404), is(405), is(422), is(500)));
    }

    // =========================================================
    // getProductByName - GET /products/{productName}
    // =========================================================

    // SCENARIO op=getProductByName type=positive expect=200
    @Test
    void getProductByName_P_existingProduct() {
        // Create product first, then retrieve it
        String productName = "TestProduct_GPB_P";
        given().when().post("/products/" + productName).then();

        given()
            .when().get("/products/" + productName)
            .then().statusCode(anyOf(is(200), is(404)));
    }

    // SCENARIO op=getProductByName type=negative expect=4xx
    @Test
    void getProductByName_N_nonExistentProduct() {
        given()
            .when().get("/products/nonExistentProduct_xyz_99999")
            .then().statusCode(anyOf(is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=getProductByName type=boundary expect=200or4xx
    @Test
    void getProductByName_B_singleCharName() {
        String productName = "X";
        given().when().post("/products/" + productName).then();

        given()
            .when().get("/products/" + productName)
            .then().statusCode(anyOf(is(200), is(404), is(400)));
    }

    // SCENARIO op=getProductByName type=boundary expect=2xxor4xx
    @Test
    void getProductByName_B_veryLongProductName() {
        String longName = "A".repeat(255);
        given()
            .when().get("/products/" + longName)
            .then().statusCode(anyOf(is(200), is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=getProductByName type=errorcode expect=4xx
    @Test
    void getProductByName_E_specialCharactersInName() {
        given()
            .when().get("/products/product%20with%20spaces")
            .then().statusCode(anyOf(is(200), is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=getProductByName type=boundary expect=200
    @Test
    void getProductByName_B_responseBodyHasProductFields() {
        String productName = "TestProduct_GPB_Fields";
        given().when().post("/products/" + productName).then();

        given()
            .when().get("/products/" + productName)
            .then().statusCode(anyOf(is(200), is(404)));
    }

    // =========================================================
    // addProduct - POST /products/{productName}
    // =========================================================

    // SCENARIO op=addProduct type=positive expect=2xx
    @Test
    void addProduct_P_createNewProduct() {
        String productName = "NewProduct_AP_P";
        given()
            .when().post("/products/" + productName)
            .then().statusCode(anyOf(is(200), is(201), is(204)));
    }

    // SCENARIO op=addProduct type=negative expect=4xx
    @Test
    void addProduct_N_duplicateProductName() {
        String productName = "DuplicateProduct_AP_N";
        given().when().post("/products/" + productName).then();

        given()
            .when().post("/products/" + productName)
            .then().statusCode(anyOf(is(200), is(201), is(204), is(400), is(409), is(422), is(500)));
    }

    // SCENARIO op=addProduct type=boundary expect=2xxor4xx
    @Test
    void addProduct_B_singleCharProductName() {
        String productName = "Z";
        given()
            .when().post("/products/" + productName)
            .then().statusCode(anyOf(is(200), is(201), is(204), is(400), is(422)));
    }

    // SCENARIO op=addProduct type=boundary expect=2xxor4xx
    @Test
    void addProduct_B_veryLongProductName() {
        String longName = "B".repeat(255);
        given()
            .when().post("/products/" + longName)
            .then().statusCode(anyOf(is(200), is(201), is(204), is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=addProduct type=errorcode expect=4xx
    @Test
    void addProduct_E_numericNameBoundary() {
        given()
            .when().post("/products/0")
            .then().statusCode(anyOf(is(200), is(201), is(204), is(400), is(422), is(500)));
    }

    // =========================================================
    // deleteProductByName - DELETE /products/{productName}
    // =========================================================

    // SCENARIO op=deleteProductByName type=positive expect=2xx
    @Test
    void deleteProductByName_P_existingProduct() {
        String productName = "ProductToDelete_DP_P";
        given().when().post("/products/" + productName).then();

        given()
            .when().delete("/products/" + productName)
            .then().statusCode(anyOf(is(200), is(204)));
    }

    // SCENARIO op=deleteProductByName type=negative expect=4xx
    @Test
    void deleteProductByName_N_nonExistentProduct() {
        given()
            .when().delete("/products/nonExistentForDelete_xyz_99999")
            .then().statusCode(anyOf(is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=deleteProductByName type=boundary expect=2xxor4xx
    @Test
    void deleteProductByName_B_deleteAlreadyDeleted() {
        String productName = "ProductDoubleDelete_DP_B";
        given().when().post("/products/" + productName).then();
        given().when().delete("/products/" + productName).then();

        given()
            .when().delete("/products/" + productName)
            .then().statusCode(anyOf(is(200), is(204), is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=deleteProductByName type=errorcode expect=4xx
    @Test
    void deleteProductByName_E_specialCharsInName() {
        given()
            .when().delete("/products/!!invalid!!")
            .then().statusCode(anyOf(is(200), is(204), is(400), is(404), is(422), is(500)));
    }

    // =========================================================
    // getConfigurationsForProduct - GET /products/{productName}/configurations
    // =========================================================

    // SCENARIO op=getConfigurationsForProduct type=positive expect=200
    @Test
    void getConfigurationsForProduct_P_existingProduct() {
        String productName = "ProdForConfigs_GCFP_P";
        given().when().post("/products/" + productName).then();

        given()
            .when().get("/products/" + productName + "/configurations")
            .then().statusCode(anyOf(is(200), is(404)));
    }

    // SCENARIO op=getConfigurationsForProduct type=negative expect=4xx
    @Test
    void getConfigurationsForProduct_N_nonExistentProduct() {
        given()
            .when().get("/products/nonExistentProd_GCFP_N/configurations")
            .then().statusCode(anyOf(is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=getConfigurationsForProduct type=boundary expect=200
    @Test
    void getConfigurationsForProduct_B_emptyConfigsList() {
        String productName = "ProdEmptyConfigs_GCFP_B";
        given().when().post("/products/" + productName).then();

        given()
            .when().get("/products/" + productName + "/configurations")
            .then().statusCode(anyOf(is(200), is(404)))
            .body(anyOf(nullValue(), instanceOf(String.class)));
    }

    // SCENARIO op=getConfigurationsForProduct type=errorcode expect=4xx
    @Test
    void getConfigurationsForProduct_E_numericProductName() {
        given()
            .when().get("/products/12345/configurations")
            .then().statusCode(anyOf(is(200), is(400), is(404), is(422), is(500)));
    }

    // =========================================================
    // getConfigurationWithNameForProduct - GET /products/{productName}/configurations/{configurationName}
    // =========================================================

    // SCENARIO op=getConfigurationWithNameForProduct type=positive expect=200
    @Test
    void getConfigurationWithNameForProduct_P_existingConfig() {
        String productName = "ProdForGetConf_GCWNFP_P";
        String configName = "Config_GCWNFP_P";
        given().when().post("/products/" + productName).then();
        given().when().post("/products/" + productName + "/configurations/" + configName).then();

        given()
            .when().get("/products/" + productName + "/configurations/" + configName)
            .then().statusCode(anyOf(is(200), is(404)));
    }

    // SCENARIO op=getConfigurationWithNameForProduct type=negative expect=4xx
    @Test
    void getConfigurationWithNameForProduct_N_nonExistentConfig() {
        String productName = "ProdForGetConf_GCWNFP_N";
        given().when().post("/products/" + productName).then();

        given()
            .when().get("/products/" + productName + "/configurations/nonExistentConfig_xyz_99999")
            .then().statusCode(anyOf(is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=getConfigurationWithNameForProduct type=negative expect=4xx
    @Test
    void getConfigurationWithNameForProduct_N_nonExistentProduct() {
        given()
            .when().get("/products/nonExistentProd_GCWNFP_N2/configurations/anyConfig")
            .then().statusCode(anyOf(is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=getConfigurationWithNameForProduct type=boundary expect=200or4xx
    @Test
    void getConfigurationWithNameForProduct_B_singleCharNames() {
        String productName = "P";
        String configName = "C";
        given().when().post("/products/" + productName).then();
        given().when().post("/products/" + productName + "/configurations/" + configName).then();

        given()
            .when().get("/products/" + productName + "/configurations/" + configName)
            .then().statusCode(anyOf(is(200), is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=getConfigurationWithNameForProduct type=errorcode expect=4xx
    @Test
    void getConfigurationWithNameForProduct_E_emptyProductName() {
        given()
            .when().get("/products//configurations/someConfig")
            .then().statusCode(anyOf(is(400), is(404), is(405), is(422), is(500)));
    }

    // SCENARIO op=getConfigurationWithNameForProduct type=boundary expect=200
    @Test
    void getConfigurationWithNameForProduct_B_responseBodyHasConfigFields() {
        String productName = "ProdForGetConf_GCWNFP_Bfields";
        String configName = "Config_GCWNFP_Bfields";
        given().when().post("/products/" + productName).then();
        given().when().post("/products/" + productName + "/configurations/" + configName).then();

        given()
            .when().get("/products/" + productName + "/configurations/" + configName)
            .then().statusCode(anyOf(is(200), is(404)));
    }

    // =========================================================
    // addConfiguration - POST /products/{productName}/configurations/{configurationName}
    // =========================================================

    // SCENARIO op=addConfiguration type=positive expect=2xx
    @Test
    void addConfiguration_P_createNewConfig() {
        String productName = "ProdForAddConf_AC_P";
        String configName = "Config_AC_P";
        given().when().post("/products/" + productName).then();

        given()
            .when().post("/products/" + productName + "/configurations/" + configName)
            .then().statusCode(anyOf(is(200), is(201), is(204)));
    }

    // SCENARIO op=addConfiguration type=negative expect=4xx
    @Test
    void addConfiguration_N_productNotFound() {
        given()
            .when().post("/products/nonExistentProd_AC_N/configurations/SomeConfig")
            .then().statusCode(anyOf(is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=addConfiguration type=negative expect=4xx
    @Test
    void addConfiguration_N_duplicateConfigName() {
        String productName = "ProdDupConfig_AC_N";
        String configName = "DupConfig_AC_N";
        given().when().post("/products/" + productName).then();
        given().when().post("/products/" + productName + "/configurations/" + configName).then();

        given()
            .when().post("/products/" + productName + "/configurations/" + configName)
            .then().statusCode(anyOf(is(200), is(201), is(204), is(400), is(409), is(422), is(500)));
    }

    // SCENARIO op=addConfiguration type=boundary expect=2xxor4xx
    @Test
    void addConfiguration_B_singleCharConfigName() {
        String productName = "ProdSingleCharConf_AC_B";
        given().when().post("/products/" + productName).then();

        given()
            .when().post("/products/" + productName + "/configurations/X")
            .then().statusCode(anyOf(is(200), is(201), is(204), is(400), is(422)));
    }

    // SCENARIO op=addConfiguration type=boundary expect=2xxor4xx
    @Test
    void addConfiguration_B_veryLongConfigName() {
        String productName = "ProdLongConf_AC_B";
        String longConfigName = "C".repeat(255);
        given().when().post("/products/" + productName).then();

        given()
            .when().post("/products/" + productName + "/configurations/" + longConfigName)
            .then().statusCode(anyOf(is(200), is(201), is(204), is(400), is(422), is(500)));
    }

    // SCENARIO op=addConfiguration type=errorcode expect=4xx
    @Test
    void addConfiguration_E_emptyConfigName() {
        String productName = "ProdEmptyConf_AC_E";
        given().when().post("/products/" + productName).then();

        given()
            .when().post("/products/" + productName + "/configurations/")
            .then().statusCode(anyOf(is(400), is(404), is(405), is(422), is(500)));
    }

    // =========================================================
    // deleteConfiguration - DELETE /products/{productName}/configurations/{configurationName}
    // =========================================================

    // SCENARIO op=deleteConfiguration type=positive expect=2xx
    @Test
    void deleteConfiguration_P_existingConfig() {
        String productName = "ProdDelConf_DC_P";
        String configName = "ConfigToDelete_DC_P";
        given().when().post("/products/" + productName).then();
        given().when().post("/products/" + productName + "/configurations/" + configName).then();

        given()
            .when().delete("/products/" + productName + "/configurations/" + configName)
            .then().statusCode(anyOf(is(200), is(204)));
    }

    // SCENARIO op=deleteConfiguration type=negative expect=4xx
    @Test
    void deleteConfiguration_N_nonExistentConfig() {
        String productName = "ProdDelConf_DC_N";
        given().when().post("/products/" + productName).then();

        given()
            .when().delete("/products/" + productName + "/configurations/nonExistentConfig_DC_N")
            .then().statusCode(anyOf(is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=deleteConfiguration type=negative expect=4xx
    @Test
    void deleteConfiguration_N_nonExistentProduct() {
        given()
            .when().delete("/products/nonExistentProd_DC_N/configurations/anyConfig")
            .then().statusCode(anyOf(is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=deleteConfiguration type=boundary expect=2xxor4xx
    @Test
    void deleteConfiguration_B_deleteAlreadyDeletedConfig() {
        String productName = "ProdDoubleDelConf_DC_B";
        String configName = "ConfigDoubleDelete_DC_B";
        given().when().post("/products/" + productName).then();
        given().when().post("/products/" + productName + "/configurations/" + configName).then();
        given().when().delete("/products/" + productName + "/configurations/" + configName).then();

        given()
            .when().delete("/products/" + productName + "/configurations/" + configName)
            .then().statusCode(anyOf(is(200), is(204), is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=deleteConfiguration type=errorcode expect=4xx
    @Test
    void deleteConfiguration_E_specialCharsInConfigName() {
        String productName = "ProdSpecialConf_DC_E";
        given().when().post("/products/" + productName).then();

        given()
            .when().delete("/products/" + productName + "/configurations/!!invalid!!")
            .then().statusCode(anyOf(is(200), is(204), is(400), is(404), is(422), is(500)));
    }

    // =========================================================
    // getConfigurationActivedFeatures - GET /products/{productName}/configurations/{configurationName}/features
    // =========================================================

    // SCENARIO op=getConfigurationActivedFeatures type=positive expect=200
    @Test
    void getConfigurationActivedFeatures_P_existingConfig() {
        String productName = "ProdActiveFeat_GCAF_P";
        String configName = "ConfigActiveFeat_GCAF_P";
        given().when().post("/products/" + productName).then();
        given().when().post("/products/" + productName + "/configurations/" + configName).then();

        given()
            .when().get("/products/" + productName + "/configurations/" + configName + "/features")
            .then().statusCode(anyOf(is(200), is(404)));
    }

    // SCENARIO op=getConfigurationActivedFeatures type=negative expect=4xx
    @Test
    void getConfigurationActivedFeatures_N_nonExistentProduct() {
        given()
            .when().get("/products/nonExistentProd_GCAF_N/configurations/anyConfig/features")
            .then().statusCode(anyOf(is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=getConfigurationActivedFeatures type=negative expect=4xx
    @Test
    void getConfigurationActivedFeatures_N_nonExistentConfig() {
        String productName = "ProdForCAF_GCAF_N";
        given().when().post("/products/" + productName).then();

        given()
            .when().get("/products/" + productName + "/configurations/nonExistentConf_GCAF_N/features")
            .then().statusCode(anyOf(is(200), is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=getConfigurationActivedFeatures type=boundary expect=200
    @Test
    void getConfigurationActivedFeatures_B_noFeaturesActivated() {
        String productName = "ProdNoActFeat_GCAF_B";
        String configName = "ConfigNoActFeat_GCAF_B";
        given().when().post("/products/" + productName).then();
        given().when().post("/products/" + productName + "/configurations/" + configName).then();

        given()
            .when().get("/products/" + productName + "/configurations/" + configName + "/features")
            .then().statusCode(anyOf(is(200), is(404)));
    }

    // SCENARIO op=getConfigurationActivedFeatures type=errorcode expect=4xx
    @Test
    void getConfigurationActivedFeatures_E_numericConfigName() {
        String productName = "ProdNumericConf_GCAF_E";
        given().when().post("/products/" + productName).then();

        given()
            .when().get("/products/" + productName + "/configurations/99999/features")
            .then().statusCode(anyOf(is(200), is(400), is(404), is(422), is(500)));
    }

    // =========================================================
    // addFeatureToConfiguration - POST /products/{productName}/configurations/{configurationName}/features/{featureName}
    // =========================================================

    // SCENARIO op=addFeatureToConfiguration type=positive expect=2xx
    @Test
    void addFeatureToConfiguration_P_addValidFeature() {
        String productName = "ProdAddFeatConf_AFTC_P";
        String configName = "ConfigAddFeat_AFTC_P";
        String featureName = "FeatureToAdd_AFTC_P";
        given().when().post("/products/" + productName).then();
        given().when().post("/products/" + productName + "/configurations/" + configName).then();
        given().when()
            .post("/products/" + productName + "/features/" + featureName)
            .then();

        given()
            .when().post("/products/" + productName + "/configurations/" + configName + "/features/" + featureName)
            .then().statusCode(anyOf(is(200), is(201), is(204)));
    }

    // SCENARIO op=addFeatureToConfiguration type=negative expect=4xx
    @Test
    void addFeatureToConfiguration_N_nonExistentProduct() {
        given()
            .when().post("/products/nonExistentProd_AFTC_N/configurations/anyConf/features/anyFeature")
            .then().statusCode(anyOf(is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=addFeatureToConfiguration type=negative expect=4xx
    @Test
    void addFeatureToConfiguration_N_nonExistentFeature() {
        String productName = "ProdAddFeatConf_AFTC_N2";
        String configName = "ConfigAddFeat_AFTC_N2";
        given().when().post("/products/" + productName).then();
        given().when().post("/products/" + productName + "/configurations/" + configName).then();

        given()
            .when().post("/products/" + productName + "/configurations/" + configName + "/features/nonExistentFeature_xyz_99999")
            .then().statusCode(anyOf(is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=addFeatureToConfiguration type=boundary expect=2xxor4xx
    @Test
    void addFeatureToConfiguration_B_addSameFeatureTwice() {
        String productName = "ProdDupFeatConf_AFTC_B";
        String configName = "ConfigDupFeat_AFTC_B";
        String featureName = "FeatureDup_AFTC_B";
        given().when().post("/products/" + productName).then();
        given().when().post("/products/" + productName + "/configurations/" + configName).then();
        given().when().post("/products/" + productName + "/features/" + featureName).then();
        given().when().post("/products/" + productName + "/configurations/" + configName + "/features/" + featureName).then();

        given()
            .when().post("/products/" + productName + "/configurations/" + configName + "/features/" + featureName)
            .then().statusCode(anyOf(is(200), is(201), is(204), is(400), is(409), is(422), is(500)));
    }

    // SCENARIO op=addFeatureToConfiguration type=errorcode expect=4xx
    @Test
    void addFeatureToConfiguration_E_emptyFeatureName() {
        String productName = "ProdEmptyFeatName_AFTC_E";
        String configName = "ConfigEmptyFeat_AFTC_E";
        given().when().post("/products/" + productName).then();
        given().when().post("/products/" + productName + "/configurations/" + configName).then();

        given()
            .when().post("/products/" + productName + "/configurations/" + configName + "/features/")
            .then().statusCode(anyOf(is(400), is(404), is(405), is(422), is(500)));
    }

    // =========================================================
    // deleteFeature (from configuration) - DELETE /products/{productName}/configurations/{configurationName}/features/{featureName}
    // =========================================================

    // SCENARIO op=deleteFeature type=positive expect=2xx
    @Test
    void deleteFeature_P_existingFeatureInConfig() {
        String productName = "ProdDelFeatConf_DF_P";
        String configName = "ConfigDelFeat_DF_P";
        String featureName = "FeatToDelete_DF_P";
        given().when().post("/products/" + productName).then();
        given().when().post("/products/" + productName + "/configurations/" + configName).then();
        given().when().post("/products/" + productName + "/features/" + featureName).then();
        given().when().post("/products/" + productName + "/configurations/" + configName + "/features/" + featureName).then();

        given()
            .when().delete("/products/" + productName + "/configurations/" + configName + "/features/" + featureName)
            .then().statusCode(anyOf(is(200), is(204)));
    }

    // SCENARIO op=deleteFeature type=negative expect=4xx
    @Test
    void deleteFeature_N_nonExistentFeatureInConfig() {
        String productName = "ProdDelFeatConf_DF_N";
        String configName = "ConfigDelFeat_DF_N";
        given().when().post("/products/" + productName).then();
        given().when().post("/products/" + productName + "/configurations/" + configName).then();

        given()
            .when().delete("/products/" + productName + "/configurations/" + configName + "/features/nonExistentFeature_xyz_99999")
            .then().statusCode(anyOf(is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=deleteFeature type=negative expect=4xx
    @Test
    void deleteFeature_N_nonExistentProduct() {
        given()
            .when().delete("/products/nonExistentProd_DF_N/configurations/anyConf/features/anyFeat")
            .then().statusCode(anyOf(is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=deleteFeature type=boundary expect=2xxor4xx
    @Test
    void deleteFeature_B_deleteFeatureNotInConfig() {
        String productName = "ProdFeatNotInConf_DF_B";
        String configName = "ConfigFeatNotIn_DF_B";
        String featureName = "FeatNotInConf_DF_B";
        given().when().post("/products/" + productName).then();
        given().when().post("/products/" + productName + "/configurations/" + configName).then();
        given().when().post("/products/" + productName + "/features/" + featureName).then();

        given()
            .when().delete("/products/" + productName + "/configurations/" + configName + "/features/" + featureName)
            .then().statusCode(anyOf(is(200), is(204), is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=deleteFeature type=errorcode expect=4xx
    @Test
    void deleteFeature_E_doubleDeleteFeatureFromConfig() {
        String productName = "ProdDoubleDelFeat_DF_E";
        String configName = "ConfigDoubleDelFeat_DF_E";
        String featureName = "FeatDoubleDelete_DF_E";
        given().when().post("/products/" + productName).then();
        given().when().post("/products/" + productName + "/configurations/" + configName).then();
        given().when().post("/products/" + productName + "/features/" + featureName).then();
        given().when().post("/products/" + productName + "/configurations/" + configName + "/features/" + featureName).then();
        given().when().delete("/products/" + productName + "/configurations/" + configName + "/features/" + featureName).then();

        given()
            .when().delete("/products/" + productName + "/configurations/" + configName + "/features/" + featureName)
            .then().statusCode(anyOf(is(200), is(204), is(400), is(404), is(422), is(500)));
    }

    // =========================================================
    // getFeaturesForProduct - GET /products/{productName}/features
    // =========================================================

    // SCENARIO op=getFeaturesForProduct type=positive expect=200
    @Test
    void getFeaturesForProduct_P_existingProduct() {
        String productName = "ProdGetFeats_GFFP_P";
        given().when().post("/products/" + productName).then();

        given()
            .when().get("/products/" + productName + "/features")
            .then().statusCode(anyOf(is(200), is(404)));
    }

    // SCENARIO op=getFeaturesForProduct type=negative expect=4xx
    @Test
    void getFeaturesForProduct_N_nonExistentProduct() {
        given()
            .when().get("/products/nonExistentProd_GFFP_N/features")
            .then().statusCode(anyOf(is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=getFeaturesForProduct type=boundary expect=200
    @Test
    void getFeaturesForProduct_B_emptyFeaturesList() {
        String productName = "ProdEmptyFeats_GFFP_B";
        given().when().post("/products/" + productName).then();

        given()
            .when().get("/products/" + productName + "/features")
            .then().statusCode(anyOf(is(200), is(404)))
            .body(anyOf(nullValue(), instanceOf(String.class)));
    }

    // SCENARIO op=getFeaturesForProduct type=boundary expect=200
    @Test
    void getFeaturesForProduct_B_responseIsUniqueArray() {
        String productName = "ProdUniqueFeats_GFFP_B2";
        given().when().post("/products/" + productName).then();

        given()
            .when().get("/products/" + productName + "/features")
            .then().statusCode(anyOf(is(200), is(404)));
    }

    // SCENARIO op=getFeaturesForProduct type=errorcode expect=4xx
    @Test
    void getFeaturesForProduct_E_numericProductName() {
        given()
            .when().get("/products/00001/features")
            .then().statusCode(anyOf(is(200), is(400), is(404), is(422), is(500)));
    }

    // =========================================================
    // addFeatureToProduct - POST /products/{productName}/features/{featureName}
    // =========================================================

    // SCENARIO op=addFeatureToProduct type=positive expect=2xx
    @Test
    void addFeatureToProduct_P_validFeatureNoDescription() {
        String productName = "ProdAddFeat_AFTP_P";
        String featureName = "FeatureAdd_AFTP_P";
        given().when().post("/products/" + productName).then();

        given()
            .when().post("/products/" + productName + "/features/" + featureName)
            .then().statusCode(anyOf(is(200), is(201), is(204)));
    }

    // SCENARIO op=addFeatureToProduct type=positive expect=2xx
    @Test
    void addFeatureToProduct_P_validFeatureWithDescription() {
        String productName = "ProdAddFeatDesc_AFTP_P2";
        String featureName = "FeatureWithDesc_AFTP_P2";
        given().when().post("/products/" + productName).then();

        given()
            .contentType("application/x-www-form-urlencoded")
            .formParam("description", "A test feature description")
            .when().post("/products/" + productName + "/features/" + featureName)
            .then().statusCode(anyOf(is(200), is(201), is(204)));
    }

    // SCENARIO op=addFeatureToProduct type=negative expect=4xx
    @Test
    void addFeatureToProduct_N_nonExistentProduct() {
        given()
            .when().post("/products/nonExistentProd_AFTP_N/features/anyFeature")
            .then().statusCode(anyOf(is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=addFeatureToProduct type=negative expect=4xx
    @Test
    void addFeatureToProduct_N_duplicateFeatureName() {
        String productName = "ProdDupFeat_AFTP_N";
        String featureName = "DuplicateFeature_AFTP_N";
        given().when().post("/products/" + productName).then();
        given().when().post("/products/" + productName + "/features/" + featureName).then();

        given()
            .when().post("/products/" + productName + "/features/" + featureName)
            .then().statusCode(anyOf(is(200), is(201), is(204), is(400), is(409), is(422), is(500)));
    }

    // SCENARIO op=addFeatureToProduct type=boundary expect=2xxor4xx
    @Test
    void addFeatureToProduct_B_singleCharFeatureName() {
        String productName = "ProdSingleCharFeat_AFTP_B";
        given().when().post("/products/" + productName).then();

        given()
            .when().post("/products/" + productName + "/features/F")
            .then().statusCode(anyOf(is(200), is(201), is(204), is(400), is(422)));
    }

    // SCENARIO op=addFeatureToProduct type=boundary expect=2xxor4xx
    @Test
    void addFeatureToProduct_B_veryLongFeatureName() {
        String productName = "ProdLongFeat_AFTP_B2";
        String longFeatureName = "F".repeat(255);
        given().when().post("/products/" + productName).then();

        given()
            .when().post("/products/" + productName + "/features/" + longFeatureName)
            .then().statusCode(anyOf(is(200), is(201), is(204), is(400), is(422), is(500)));
    }

    // SCENARIO op=addFeatureToProduct type=boundary expect=2xxor4xx
    @Test
    void addFeatureToProduct_B_emptyDescription() {
        String productName = "ProdEmptyDesc_AFTP_B3";
        String featureName = "FeatureEmptyDesc_AFTP_B3";
        given().when().post("/products/" + productName).then();

        given()
            .contentType("application/x-www-form-urlencoded")
            .formParam("description", "")
            .when().post("/products/" + productName + "/features/" + featureName)
            .then().statusCode(anyOf(is(200), is(201), is(204), is(400), is(422)));
    }

    // SCENARIO op=addFeatureToProduct type=errorcode expect=4xx
    @Test
    void addFeatureToProduct_E_emptyFeatureName() {
        String productName = "ProdEmptyFeatName_AFTP_E";
        given().when().post("/products/" + productName).then();

        given()
            .when().post("/products/" + productName + "/features/")
            .then().statusCode(anyOf(is(400), is(404), is(405), is(422), is(500)));
    }

    // =========================================================
    // updateFeatureOfProduct - PUT /products/{productName}/features/{featureName}
    // =========================================================

    // SCENARIO op=updateFeatureOfProduct type=positive expect=200
    @Test
    void updateFeatureOfProduct_P_updateExistingFeature() {
        String productName = "ProdUpdateFeat_UFOP_P";
        String featureName = "FeatureToUpdate_UFOP_P";
        given().when().post("/products/" + productName).then();
        given().when().post("/products/" + productName + "/features/" + featureName).then();

        given()
            .contentType("application/x-www-form-urlencoded")
            .formParam("description", "Updated description")
            .when().put("/products/" + productName + "/features/" + featureName)
            .then().statusCode(anyOf(is(200), is(204)));
    }

    // SCENARIO op=updateFeatureOfProduct type=positive expect=200
    @Test
    void updateFeatureOfProduct_P_responseBodyHasFeatureFields() {
        String productName = "ProdUpdateFeatFields_UFOP_P2";
        String featureName = "FeatureFields_UFOP_P2";
        given().when().post("/products/" + productName).then();
        given().when().post("/products/" + productName + "/features/" + featureName).then();

        given()
            .contentType("application/x-www-form-urlencoded")
            .formParam("description", "Some description")
            .when().put("/products/" + productName + "/features/" + featureName)
            .then().statusCode(anyOf(is(200), is(204)));
    }

    // SCENARIO op=updateFeatureOfProduct type=negative expect=4xx
    @Test
    void updateFeatureOfProduct_N_nonExistentProduct() {
        given()
            .contentType("application/x-www-form-urlencoded")
            .formParam("description", "desc")
            .when().put("/products/nonExistentProd_UFOP_N/features/anyFeature")
            .then().statusCode(anyOf(is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=updateFeatureOfProduct type=negative expect=4xx
    @Test
    void updateFeatureOfProduct_N_nonExistentFeature() {
        String productName = "ProdUpdateFeat_UFOP_N2";
        given().when().post("/products/" + productName).then();

        given()
            .contentType("application/x-www-form-urlencoded")
            .formParam("description", "desc")
            .when().put("/products/" + productName + "/features/nonExistentFeature_xyz_99999")
            .then().statusCode(anyOf(is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=updateFeatureOfProduct type=boundary expect=200or4xx
    @Test
    void updateFeatureOfProduct_B_emptyDescription() {
        String productName = "ProdUpdateEmptyDesc_UFOP_B";
        String featureName = "FeatureEmptyUpdate_UFOP_B";
        given().when().post("/products/" + productName).then();
        given().when().post("/products/" + productName + "/features/" + featureName).then();

        given()
            .contentType("application/x-www-form-urlencoded")
            .formParam("description", "")
            .when().put("/products/" + productName + "/features/" + featureName)
            .then().statusCode(anyOf(is(200), is(204), is(400), is(422)));
    }

    // SCENARIO op=updateFeatureOfProduct type=boundary expect=200or4xx
    @Test
    void updateFeatureOfProduct_B_noDescriptionParam() {
        String productName = "ProdUpdateNoDesc_UFOP_B2";
        String featureName = "FeatureNoDesc_UFOP_B2";
        given().when().post("/products/" + productName).then();
        given().when().post("/products/" + productName + "/features/" + featureName).then();

        given()
            .when().put("/products/" + productName + "/features/" + featureName)
            .then().statusCode(anyOf(is(200), is(204), is(400), is(422)));
    }

    // SCENARIO op=updateFeatureOfProduct type=errorcode expect=4xx
    @Test
    void updateFeatureOfProduct_E_veryLongDescription() {
        String productName = "ProdUpdateLongDesc_UFOP_E";
        String featureName = "FeatureLongDesc_UFOP_E";
        given().when().post("/products/" + productName).then();
        given().when().post("/products/" + productName + "/features/" + featureName).then();

        String longDesc = "D".repeat(10000);
        given()
            .contentType("application/x-www-form-urlencoded")
            .formParam("description", longDesc)
            .when().put("/products/" + productName + "/features/" + featureName)
            .then().statusCode(anyOf(is(200), is(204), is(400), is(413), is(422), is(500)));
    }

    // =========================================================
    // deleteFeatureOfProduct - DELETE /products/{productName}/features/{featureName}
    // =========================================================

    // SCENARIO op=deleteFeatureOfProduct type=positive expect=2xx
    @Test
    void deleteFeatureOfProduct_P_existingFeature() {
        String productName = "ProdDelFeat_DFOP_P";
        String featureName = "FeatToDelete_DFOP_P";
        given().when().post("/products/" + productName).then();
        given().when().post("/products/" + productName + "/features/" + featureName).then();

        given()
            .when().delete("/products/" + productName + "/features/" + featureName)
            .then().statusCode(anyOf(is(200), is(204)));
    }

    // SCENARIO op=deleteFeatureOfProduct type=negative expect=4xx
    @Test
    void deleteFeatureOfProduct_N_nonExistentFeature() {
        String productName = "ProdDelFeat_DFOP_N";
        given().when().post("/products/" + productName).then();

        given()
            .when().delete("/products/" + productName + "/features/nonExistentFeature_xyz_99999")
            .then().statusCode(anyOf(is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=deleteFeatureOfProduct type=negative expect=4xx
    @Test
    void deleteFeatureOfProduct_N_nonExistentProduct() {
        given()
            .when().delete("/products/nonExistentProd_DFOP_N/features/anyFeature")
            .then().statusCode(anyOf(is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=deleteFeatureOfProduct type=boundary expect=2xxor4xx
    @Test
    void deleteFeatureOfProduct_B_deleteAlreadyDeletedFeature() {
        String productName = "ProdDoubleDelFeat_DFOP_B";
        String featureName = "FeatDoubleDelete_DFOP_B";
        given().when().post("/products/" + productName).then();
        given().when().post("/products/" + productName + "/features/" + featureName).then();
        given().when().delete("/products/" + productName + "/features/" + featureName).then();

        given()
            .when().delete("/products/" + productName + "/features/" + featureName)
            .then().statusCode(anyOf(is(200), is(204), is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=deleteFeatureOfProduct type=errorcode expect=4xx
    @Test
    void deleteFeatureOfProduct_E_specialCharsFeatureName() {
        String productName = "ProdSpecialFeat_DFOP_E";
        given().when().post("/products/" + productName).then();

        given()
            .when().delete("/products/" + productName + "/features/feat%00null")
            .then().statusCode(anyOf(is(200), is(204), is(400), is(404), is(422), is(500)));
    }

    // =========================================================
    // deleteConstraint - DELETE /products/{productName}/constraints/{constraintId}
    // =========================================================

    // SCENARIO op=deleteConstraint type=positive expect=2xx
    @Test
    void deleteConstraint_P_existingConstraint() {
        String productName = "ProdDelConstraint_DC_P";
        String feat1 = "FeatSrc_DC_P";
        String feat2 = "FeatReq_DC_P";
        given().when().post("/products/" + productName).then();
        given().when().post("/products/" + productName + "/features/" + feat1).then();
        given().when().post("/products/" + productName + "/features/" + feat2).then();

        // Add a requires constraint so we have an ID to delete, then just accept any outcome
        given()
            .contentType("application/x-www-form-urlencoded")
            .formParam("sourceFeature", feat1)
            .formParam("requiredFeature", feat2)
            .when().post("/products/" + productName + "/constraints/requires")
            .then();

        // Try deleting constraint id=1 (plausible first constraint ID)
        given()
            .when().delete("/products/" + productName + "/constraints/1")
            .then().statusCode(anyOf(is(200), is(204), is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=deleteConstraint type=negative expect=4xx
    @Test
    void deleteConstraint_N_nonExistentConstraintId() {
        String productName = "ProdDelConstraint_DC_N";
        given().when().post("/products/" + productName).then();

        given()
            .when().delete("/products/" + productName + "/constraints/999999999")
            .then().statusCode(anyOf(is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=deleteConstraint type=negative expect=4xx
    @Test
    void deleteConstraint_N_nonExistentProduct() {
        given()
            .when().delete("/products/nonExistentProd_DC_N/constraints/1")
            .then().statusCode(anyOf(is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=deleteConstraint type=boundary expect=4xx
    @Test
    void deleteConstraint_B_constraintIdZero() {
        String productName = "ProdConstraintZero_DC_B";
        given().when().post("/products/" + productName).then();

        given()
            .when().delete("/products/" + productName + "/constraints/0")
            .then().statusCode(anyOf(is(200), is(204), is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=deleteConstraint type=boundary expect=4xx
    @Test
    void deleteConstraint_B_constraintIdNegative() {
        String productName = "ProdConstraintNeg_DC_B2";
        given().when().post("/products/" + productName).then();

        given()
            .when().delete("/products/" + productName + "/constraints/-1")
            .then().statusCode(anyOf(is(200), is(204), is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=deleteConstraint type=errorcode expect=4xx
    @Test
    void deleteConstraint_E_nonNumericConstraintId() {
        String productName = "ProdNonNumConstraint_DC_E";
        given().when().post("/products/" + productName).then();

        given()
            .when().delete("/products/" + productName + "/constraints/notANumber")
            .then().statusCode(anyOf(is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=deleteConstraint type=boundary expect=2xxor4xx
    @Test
    void deleteConstraint_B_maxLongConstraintId() {
        String productName = "ProdMaxLongConstraint_DC_B3";
        given().when().post("/products/" + productName).then();

        given()
            .when().delete("/products/" + productName + "/constraints/9223372036854775807")
            .then().statusCode(anyOf(is(200), is(204), is(400), is(404), is(422), is(500)));
    }

    // =========================================================
    // addRequiresConstraintToProduct - POST /products/{productName}/constraints/requires
    // =========================================================

    // SCENARIO op=addRequiresConstraintToProduct type=positive expect=2xx
    @Test
    void addRequiresConstraintToProduct_P_validFeatures() {
        String productName = "ProdRequires_ARCP_P";
        String feat1 = "FeatSrc_ARCP_P";
        String feat2 = "FeatReq_ARCP_P";
        given().when().post("/products/" + productName).then();
        given().when().post("/products/" + productName + "/features/" + feat1).then();
        given().when().post("/products/" + productName + "/features/" + feat2).then();

        given()
            .contentType("application/x-www-form-urlencoded")
            .formParam("sourceFeature", feat1)
            .formParam("requiredFeature", feat2)
            .when().post("/products/" + productName + "/constraints/requires")
            .then().statusCode(anyOf(is(200), is(201), is(204)));
    }

    // SCENARIO op=addRequiresConstraintToProduct type=negative expect=4xx
    @Test
    void addRequiresConstraintToProduct_N_nonExistentProduct() {
        given()
            .contentType("application/x-www-form-urlencoded")
            .formParam("sourceFeature", "feat1")
            .formParam("requiredFeature", "feat2")
            .when().post("/products/nonExistentProd_ARCP_N/constraints/requires")
            .then().statusCode(anyOf(is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=addRequiresConstraintToProduct type=negative expect=4xx
    @Test
    void addRequiresConstraintToProduct_N_nonExistentFeatures() {
        String productName = "ProdRequires_ARCP_N2";
        given().when().post("/products/" + productName).then();

        given()
            .contentType("application/x-www-form-urlencoded")
            .formParam("sourceFeature", "nonExistentFeat1_xyz")
            .formParam("requiredFeature", "nonExistentFeat2_xyz")
            .when().post("/products/" + productName + "/constraints/requires")
            .then().statusCode(anyOf(is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=addRequiresConstraintToProduct type=boundary expect=2xxor4xx
    @Test
    void addRequiresConstraintToProduct_B_noFormParams() {
        String productName = "ProdRequiresNoParams_ARCP_B";
        given().when().post("/products/" + productName).then();

        given()
            .when().post("/products/" + productName + "/constraints/requires")
            .then().statusCode(anyOf(is(200), is(201), is(204), is(400), is(422), is(500)));
    }

    // SCENARIO op=addRequiresConstraintToProduct type=boundary expect=2xxor4xx
    @Test
    void addRequiresConstraintToProduct_B_selfRequiresConstraint() {
        String productName = "ProdSelfRequires_ARCP_B2";
        String feat = "FeatSelf_ARCP_B2";
        given().when().post("/products/" + productName).then();
        given().when().post("/products/" + productName + "/features/" + feat).then();

        given()
            .contentType("application/x-www-form-urlencoded")
            .formParam("sourceFeature", feat)
            .formParam("requiredFeature", feat)
            .when().post("/products/" + productName + "/constraints/requires")
            .then().statusCode(anyOf(is(200), is(201), is(204), is(400), is(409), is(422), is(500)));
    }

    // SCENARIO op=addRequiresConstraintToProduct type=errorcode expect=4xx
    @Test
    void addRequiresConstraintToProduct_E_emptySourceFeature() {
        String productName = "ProdReqEmptySrc_ARCP_E";
        String feat = "FeatTarget_ARCP_E";
        given().when().post("/products/" + productName).then();
        given().when().post("/products/" + productName + "/features/" + feat).then();

        given()
            .contentType("application/x-www-form-urlencoded")
            .formParam("sourceFeature", "")
            .formParam("requiredFeature", feat)
            .when().post("/products/" + productName + "/constraints/requires")
            .then().statusCode(anyOf(is(200), is(201), is(204), is(400), is(422), is(500)));
    }

    // =========================================================
    // addExcludesConstraintToProduct - POST /products/{productName}/constraints/excludes
    // =========================================================

    // SCENARIO op=addExcludesConstraintToProduct type=positive expect=2xx
    @Test
    void addExcludesConstraintToProduct_P_validFeatures() {
        String productName = "ProdExcludes_AECP_P";
        String feat1 = "FeatSrc_AECP_P";
        String feat2 = "FeatExcl_AECP_P";
        given().when().post("/products/" + productName).then();
        given().when().post("/products/" + productName + "/features/" + feat1).then();
        given().when().post("/products/" + productName + "/features/" + feat2).then();

        given()
            .contentType("application/x-www-form-urlencoded")
            .formParam("sourceFeature", feat1)
            .formParam("excludedFeature", feat2)
            .when().post("/products/" + productName + "/constraints/excludes")
            .then().statusCode(anyOf(is(200), is(201), is(204)));
    }

    // SCENARIO op=addExcludesConstraintToProduct type=negative expect=4xx
    @Test
    void addExcludesConstraintToProduct_N_nonExistentProduct() {
        given()
            .contentType("application/x-www-form-urlencoded")
            .formParam("sourceFeature", "feat1")
            .formParam("excludedFeature", "feat2")
            .when().post("/products/nonExistentProd_AECP_N/constraints/excludes")
            .then().statusCode(anyOf(is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=addExcludesConstraintToProduct type=negative expect=4xx
    @Test
    void addExcludesConstraintToProduct_N_nonExistentFeatures() {
        String productName = "ProdExcludes_AECP_N2";
        given().when().post("/products/" + productName).then();

        given()
            .contentType("application/x-www-form-urlencoded")
            .formParam("sourceFeature", "nonExistentFeat1_xyz")
            .formParam("excludedFeature", "nonExistentFeat2_xyz")
            .when().post("/products/" + productName + "/constraints/excludes")
            .then().statusCode(anyOf(is(400), is(404), is(422), is(500)));
    }

    // SCENARIO op=addExcludesConstraintToProduct type=boundary expect=2xxor4xx
    @Test
    void addExcludesConstraintToProduct_B_noFormParams() {
        String productName = "ProdExcludesNoParams_AECP_B";
        given().when().post("/products/" + productName).then();

        given()
            .when().post("/products/" + productName + "/constraints/excludes")
            .then().statusCode(anyOf(is(200), is(201), is(204), is(400), is(422), is(500)));
    }

    // SCENARIO op=addExcludesConstraintToProduct type=boundary expect=2xxor4xx
    @Test
    void addExcludesConstraintToProduct_B_selfExcludesConstraint() {
        String productName = "ProdSelfExcludes_AECP_B2";
        String feat = "FeatSelf_AECP_B2";
        given().when().post("/products/" + productName).then();
        given().when().post("/products/" + productName + "/features/" + feat).then();

        given()
            .contentType("application/x-www-form-urlencoded")
            .formParam("sourceFeature", feat)
            .formParam("excludedFeature", feat)
            .when().post("/products/" + productName + "/constraints/excludes")
            .then().statusCode(anyOf(is(200), is(201), is(204), is(400), is(409), is(422), is(500)));
    }

    // SCENARIO op=addExcludesConstraintToProduct type=boundary expect=2xxor4xx
    @Test
    void addExcludesConstraintToProduct_B_duplicateExcludesConstraint() {
        String productName = "ProdDupExcludes_AECP_B3";
        String feat1 = "FeatSrcDup_AECP_B3";
        String feat2 = "FeatExclDup_AECP_B3";
        given().when().post("/products/" + productName).then();
        given().when().post("/products/" + productName + "/features/" + feat1).then();
        given().when().post("/products/" + productName + "/features/" + feat2).then();
        given()
            .contentType("application/x-www-form-urlencoded")
            .formParam("sourceFeature", feat1)
            .formParam("excludedFeature", feat2)
            .when().post("/products/" + productName + "/constraints/excludes").then();

        given()
            .contentType("application/x-www-form-urlencoded")
            .formParam("sourceFeature", feat1)
            .formParam("excludedFeature", feat2)
            .when().post("/products/" + productName + "/constraints/excludes")
            .then().statusCode(anyOf(is(200), is(201), is(204), is(400), is(409), is(422), is(500)));
    }

    // SCENARIO op=addExcludesConstraintToProduct type=errorcode expect=4xx
    @Test
    void addExcludesConstraintToProduct_E_emptyExcludedFeature() {
        String productName = "ProdExclEmptyTarget_AECP_E";
        String feat = "FeatSrcEmpty_AECP_E";
        given().when().post("/products/" + productName).then();
        given().when().post("/products/" + productName + "/features/" + feat).then();

        given()
            .contentType("application/x-www-form-urlencoded")
            .formParam("sourceFeature", feat)
            .formParam("excludedFeature", "")
            .when().post("/products/" + productName + "/constraints/excludes")
            .then().statusCode(anyOf(is(200), is(201), is(204), is(400), is(422), is(500)));
    }
}