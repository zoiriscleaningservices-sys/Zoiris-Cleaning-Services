import PageTemplate from "../../../components/PageTemplate";

export default async function ServicePage({ params }: { params: Promise<{ location: string, service: string }> }) {
    // Extract params
    const resolvedParams = await params;
    const locationParts = resolvedParams.location.split("-");
    const state = locationParts.pop()?.toUpperCase() || "AL";
    const city = locationParts.map((p) => p.charAt(0).toUpperCase() + p.slice(1)).join(" ");

    // Format service URL
    const formattedService = resolvedParams.service
        .split("-")
        .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
        .join(" ");

    return <PageTemplate city={city} state={state} service={formattedService} />;
}
