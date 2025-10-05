'use strict';

const MOCK_ORDERS = [
  {
    id: 'ord_1001',
    orderNumber: 'SE-1001',
    placedAt: '2025-09-25T10:15:00Z',
    status: 'Delivered',
    totalCents: 12999,
    currency: 'USD',
    orderUrl: 'https://shops.easy/orders/SE-1001',
    items: [
      { sku: 'SKU-IPHONE', name: 'iPhone Case', quantity: 1, priceCents: 1999 },
      { sku: 'SKU-CABLE', name: 'USB-C Cable', quantity: 2, priceCents: 1500 }
    ]
  },
  {
    id: 'ord_1002',
    orderNumber: 'SE-1002',
    placedAt: '2025-09-27T12:40:00Z',
    status: 'Shipped',
    totalCents: 8999,
    currency: 'USD',
    orderUrl: 'https://shops.easy/orders/SE-1002',
    items: [
      { sku: 'SKU-HDST', name: 'Bluetooth Headset', quantity: 1, priceCents: 8999 }
    ]
  },
  {
    id: 'ord_1003',
    orderNumber: 'SE-1003',
    placedAt: '2025-09-30T09:05:00Z',
    status: 'Processing',
    totalCents: 4599,
    currency: 'USD',
    orderUrl: 'https://shops.easy/orders/SE-1003',
    items: [
      { sku: 'SKU-MSE', name: 'Wireless Mouse', quantity: 1, priceCents: 4599 }
    ]
  }
];

exports = {
  /**
   * App lifecycle handlers (optional)
   */
  onInstall: async function (args) {
    console.info('App installed', args);
    renderData();
  },
  onUninstall: async function (args) {
    console.info('App uninstalled', args);
    renderData();
  },

  /**
   * Server method to fetch recent orders for a given customer.
   * Exposed as: client.request.invoke('server.getRecentOrders', payload)
   */
  getRecentOrders: async function (args) {
    try {
      const { baseUrl, apiToken, ordersLimit = 5, customer = {} } = args;

      const normalizedCustomer = normalizeCustomer(customer);
      if (!normalizedCustomer) {
        // Cannot identify customer, return empty list gracefully
        return renderData([]);
      }

      if (!baseUrl) {
        // No API configured: return mock
        return renderData(MOCK_ORDERS.slice(0, ordersLimit));
      }

      const url = `${trimTrailingSlash(baseUrl)}/orders/recent`;
      const query = buildQuery({ email: normalizedCustomer.email, contactId: normalizedCustomer.id, limit: ordersLimit });
      const fullUrl = `${url}?${query}`;

      const options = {
        method: 'GET',
        headers: { 'Content-Type': 'application/json', ...(apiToken ? { Authorization: apiToken } : {}) },
        timeout: 5000
      };

      try {
        const response = await $request.get(fullUrl, { headers: options.headers, timeout: 5000 });
        const parsed = Array.isArray(response.response) ? response.response : JSON.parse(response.response || '[]');
        const orders = sanitizeOrders(parsed).slice(0, ordersLimit);
        return renderData(orders);
      } catch (apiError) {
        console.error('Orders API failed, falling back to mock', apiError);
        return renderData(MOCK_ORDERS.slice(0, ordersLimit), { fallback: true, error: toError(apiError) });
      }
    } catch (error) {
      console.error('getRecentOrders error', error);
      return renderData([], { error: toError(error) });
    }
  }
};

function sanitizeOrders(input) {
  try {
    const list = Array.isArray(input) ? input : [];
    return list.map((o, idx) => ({
      id: o.id || o.order_id || `tmp_${idx}`,
      orderNumber: o.orderNumber || o.number || o.code || `ORD-${idx + 1}`,
      placedAt: o.placedAt || o.created_at || o.createdAt || new Date().toISOString(),
      status: o.status || 'Unknown',
      totalCents: ensureCents(o.totalCents ?? o.total_cents ?? o.total ?? 0),
      currency: o.currency || 'USD',
      orderUrl: o.orderUrl || o.url || null,
      items: Array.isArray(o.items) ? o.items.map(it => ({
        sku: it.sku || it.code || null,
        name: it.name || it.title || 'Item',
        quantity: Number(it.quantity || 1),
        priceCents: ensureCents(it.priceCents ?? it.price_cents ?? it.price ?? 0)
      })) : []
    }));
  } catch (_) { return []; }
}

function ensureCents(value) {
  const num = Number(value);
  return Number.isFinite(num) ? Math.round(num % 1 === 0 ? num : num * 100) : 0;
}

function normalizeCustomer(customer) {
  if (!customer) return null;
  const id = customer.id || customer.contact_id || customer.requester_id;
  const email = customer.email || customer.requester_email || null;
  if (!id && !email) return null;
  return { id, email };
}

function buildQuery(params) {
  return Object.entries(params)
    .filter(([, v]) => v !== undefined && v !== null && v !== '')
    .map(([k, v]) => `${encodeURIComponent(k)}=${encodeURIComponent(v)}`)
    .join('&');
}

function trimTrailingSlash(s) { return (s || '').replace(/\/$/, ''); }

function toError(err) {
  try { return { message: err.message || String(err), status: err.status || err.statusCode, code: err.code }; } catch (_) { return { message: 'Unknown error' }; }
}
