export type SummaryItem = {
  brand: string;
  articles: number;
  positive: number;
  neutral: number;
  negative: number;
  score: number;
};

export type TrendPoint = {
  date: string;
  score: number;
};

export type TopicDistributionItem = {
  brand: string;
  topic: string;
  count: number;
};

export type TrendsResponse = {
  sentiment: Record<string, TrendPoint[]>;
  topics: TopicDistributionItem[];
};

export type InsightResponse = {
  insights: string[];
};

export type ArticleItem = {
  id: number;
  brand: string;
  headline: string;
  source: string;
  url: string;
  sentiment: string;
  topic: string;
  published_date: string;
  created_at: string;
};

export type PaginatedArticles = {
  page: number;
  limit: number;
  total: number;
  items: ArticleItem[];
};

export type AlertItem = {
  brand: string;
  negative_ratio: number;
  negative_articles: number;
  total_articles: number;
  triggered: boolean;
};
