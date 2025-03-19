const { createProxyMiddleware } = require('http-proxy-middleware');

module.exports = function(app) {
  // 配置 API 代理
  app.use(
    '/api',  // 匹配 /api 路径
    createProxyMiddleware({
      target: 'http://localhost:8000',  // 后端服务地址
      changeOrigin: true,
      logLevel: 'debug',
      onProxyReq: (proxyReq, req) => {
        console.log(`[Proxy] ${req.method} ${req.originalUrl} -> ${proxyReq.path}`);
      }
    })
  );
}; 