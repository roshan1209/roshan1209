/******** Freshdesk Serverless: ShopEasy Order Summary ********/

exports = {
  onAppInstall: function (args) {
    console.info('ShopEasy Order Summary app installed', args);
    renderData();
  },

  onAppUninstall: function (args) {
    console.info('ShopEasy Order Summary app uninstalled', args);
    renderData();
  },

  /**
   * fetchRecentOrders
   * Serverless method callable from client to fetch recent orders for a given customer.
   * Input: { requesterEmail?, requesterId?, externalCustomerId?, limit? }
   */
  fetchRecentOrders: async function (args) {
    try {
      const {iparams} = args || {};
      const baseUrl = (iparams && iparams.orders_api_base_url) || (await $iparams.get('orders_api_base_url'));
      const apiToken = (iparams && iparams.orders_api_token) || (await $iparams.get('orders_api_token'));
      const limit = (args && args.limit) || (await $iparams.get('orders_to_show')) || 5;

      const identity = buildIdentity(args);
      if (!identity) {
        return renderData({
          status: 400,
          message: 'Missing customer identity. Provide requesterEmail, requesterId, or externalCustomerId.'
        });
      }

      // If using a mock base URL, synthesize orders locally for ease of demo
      const isMock = !baseUrl || /api\.mockorders\.local/i.test(baseUrl) || /^mock:/i.test(String(baseUrl));
      if (isMock) {
        const mocked = generateOrders(Math.min(Number(limit) || 5, 20));
        return renderData({ orders: mocked, fetchedAt: new Date().toISOString(), source: 'mock' });
      }

      // Call external Orders API via FDK $request with whitelisted domain
      const url = `${String(baseUrl).replace(/\/$/, '')}/orders/recent`;
      const headers = {
        'Content-Type': 'application/json',
        ...(apiToken ? { Authorization: `Bearer ${apiToken}` } : {})
      };

      const response = await $request.post(url, { headers, body: JSON.stringify({ identity, limit }) });

      if (!response || typeof response.status !== 'number') {
        return renderData({ status: 502, message: 'Invalid response from Orders API' });
      }
      if (response.status < 200 || response.status >= 300) {
        return renderData({ status: response.status, message: `Orders API error (${response.status})` });
      }

      let data;
      try {
        data = response.response ? JSON.parse(response.response) : {};
      } catch (e) {
        return renderData({ status: 502, message: 'Malformed JSON from Orders API' });
      }

      const orders = Array.isArray(data && data.orders) ? data.orders : [];
      return renderData({ orders, fetchedAt: new Date().toISOString(), source: 'api' });
    } catch (error) {
      console.error('fetchRecentOrders error', error);
      return renderData({ status: 500, message: 'Unexpected error fetching orders' });
    }
  }
};

function buildIdentity(args) {
  if (!args) return null;
  if (args.requesterEmail) return { type: 'email', value: String(args.requesterEmail).trim().toLowerCase() };
  if (args.requesterId) return { type: 'freshdesk_requester_id', value: String(args.requesterId) };
  if (args.externalCustomerId) return { type: 'external_id', value: String(args.externalCustomerId) };
  return null;
}

function generateOrders(n) {
  const result = [];
  for (let i = 0; i < (n || 5); i++) {
    const id = 100000 + i;
    result.push({
      order_id: id,
      placed_at: new Date(Date.now() - i * 86400000).toISOString(),
      currency: 'USD',
      total_amount: 29.99 + i * 5,
      status: ['Processing', 'Shipped', 'Delivered'][i % 3],
      items_summary: `Item ${(i % 5) + 1} and more`,
      order_url: `https://shop.shopeasy.example/orders/${id}`
    });
  }
  return result;
}
