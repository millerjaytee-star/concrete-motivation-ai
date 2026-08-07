import type { MetadataRoute } from "next";

export default function manifest(): MetadataRoute.Manifest {
  return {
    name: "Concrete Motivation",
    short_name: "Concrete",
    description: "Build from pressure. Lead with purpose. Move with discipline.",
    start_url: "/",
    display: "standalone",
    background_color: "#070707",
    theme_color: "#d5a021",
    categories: ["business", "education", "lifestyle"],
  };
}
