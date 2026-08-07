# Custom Domain

No domain change is authorized. The canonical production URL remains `https://concrete-motivation-app.lovable.app` until Jaytee approves a domain and DNS records.

In Lovable, open project `09f0d02d-8d41-40c7-9c36-bbdbf8d11adf`, choose the custom-domain settings, enter the owner-approved domain, and copy the exact records Lovable displays into the DNS provider. Do not guess records. Choose either apex as canonical with `www` redirect, or `www` as canonical with apex redirect. After propagation verify HTTPS, redirects, canonical tags, sitemap, robots, OAuth callbacks, Stripe webhook, email links, social links, and store support/privacy URLs. Record prior DNS values and TTL before any approved change so rollback is possible.
