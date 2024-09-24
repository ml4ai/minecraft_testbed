FROM mcr.microsoft.com/dotnet/core/sdk:3.1 AS build-env
WORKDIR /app

ARG CACHE_BREAKER
# Copy csproj and restore as distinct layers
COPY  NuGet.config ./
COPY src/MQTTValidationService.sln ./
COPY src/MQTTValidationService/MQTTValidationService.csproj ./MQTTValidationService/MQTTValidationService.csproj
COPY src/ValidationServices/ValidationServices.csproj ./ValidationServices/ValidationServices.csproj
COPY src/LogFileValidator/LogFileValidator.csproj ./LogFileValidator/LogFileValidator.csproj
RUN dotnet restore

COPY src/MQTTValidationService ./MQTTValidationService
COPY src/ValidationServices ./ValidationServices
COPY src/LogFileValidator ./LogFileValidator
RUN dotnet publish -c Release -o out MQTTValidationService/MQTTValidationService.csproj

# Build runtime image
FROM mcr.microsoft.com/dotnet/core/aspnet:2.1
WORKDIR /app
COPY --from=build-env /app/out .
COPY ./src/MQTTValidationService/cert-aspnetcore.pfx .
ENTRYPOINT ["dotnet", "MQTTValidationService.dll"]

