import PageTemplate from "../../components/PageTemplate";

export default async function LocationPage({ params }: { params: Promise<{ location: string }> }) {
    const resolvedParams = await params;
    const locationParts = resolvedParams.location.split("-");
    const state = locationParts.pop()?.toUpperCase() || "AL";
    const city = locationParts.map((p) => p.charAt(0).toUpperCase() + p.slice(1)).join(" ");

    return <PageTemplate city={city} state={state} service="Cleaning Service" />;
}
