"use client";

import { SummaryItem } from "@/lib/types";

export function SentimentTable({ items }: { items: SummaryItem[] }) {
  return (
    <div className="panel overflow-hidden">
      <div className="mb-4 flex items-center justify-between">
        <div>
          <p className="text-sm uppercase tracking-[0.3em] text-slate-500">Section 1</p>
          <h2 className="text-2xl font-semibold">Sentiment Summary Table</h2>
        </div>
      </div>
      <div className="overflow-x-auto">
        <table className="min-w-full text-sm">
          <thead>
            <tr className="border-b border-slate-200 text-left text-slate-500">
              <th className="py-3">Brand</th>
              <th className="py-3">Articles</th>
              <th className="py-3">Positive</th>
              <th className="py-3">Neutral</th>
              <th className="py-3">Negative</th>
              <th className="py-3">Score</th>
            </tr>
          </thead>
          <tbody>
            {items.map((item) => (
              <tr key={item.brand} className="border-b border-slate-100">
                <td className="py-3 font-semibold">{item.brand}</td>
                <td>{item.articles}</td>
                <td className="text-emerald-600">{item.positive}</td>
                <td className="text-amber-600">{item.neutral}</td>
                <td className="text-rose-600">{item.negative}</td>
                <td>{item.score.toFixed(2)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
