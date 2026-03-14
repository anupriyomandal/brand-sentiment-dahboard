import {
  AlertItem,
  InsightResponse,
  PaginatedArticles,
  SummaryItem,
  TrendsResponse
} from "@/lib/types";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://127.0.0.1:8000";

export async function fetchSummary(): Promise<SummaryItem[]> {
  const response = await fetch(`${API_BASE_URL}/summary`, { cache: "no-store" });
  if (!response.ok) throw new Error("Failed to fetch summary");
  return response.json();
}

export async function fetchTrends(): Promise<TrendsResponse> {
  const response = await fetch(`${API_BASE_URL}/trends`, { cache: "no-store" });
  if (!response.ok) throw new Error("Failed to fetch trends");
  return response.json();
}

export async function fetchInsights(): Promise<InsightResponse> {
  const response = await fetch(`${API_BASE_URL}/insights`, { cache: "no-store" });
  if (!response.ok) throw new Error("Failed to fetch insights");
  return response.json();
}

export async function fetchAlerts(): Promise<AlertItem[]> {
  const response = await fetch(`${API_BASE_URL}/alerts`, { cache: "no-store" });
  if (!response.ok) throw new Error("Failed to fetch alerts");
  return response.json();
}

export async function fetchArticles(params: {
  page?: number;
  limit?: number;
  brand?: string;
  sentiment?: string;
  topic?: string;
}): Promise<PaginatedArticles> {
  const search = new URLSearchParams();
  if (params.page) search.set("page", String(params.page));
  if (params.limit) search.set("limit", String(params.limit));
  if (params.brand) search.set("brand", params.brand);
  if (params.sentiment) search.set("sentiment", params.sentiment);
  if (params.topic) search.set("topic", params.topic);

  const response = await fetch(`${API_BASE_URL}/articles?${search.toString()}`, { cache: "no-store" });
  if (!response.ok) throw new Error("Failed to fetch articles");
  return response.json();
}
