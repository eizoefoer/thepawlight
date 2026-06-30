// Public site analytics configuration.
// Cloudflare Web Analytics site tokens are public browser tokens.
// Cloudflare Web Analytics token for thepawlight.com.
window.PAWLIGHT_ANALYTICS = window.PAWLIGHT_ANALYTICS || {
  provider: "cloudflare-web-analytics",
  cloudflareToken: "959743b47645483e96d369eb6b75a594",
  sourceParameters: [
    "utm_source",
    "utm_medium",
    "utm_campaign",
    "utm_content",
    "utm_term"
  ]
};
