import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  reactStrictMode: true,
  poweredByHeader: false,
  env: {
    COMMAND_BUILD_ORIGIN: process.env.DEPLOY_PRIME_URL ?? "",
    COMMAND_IMMUTABLE_BUILD_ORIGIN: process.env.DEPLOY_URL ?? ""
  },
  async redirects() {
    return [
      { source: "/about", destination: "/about-jaytee", permanent: true },
      { source: "/membership", destination: "/memberships", permanent: true },
      { source: "/pillars", destination: "/#framework", permanent: true }
    ];
  },
  images: { formats: ["image/avif", "image/webp"] }
};

export default nextConfig;
