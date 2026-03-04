import "./globals.css";

export const metadata = {
    title: "Zoiris Cleaning Services",
    description: "Top-Rated Cleaning Services in Alabama",
};

export default function RootLayout({
    children,
}: {
    children: React.ReactNode;
}) {
    return (
        <html lang="en">
            <body>{children}</body>
        </html>
    );
}
