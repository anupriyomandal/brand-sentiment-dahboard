"use client";

import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

import { TopicDistributionItem } from "@/lib/types";

export function TopicChart({ data }: { data: TopicDistributionItem[] }) {
  return (
    <div className="panel">
      <p className="text-sm uppercase tracking-[0.3em] text-slate-500">Section 3</p>
      <h2 className="mb-6 text-2xl font-semibold">Topic Distribution</h2>
      <div className="h-80">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="topic" />
            <YAxis />
            <Tooltip />
            <Bar dataKey="count" fill="#0f766e" radius={[8, 8, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
