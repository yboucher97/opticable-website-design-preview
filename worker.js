const APEX_HOST = "opticable.ca";
const WWW_HOST = "www.opticable.ca";
const HSTS_VALUE = "max-age=31536000; includeSubDomains; preload";
const LONG_CACHE = "public, max-age=31536000, immutable";
const HTML_CACHE = "public, max-age=0, must-revalidate";
const LEGACY_REDIRECTS = new Map([
  ["/fr", "/"],
  ["/fr/", "/"],
  ["/fr/index.html", "/"],
  ["/fr/secteurs", "/fr/clientele/"],
  ["/fr/secteurs/", "/fr/clientele/"],
  ["/fr/secteurs/index.html", "/fr/clientele/"],
]);

function cacheControlForPath(pathname) {
  if (pathname.startsWith("/assets/")) {
    return LONG_CACHE;
  }

  if (pathname === "/site.webmanifest") {
    return "public, max-age=86400";
  }

  if (pathname === "/robots.txt" || pathname === "/sitemap.xml" || pathname === "/ads.txt") {
    return "public, max-age=3600";
  }

  return HTML_CACHE;
}

function withResponseHeaders(response, pathname) {
  const headers = new Headers(response.headers);
  headers.set("Strict-Transport-Security", HSTS_VALUE);
  headers.set("X-Content-Type-Options", "nosniff");
  headers.set("Referrer-Policy", "strict-origin-when-cross-origin");
  headers.set("Cache-Control", cacheControlForPath(pathname));
  return new Response(response.body, {
    status: response.status,
    statusText: response.statusText,
    headers,
  });
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const redirectUrl = new URL(url);
    let shouldRedirect = false;

    if (redirectUrl.hostname === WWW_HOST) {
      redirectUrl.hostname = APEX_HOST;
      shouldRedirect = true;
    }

    const legacyTarget = LEGACY_REDIRECTS.get(redirectUrl.pathname);
    if (legacyTarget) {
      redirectUrl.pathname = legacyTarget;
      shouldRedirect = true;
    }

    if (shouldRedirect) {
      return Response.redirect(redirectUrl.toString(), 301);
    }

    let response = await env.ASSETS.fetch(request);

    if (response.status === 404 && url.pathname !== "/404.html") {
      const notFoundUrl = new URL("/404.html", url.origin);
      const notFoundRequest = new Request(notFoundUrl.toString(), request);
      const notFoundResponse = await env.ASSETS.fetch(notFoundRequest);
      if (notFoundResponse.ok) {
        response = new Response(notFoundResponse.body, {
          status: 404,
          statusText: "Not Found",
          headers: notFoundResponse.headers,
        });
      }
    }

    return withResponseHeaders(response, url.pathname);
  },
};
