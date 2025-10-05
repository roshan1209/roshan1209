'use strict';

let client;

function formatMoney(cents, currency) {
  try {
    return new Intl.NumberFormat(undefined, { style: 'currency', currency: currency || 'USD' }).format((cents || 0) / 100);
  } catch (_) {
    return `$${((cents || 0) / 100).toFixed(2)}`;
  }
}

function formatDate(value) { try { return new Date(value).toLocaleString(); } catch (_) { return value; } }

function orderCard(order) {
  const statusClass = 'badge';
  return `
    <div class="card">
      <div class="row">
        <div>
          <div><strong>${order.orderNumber}</strong> <span class="${statusClass}">${order.status}</span></div>
          <div class="muted">Placed: ${formatDate(order.placedAt)}</div>
        </div>
        <div><strong>${formatMoney(order.totalCents, order.currency)}</strong></div>
      </div>
      <div class="actions">
        ${order.orderUrl ? `<a class="link" target="_blank" href="${order.orderUrl}">View in ShopEasy</a>` : ''}
        ${order.items && order.items.length ? `<button class="button secondary" data-order="${order.id}" data-action="toggle">Items (${order.items.length})</button>` : ''}
      </div>
      ${order.items && order.items.length ? `<div class="items" id="items-${order.id}" style="display:none; margin-top:6px;">
        ${order.items.slice(0, 5).map(i => `<div class=\"muted\">${i.quantity} x ${i.name}</div>`).join('')}
      </div>` : ''}
    </div>
  `;
}

function renderLoading() { document.getElementById('content').innerHTML = '<div class="skeleton"></div><div class="skeleton"></div>'; }
function renderError(message) { document.getElementById('content').innerHTML = `<div class="error">${message}</div>`; }

function renderOrders(orders) {
  if (!orders || orders.length === 0) { document.getElementById('content').innerHTML = '<div class="muted">No recent orders found.</div>'; return; }
  const html = `<div class="list">${orders.map(orderCard).join('')}</div>`;
  const content = document.getElementById('content');
  content.innerHTML = html;
  content.addEventListener('click', (e) => {
    const target = e.target;
    if (target && target.dataset && target.dataset.action === 'toggle') {
      const id = target.dataset.order;
      const el = document.getElementById(`items-${id}`);
      if (el) el.style.display = el.style.display === 'none' ? 'block' : 'none';
    }
  });
}

async function fetchOrders(context) {
  const iparams = await client.iparams.get();
  const ordersLimit = iparams.orders_limit || 5;
  const baseUrl = iparams.api_base_url;
  const apiToken = iparams.api_token;

  const payload = {
    action: 'getRecentOrders',
    baseUrl,
    apiToken,
    ordersLimit,
    customer: context.customer,
  };

  const response = await client.request.invoke('getRecentOrders', payload);
  return response.response;
}

async function init() {
  try {
    client = await app.initialized();

    let context = { location: 'support_portal' };
    try {
      const contactData = await client.data.get('contact');
      context.customer = { id: contactData.contact && contactData.contact.id, email: contactData.contact && contactData.contact.email };
    } catch (_) { context.customer = {}; }

    renderLoading();
    const orders = await fetchOrders(context);
    renderOrders(orders);
  } catch (error) {
    console.error('Init error', error);
    renderError('Unable to load your orders. Please try again later.');
  }
}

init();
