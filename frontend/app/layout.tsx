import "./globals.css";

import { Providers } from "@/app/providers";

export const metadata = {
  title: "Tyre Industry Intelligence Platform",
  description: "Sentiment, trends, topics, alerts, and AI insights for tyre brands."
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
