import type { APIRoute } from "astro";
import { llmsTxt, postSummaries } from "../lib/agent-markdown";

export const GET: APIRoute = async ({ site }) =>
  new Response(llmsTxt(await postSummaries(), site!), {
    headers: { "Content-Type": "text/plain; charset=utf-8" },
  });
