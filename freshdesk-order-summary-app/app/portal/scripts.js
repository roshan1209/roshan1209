let client;

async function init() {
  client = await app.initialized();

  setLoading();

  try {
    const iparams = await client.iparams.get();
    const contact = await client.data.get('loggedInUser');

    const requesterEmail = contact && contact.loggedInUser && contact.loggedInUser.contact && contact.loggedInUser.contact.email;
    const requesterId = contact && contact.loggedInUser && contact.loggedInUser.contact && contact.loggedInUser.contact.id;

    const data = await client.request.invoke('fetchRecentOrders', {
      requesterEmail,
      requesterId,
      limit: iparams.orders_to_show
    });

    renderOrders((data && data.orders) || []);
  } catch (e) {
    setError('Failed to load orders');
  }
}

function setLoading() {
  const state = document.getElementById('state');
  const orders = document.getElementById('orders');
  state.innerHTML = '<div class="muted">Loading your orders…</div>';
  orders.innerHTML = '<div class="skeleton"></div><div class="skeleton"></div>';
}

function setError(msg) {
  document.getElementById('state').innerHTML = `<div class="error">${msg}</div>`;
  document.getElementById('orders').innerHTML = '';
}

function renderOrders(orders) {
  const state = document.getElementById('state');
  const list = document.getElementById('orders');
  if (!orders || orders.length === 0) {
    state.innerHTML = '<div class="muted">No recent orders found.</div>';
    list.innerHTML = '';
    return;
  }
  state.innerHTML = '';
  list.innerHTML = orders.map(renderOrder).join('');
}

function renderOrder(o) {
  const date = o.placed_at ? new Date(o.placed_at).toLocaleDateString() : '';
  const total = formatCurrency(o.currency || 'USD', o.total_amount || 0);
  const link = o.order_url ? `<a href="${o.order_url}" target="_blank">View</a>` : '';
  const status = o.status ? `<span class="badge">${o.status}</span>` : '';
  return `<li class="order">
    <div class="meta"><span>#${o.order_id || o.id}</span><span>${date}</span></div>
    <div class="title">${o.items_summary || (o.items && o.items[0] && o.items[0].name) || 'Order'}</div>
    <div class="meta"><span>${total}</span><span>${status} ${link}</span></div>
  </li>`;
}

function formatCurrency(code, amount) {
  try { return new Intl.NumberFormat(undefined, { style: 'currency', currency: code }).format(amount); } catch { return `${amount} ${code}`; }
}

document.addEventListener('DOMContentLoaded', init);
