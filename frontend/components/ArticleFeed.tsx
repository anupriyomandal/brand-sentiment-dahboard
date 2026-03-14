"use client";

import { useInfiniteQuery } from "@tanstack/react-query";
import { useMemo } from "react";

import { fetchArticles } from "@/lib/api";
import { ArticleCard } from "@/components/ArticleCard";

type Filters = {
  brand: string;
  sentiment: string;
  topic: string;
};

export function ArticleFeed({ filters }: { filters: Filters }) {
  const query = useInfiniteQuery({
    queryKey: ["articles", filters],
    queryFn: ({ pageParam = 1 }) =>
      fetchArticles({
        page: pageParam,
        limit: 20,
        brand: filters.brand || undefined,
        sentiment: filters.sentiment || undefined,
        topic: filters.topic || undefined
      }),
    initialPageParam: 1,
    getNextPageParam: (lastPage) => {
      const loaded = lastPage.page * lastPage.limit;
      return loaded < lastPage.total ? lastPage.page + 1 : undefined;
    }
  });

  const articles = useMemo(
    () => query.data?.pages.flatMap((page) => page.items) ?? [],
    [query.data]
  );

  return (
    <div className="panel">
      <div className="mb-6 flex items-end justify-between gap-4">
        <div>
          <p className="text-sm uppercase tracking-[0.3em] text-slate-500">Section 5</p>
          <h2 className="text-2xl font-semibold">Articles Feed</h2>
        </div>
        {query.hasNextPage && (
          <button
            onClick={() => query.fetchNextPage()}
            className="rounded-full bg-ink px-4 py-2 text-sm font-semibold text-white"
          >
            Load more
          </button>
        )}
      </div>
      <div className="grid gap-4">
        {articles.map((article) => (
          <ArticleCard key={article.id} article={article} />
        ))}
      </div>
    </div>
  );
}
