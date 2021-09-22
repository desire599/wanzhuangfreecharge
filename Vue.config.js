module.exports = {
//   lintOnSave: false // 暂时关闭代码格式检测
// 配置反向代理
  devServer: {
    proxy: {
      '/query': {
        // target: 'https://websocket.wanzhuangkj.com',
        target: 'http://localhost:5000',
        changeOrigin: true
      },
      '/device/getChargeInfo': {
        target: 'http://localhost:5000',
        changeOrigin: true
      },
      '/device/stop_charge': {
        target: 'http://localhost:5000',
        changeOrigin: true
      },
      '/device': {
        target: 'https://websocket.wanzhuangkj.com',
        changeOrigin: true
      },
      '/pay/request': {
        // target: 'https://webapi.wanzhuangkj.com',
        target: 'http://localhost:5000',
        changeOrigin: true
      },
      '/uploadInfo': {
        target: 'http://localhost:5000',
        changeOrigin: true
      },
      '/getAuth': {
        target: 'http://localhost:5000',
        changeOrigin: true
      }

    }
  }
}
