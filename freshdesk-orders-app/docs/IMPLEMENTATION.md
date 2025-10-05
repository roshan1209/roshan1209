## Freshdesk Orders Summary App

This app shows a customer's recent orders within Freshdesk for both agents (ticket sidebar) and end-customers (support portal). It uses mock APIs initially and supports an easy switch to real APIs via iparams.

### Core Requirements
- Show recent orders for customers in the support portal when they view/create tickets.
- Show the same summary for agents viewing tickets.
- Use FDK; support both app locations.

### Architecture
- Locations: `ticket_sidebar` (agent), `support_portal` (customer portal)
- UI: `app/index.html` and `portal/index.html` with light JS to render cards
- Serverless: `server/handlers.js` exposes `getRecentOrders` using `$request.invokeTemplate`
- Iparams: `api_base_url`, `api_token`, `orders_limit`, `enable_portal_app`
- Security: No customer PII stored. Requests to external API originate from serverless to avoid exposing tokens in the browser. Customer is derived from Freshdesk context (requester/contact).

### Data Flow
1. UI loads and fetches iparams via `client.iparams.get()`.
2. UI gathers context via `client.data.get('ticket')` or `client.data.get('contact')`.
3. UI invokes serverless: `client.request.invoke('server.getRecentOrders', {...})`.
4. Serverless calls external API (or returns mock on failure/misconfig) and normalizes the response.
5. UI renders order cards with expand/collapse items and optional link to ShopEasy.

### API Contract (Mock)
- Endpoint: `${api_base_url}/orders/recent?email={email}&contactId={id}&limit={n}`
- Response: array of orders
```
[{
  id: "ord_1001",
  orderNumber: "SE-1001",
  placedAt: "2025-09-25T10:15:00Z",
  status: "Delivered",
  totalCents: 12999,
  currency: "USD",
  orderUrl: "https://shops.easy/orders/SE-1001",
  items: [{ sku: "SKU-IPHONE", name: "iPhone Case", quantity: 1, priceCents: 1999 }]
}]
```

### Error Handling Strategy
- UI shows skeleton then an error banner on exceptions.
- Serverless wraps API call; if it fails or iparams missing, returns mock dataset with `{ fallback: true }` meta.
- Unknown customer (no id/email) returns empty list gracefully.
- Network timeouts are capped (5s) and logged.

### Testing
- Local: `fdk run` and test both locations.
- Agent: Open any ticket with a requester; verify orders render.
- Portal: Log in to support portal and view/create a ticket; verify orders.
- Edge cases: unknown contact, API down, empty orders, large item lists.

### Deployment
1. Configure iparams in Freshdesk (base URL, token, limit).
2. Validate and package: `fdk validate` then `fdk pack`.
3. Upload the zip in Freshdesk Apps > Custom Apps.

### Future Enhancements
- Add actions: Start return/reorder; deep link with SSO.
- Add status filters and pagination.
- Add SLA badges and fraud/risk indicators.
- Add analytics and feature flags.
- Add caching layer and rate-limiting in serverless.

### Security
- External API token stored in iparams; only serverless uses it.
- Minimal PII: customer id/email transiently used for lookup.
- Consider Freshworks Data Storage for limited per-contact caching with TTL.
