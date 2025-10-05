'use strict';

// Re-export handlers so that client.request.invoke can find functions here
const handlers = require('./handlers');
exports = handlers;
