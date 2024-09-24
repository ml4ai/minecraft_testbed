FROM mcr.microsoft.com/dotnet/core/sdk:2.1 AS build-env
WORKDIR /app

ARG CACHE_BREAKER
# Copy csproj and restore as distinct layers
COPY  NuGet.config ./
COPY src/AsistDataIngester.sln ./
COPY src/AsistDataIngester/AsistDataIngester.csproj ./AsistDataIngester/AsistDataIngester.csproj
RUN dotnet restore

COPY src/AsistDataIngester ./AsistDataIngester
RUN dotnet publish -c Release -o out

# Build runtime image
FROM mcr.microsoft.com/dotnet/core/aspnet:2.1
WORKDIR /app
COPY --from=build-env /app/AsistDataIngester/out .
COPY ./src/AsistDataIngester/cert-aspnetcore.pfx .
ENTRYPOINT ["dotnet", "AsistDataIngester.dll"]

