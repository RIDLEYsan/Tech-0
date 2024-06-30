import "../styles/globals.css"; // 正しいCSSファイルのインポートパス

function MyApp({ Component, pageProps }) {
  return <Component {...pageProps} />;
}

export default MyApp;
