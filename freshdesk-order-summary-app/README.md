# ShopEasy Order Summary - Freshdesk App

A professional FDK v2.3 app that shows recent customer orders to agents (ticket sidebar) and customers (portal). Includes serverless data fetching, mock support, and clean UI.

## Features
- Agent: `ticket_sidebar` shows recent orders for the ticket requester
- Customer portal: `portal_ticket_requester_info` shows the logged-in user's orders
- Serverless `fetchRecentOrders` with mock data fallback
- Configurable base URL, token, and order count via iparams
- Loading, empty, and error states

## Getting Started
1. Install FDK: `npm i -g fdk` (or refer to Freshworks docs)
2. Configure `iparams` after install
   - Base URL: `https://api.mockorders.local` (keeps mock mode on)
   - Token: optional
   - Orders to show: default 5
3. Run locally: `fdk run`
4. Package: `fdk pack` → upload the zip in Freshdesk Admin → Apps → Upload Custom App

## Files
- `manifest.json`: app meta, locations, serverless methods
- `app/agent/*`: agent UI
- `app/portal/*`: portal UI
- `server/server.js`: serverless logic
- `server/mock.js`: mock orders generator for reference
- `config/iparams.*`: app configuration UI/JSON
- `docs/IMPLEMENTATION.md`: architecture and deployment notes

## Security Notes
- Uses requester identity from Freshdesk context; do not trust client input alone
- Prefer real API with auth + allow-list and rate limits when going live
- Ensure whitelisted domains match your Orders API
