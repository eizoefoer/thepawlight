// Public site analytics configuration.
// Cloudflare Web Analytics site tokens are public browser tokens.
// Fill cloudflareToken after creating a Web Analytics site for thepawlight.com.
window.PAWLIGHT_ANALYTICS = window.PAWLIGHT_ANALYTICS || {
  provider: "cloudflare-web-analytics",
  cloudflareToken: "",
  sourceParameters: [
    "utm_source",
    "utm_medium",
    "utm_campaign",
    "utm_content",
    "utm_term"
  ]
};
