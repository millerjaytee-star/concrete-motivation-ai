"use client";

import Script from "next/script";
import { useEffect, useState } from "react";

type Consent = "unknown" | "granted" | "denied";

export function AnalyticsConsent({ measurementId }: { measurementId?: string }) {
  const [consent, setConsent] = useState<Consent>("unknown");

  useEffect(() => {
    const stored = window.localStorage.getItem("cm-analytics-consent");
    // Restore the browser-only preference after hydration to avoid server/client markup drift.
    // eslint-disable-next-line react-hooks/set-state-in-effect
    if (stored === "granted" || stored === "denied") setConsent(stored);
  }, []);

  if (!measurementId) return null;

  const choose = (next: Exclude<Consent, "unknown">) => {
    window.localStorage.setItem("cm-analytics-consent", next);
    setConsent(next);
  };

  return (
    <>
      {consent === "granted" ? (
        <>
          <Script src={`https://www.googletagmanager.com/gtag/js?id=${measurementId}`} strategy="afterInteractive" />
          <Script id="cm-ga4" strategy="afterInteractive">{`
            window.dataLayer = window.dataLayer || [];
            function gtag(){dataLayer.push(arguments);}
            gtag('js', new Date());
            gtag('config', '${measurementId}', { anonymize_ip: true, allow_google_signals: false });
          `}</Script>
        </>
      ) : null}
      {consent === "unknown" ? (
        <aside className="consent-banner" aria-label="Analytics preference">
          <p><strong>Privacy-first analytics.</strong> Help improve the experience with anonymized usage measurement. No advertising profiles.</p>
          <div className="button-row">
            <button className="button button-primary" type="button" onClick={() => choose("granted")}>Allow analytics</button>
            <button className="button button-secondary" type="button" onClick={() => choose("denied")}>Essential only</button>
          </div>
        </aside>
      ) : null}
    </>
  );
}
