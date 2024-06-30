import React, { useState } from "react";
import axios from "axios";
import "../styles/globals.css"; // 正しいCSSファイルのインポートパス
import Layout from "./layout"; // 正しいlayout.tsxのインポートパス

const Home: React.FC = () => {
  const [barcode, setBarcode] = useState("");
  const [product, setProduct] = useState<any>(null);
  const [purchaseList, setPurchaseList] = useState<any[]>([]);

  const fetchProduct = async () => {
    try {
      const response = await axios.get(`http://localhost:8000/api/products/${barcode}`);
      console.log("API Response:", response.data); // デバッグ用
      if (response.data && response.data.name && response.data.price) {
        setProduct(response.data);
      } else {
        setProduct(null);
      }
    } catch (error) {
      console.error("API Error:", error); // デバッグ用
      setProduct(null);
    }
  };

  const addProductToList = () => {
    if (product) {
      setPurchaseList([...purchaseList, product]);
      setProduct(null);
      setBarcode("");
    }
  };

  const handlePurchase = async () => {
    try {
      const purchaseData = purchaseList.map((item) => ({
        code: item.code,
        quantity: 1, // quantityを適切に設定
      }));
      await axios.post("http://localhost:8000/api/purchase/", purchaseData);
      setPurchaseList([]);
    } catch (error) {
      console.error("Purchase Error:", error);
    }
  };

  const totalPrice = purchaseList.reduce((total, item) => total + item.price, 0);

  return (
    <Layout>
      <div className="bg-white p-6 rounded shadow-md w-full max-w-md">
        <div className="input-button-group mb-4">
          <input value={barcode} onChange={(e) => setBarcode(e.target.value)} placeholder="商品コードを入力" className="p-2 border rounded" />
          <button onClick={fetchProduct} className="button-blue">
            商品コード読み込み
          </button>
        </div>
        {product ? (
          <div className="product-info mb-4 p-4 border rounded bg-gray-50">
            <p>商品名: {product.name}</p>
            <p>価格: {product.price}円</p>
            <button onClick={addProductToList} className="button-green w-full">
              追加
            </button>
          </div>
        ) : (
          <div className="product-info mb-4 p-4 border rounded bg-gray-50">
            <p>商品名: -</p>
            <p>価格: -</p>
            <button disabled className="button-green w-full">
              追加
            </button>
          </div>
        )}
        <h2 className="text-xl mb-2">購入リスト</h2>
        <div className="purchase-list mb-4 p-4 border rounded bg-gray-50" style={{ minHeight: "150px" }}>
          {purchaseList.length > 0 ? (
            <ul className="list-disc pl-5">
              {purchaseList.map((item, index) => (
                <li key={index} className="mt-2">
                  {item.name} x 1 - {item.price}円
                </li>
              ))}
            </ul>
          ) : (
            <p>購入リストは空です</p>
          )}
        </div>
        <div className="total-amount mb-4 p-4 border rounded bg-gray-50">
          <p>合計金額: {totalPrice}円</p>
        </div>
        {purchaseList.length > 0 && (
          <button onClick={handlePurchase} className="button-red w-full">
            購入
          </button>
        )}
      </div>
    </Layout>
  );
};

export default Home;
