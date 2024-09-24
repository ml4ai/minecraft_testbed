FROM mcr.microsoft.com/dotnet/core/aspnet:2.2 AS runtime
WORKDIR /app
COPY DashboardService/. .

ENTRYPOINT ["dotnet", "asa.services.dashboardservice.dll"]

