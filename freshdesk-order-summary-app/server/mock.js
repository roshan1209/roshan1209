exports = {
  /**
   * Mock endpoint logic for local development via platform serverless testing.
   * Not called directly by Freshdesk, but you can use this with a mock URL.
   */
  recentOrders: function (args) {
    const limit = (args && args.limit) || 5;
    const orders = generateOrders(Math.min(limit, 10));
    renderData({ orders });
  }
};

function generateOrders(n) {
  const results = [];
  for (let i = 0; i < n; i++) {
    const id = 2000 + i;
    results.push({
      order_id: id,
      placed_at: new Date(Date.now() - i * 86400000).toISOString(),
      currency: 'USD',
      total_amount: 29.99 + i * 5,
      status: ['Processing', 'Shipped', 'Delivered'][i % 3],
      items_summary: `Item ${(i % 5) + 1} and more`,
      order_url: `https://shop.shopeasy.example/orders/${id}`
    });
  }
  return results;
}
