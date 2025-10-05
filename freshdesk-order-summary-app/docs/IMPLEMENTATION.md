## ShopEasy Order Summary (Freshdesk App)

### Overview
- Displays a customer's recent orders to both customers (Freshdesk portal) and agents (ticket sidebar)
- Built with FDK v2.3, serverless method `fetchRecentOrders` and two UI locations

### Core requirements
- Customers (portal): See a concise list of their recent orders when creating or viewing tickets
- Agents (ticket sidebar): See the same order summary for the ticket requester
- Data should be secure, scoped to the requester identity, fast to load, resilient to API failures

### Benefits for ShopEasy
- Faster agent resolution with immediate order context
- Reduced back-and-forth with customers; improved self-service experience
- Lower ticket volume if customers can confirm order details by themselves

### Clarifying questions for ShopEasy
- How many orders should be displayed by default? (configurable now)
- Which fields are most important? (status, date, total, shipping ETA?)
- Any PII constraints? Should totals be hidden in portal?
- SLA for Orders API latency and error budget?
- Should customers be able to click through to ShopEasy orders? Deep link format?

### Architecture
- Locations
  - Agent: `ticket_sidebar` → `app/agent/index.html`
  - Portal: `portal_ticket_new`, `portal_ticket_view` → `app/portal/index.html`
- Serverless
  - `server/server.js` exposes `fetchRecentOrders`
  - Reads `iparams` and calls external Orders API or returns mock data
- Configuration
  - `config/iparams.json` & `config/iparams.html`
  - Fields: base URL, token, number of orders
- Network
  - Whitelisted domains in `manifest.json`

### Authentication & Authorization
- Portal identity from `loggedInUser.contact.email`/`id` via Freshdesk SDK
- Agent identity from `ticket.requester_email`/`requester_id`
- Serverless is the single trusted caller to Orders API (clients never call API directly)
- Real API should validate identity, ideally via signed token (JWT) or allow-listed server-to-server token

### Data Fetching Strategy (Mock APIs)
- When `orders_api_base_url` is empty or set to `https://api.mockorders.local` (or `mock:`), serverless returns synthesized orders
- For real integrations, point to the live API and set `orders_api_token`
- Request body `{ identity: {type, value}, limit }`

### Error Handling & Edge Cases
- UI shows skeletons, empty states, and actionable error messages
- Server validates identity, catches exceptions, and normalizes non-2xx responses
- Add retries with exponential backoff and circuit breaker when integrating the real API

### Data Presentation
- Compact cards with:
  - Order ID, placed date, status badge, total amount
  - Optional deep link to ShopEasy order page when available
- Same component structure for portal and agent; labels customized for tone (“Your recent orders” vs “Recent orders”)
- Consider expanders for item lines in future

### Testing
- Local: `fdk run`. Test on:
  - Customer with orders, customer with no orders
  - API unavailable; slow responses; malformed JSON
  - Portal ticket creation page and portal ticket view; agent ticket sidebar
- Validate identity extraction in both locations

### Deployment
1. Package: `fdk pack` → zip artifact
2. Upload to Freshdesk: Admin → Apps → Upload Custom App
3. Configure iparams: base URL (mock first), token, number of orders
4. Enable and verify in production

### Future Considerations
- Swap mock with live Orders API; add caching and pagination
- Portal actions: reorder/return; Agent insights: LTV, last order status detail
- Harden security: JWT per request, tenant allow-list, rate limiting
- Observability: structured logs, metrics, distributed tracing

### File Map
- `manifest.json` – app definition (locations, serverless)
- `app/agent/*` – agent UI
- `app/portal/*` – portal UI
- `server/server.js` – serverless method and mock fallback
- `config/iparams.*` – app configuration
- `docs/IMPLEMENTATION.md` – this document
