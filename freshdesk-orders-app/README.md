# ShopEasy Orders Summary - Freshdesk App

This Freshdesk app shows a customer's recent orders for both Agents (ticket sidebar) and Customers (support portal). Built with FDK v2.3 and serverless functions.

## Run Locally
1. Install FDK: `npm i -g fdk` (or see docs)
2. From the project root:
   - `fdk validate`
   - `fdk run`
3. In Freshdesk (trial), install the app in dev mode and set iparams.

## Configure
- `api_base_url` (optional): mock or real API. If blank, app uses mock data.
- `api_token` (optional): sent as `Authorization` header from serverless.
- `orders_limit` (optional): default 5.
- `enable_portal_app`: keep true to show in portal.

## Deploy
- `fdk pack` -> upload zip in Freshdesk Admin > Apps > Custom Apps.

See `docs/IMPLEMENTATION.md` for details and R2 write-up.
