"use client";

import { ArticleItem } from "@/lib/types";

function sentimentStyle(sentiment: string) {
  if (sentiment === "Positive") return "bg-emerald-100 text-emerald-700";
  if (sentiment === "Negative") return "bg-rose-100 text-rose-700";
  return "bg-amber-100 text-amber-700";
}

export function ArticleCard({ article }: { article: ArticleItem }) {
  return (
    <article className="rounded-3xl border border-white/60 bg-white p-5 shadow-panel">
      <div className="mb-3 flex flex-wrap items-center gap-2">
        <span className="rounded-full bg-slate-900 px-3 py-1 text-xs font-semibold text-white">{article.brand}</span>
        <span className={`rounded-full px-3 py-1 text-xs font-semibold ${sentimentStyle(article.sentiment)}`}>
          {article.sentiment}
        </span>
        <span className="rounded-full bg-slate-100 px-3 py-1 text-xs font-semibold text-slate-600">{article.topic}</span>
      </div>
      <h3 className="text-lg font-semibold leading-7 text-slate-900">{article.headline}</h3>
      <p className="mt-3 text-sm text-slate-500">
        {article.source} • {article.published_date}
      </p>
      <a
        href={article.url}
        target="_blank"
        rel="noreferrer"
        className="mt-4 inline-flex text-sm font-semibold text-coral"
      >
        Read article
      </a>
    </article>
  );
}
