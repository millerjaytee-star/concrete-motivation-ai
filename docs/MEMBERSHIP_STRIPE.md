# Membership And Stripe

Concrete Builder Membership gives the brand a recurring revenue path without pretending the community is already proven.

## Offers

- Weekly Builder: $9/month for weekly challenges, reflection prompts, early selected content, and reset emails.
- Concrete Builder: $29/month for challenges, monthly live reset/replay, guides, and workshop/event discounts.
- Team Standard: custom pricing for schools, teams, churches, and organizations.

## Stripe Setup

Use Stripe Payment Links or Checkout for the first launch. Do not commit Stripe secret keys.

1. Create products and recurring prices in Stripe.
2. Create Payment Links for Weekly Builder and Concrete Builder.
3. Copy the approved public Payment Links into the website deployment config.
4. Replace the empty `stripeLinks` values in `website/script.js` during deployment or inject them through the hosting layer.
5. Run a test checkout before sharing the page.

The local website intentionally does not collect payment until real Stripe links are added.
