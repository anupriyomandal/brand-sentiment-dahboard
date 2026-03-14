"use client";

import { Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

import { TrendsResponse } from "@/lib/types";

const COLORS = ["#f97316", "#0f766e", "#1d4ed8", "#dc2626", "#7c3aed"];

export function TrendChart({ data }: { data: TrendsResponse }) {
  const merged = Object.entries(data.sentiment).flatMap(([brand, points]) =>
    points.map((point) => ({ ...point, brand }))
  );

  return (
    <div className="panel">
      <p className="text-sm uppercase tracking-[0.3em] text-slate-500">Section 2</p>
      <h2 className="mb-6 text-2xl font-semibold">Sentiment Trend Chart</h2>
      <div className="h-80">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={merged}>
            <XAxis dataKey="date" />
            <YAxis domain={[-1, 1]} />
            <Tooltip />
            {Object.keys(data.sentiment).map((brand, index) => (
              <Line
                key={brand}
                type="monotone"
                dataKey="score"
                data={data.sentiment[brand]}
                stroke={COLORS[index % COLORS.length]}
                strokeWidth={3}
                dot={false}
                name={brand}
              />
            ))}
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
