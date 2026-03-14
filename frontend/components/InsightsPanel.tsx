"use client";

export function InsightsPanel({ insights }: { insights: string[] }) {
  return (
    <div className="panel">
      <p className="text-sm uppercase tracking-[0.3em] text-slate-500">Section 4</p>
      <h2 className="mb-4 text-2xl font-semibold">Market Insights</h2>
      <div className="space-y-3">
        {insights.map((insight) => (
          <div key={insight} className="rounded-2xl bg-slate-50 p-4 text-sm leading-6 text-slate-700">
            {insight}
          </div>
        ))}
      </div>
    </div>
  );
}
