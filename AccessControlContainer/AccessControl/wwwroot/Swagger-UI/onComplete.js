if (window.sessionStorage.token) {
    key = "Bearer " + window.sessionStorage.token;
    swaggerUi.api.clientAuthorizations.add("key", new SwaggerClient.ApiKeyAuthorization("Authorization", key, "header"));
}
