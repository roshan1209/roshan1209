# Serverless Overview

- `getRecentOrders(args)`
  - input: `{ baseUrl, apiToken, ordersLimit, customer: { id, email } }`
  - output: `renderData(ordersArray)`
  - behavior: uses `$request.get` to call `${baseUrl}/orders/recent?email=..&contactId=..&limit=..`. Falls back to mock data on error.

Notes:
- This is intentionally stateless and idempotent.
- Add caching with `$storage` if needed in future iterations.
