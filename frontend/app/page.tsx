"use client";

import { useQuery } from "@tanstack/react-query";
import { useState } from "react";

import { ArticleFeed } from "@/components/ArticleFeed";
import { InsightsPanel } from "@/components/InsightsPanel";
import { SentimentTable } from "@/components/SentimentTable";
import { TopicChart } from "@/components/TopicChart";
import { TrendChart } from "@/components/TrendChart";
import { fetchAlerts, fetchInsights, fetchSummary, fetchTrends } from "@/lib/api";

export default function HomePage() {
  const [brand, setBrand] = useState("");
  const [sentiment, setSentiment] = useState("");
  const [topic, setTopic] = useState("");

  const summaryQuery = useQuery({ queryKey: ["summary"], queryFn: fetchSummary });
  const trendsQuery = useQuery({ queryKey: ["trends"], queryFn: fetchTrends });
  const insightsQuery = useQuery({ queryKey: ["insights"], queryFn: fetchInsights });
  const alertsQuery = useQuery({ queryKey: ["alerts"], queryFn: fetchAlerts });

  return (
    <main className="mx-auto flex min-h-screen max-w-7xl flex-col gap-8 px-6 py-10">
      <header className="overflow-hidden rounded-[2rem] border border-slate-700/60 bg-gradient-to-br from-slate-950 via-slate-900 to-slate-800 p-8 text-white shadow-panel">
        <p className="text-sm uppercase tracking-[0.4em] text-orange-200">Anupriyo Mandal&apos;s Intelligence Platform</p>
        <div className="mt-4 flex flex-col gap-6 lg:flex-row lg:items-end lg:justify-between">
          <div>
            <h1 className="text-4xl font-semibold">Tyre Brand Sentiment Dashboard</h1>
            <p className="mt-3 max-w-2xl text-sm leading-6 text-slate-300">
              Live brand monitoring across sentiment, trend tracking, topic intelligence, AI insights, alerts,
              and an infinite article feed.
            </p>
          </div>
          <div className="grid gap-3 sm:grid-cols-3">
            <select value={brand} onChange={(e) => setBrand(e.target.value)} className="rounded-2xl border border-white/15 bg-white/10 px-4 py-3 text-sm text-white">
              <option value="">All brands</option>
              <option value="CEAT">CEAT</option>
              <option value="MRF">MRF</option>
              <option value="Apollo">Apollo</option>
              <option value="TVS">TVS</option>
              <option value="JK">JK</option>
            </select>
            <select value={sentiment} onChange={(e) => setSentiment(e.target.value)} className="rounded-2xl border border-white/15 bg-white/10 px-4 py-3 text-sm text-white">
              <option value="">All sentiments</option>
              <option value="Positive">Positive</option>
              <option value="Neutral">Neutral</option>
              <option value="Negative">Negative</option>
            </select>
            <select value={topic} onChange={(e) => setTopic(e.target.value)} className="rounded-2xl border border-white/15 bg-white/10 px-4 py-3 text-sm text-white">
              <option value="">All topics</option>
              <option value="Product Launch">Product Launch</option>
              <option value="Earnings">Earnings</option>
              <option value="Exports">Exports</option>
              <option value="Market Expansion">Market Expansion</option>
              <option value="Cost Pressure">Cost Pressure</option>
              <option value="EV Tyres">EV Tyres</option>
              <option value="Regulation">Regulation</option>
              <option value="Other">Other</option>
            </select>
          </div>
        </div>
        <div className="mt-6 flex flex-wrap gap-3">
          {alertsQuery.data?.filter((item) => item.triggered).map((alert) => (
            <div key={alert.brand} className="rounded-full border border-rose-400/30 bg-rose-500/20 px-4 py-2 text-sm text-rose-50">
              Alert: {alert.brand} negative coverage at {(alert.negative_ratio * 100).toFixed(0)}%
            </div>
          ))}
        </div>
      </header>

      {summaryQuery.data && <SentimentTable items={summaryQuery.data} />}

      <section className="grid gap-8 lg:grid-cols-[1.4fr_1fr]">
        {trendsQuery.data && <TrendChart data={trendsQuery.data} />}
        {insightsQuery.data && <InsightsPanel insights={insightsQuery.data.insights} />}
      </section>

      {trendsQuery.data && <TopicChart data={trendsQuery.data.topics} />}
      <ArticleFeed filters={{ brand, sentiment, topic }} />
    </main>
  );
}
