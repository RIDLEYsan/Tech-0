"use client";

import React, { useState } from "react";
import axios from "axios";
import "../app/global.css"; // 正しいパスでインポート

const Home: React.FC = () => {
  const [barcode, setBarcode] = useState("");
  const [product, setProduct] = useState<any>(null);
  const [purchaseList, setPurchaseList] = useState<any[]>([]);

  const fetchProduct = async () => {
    try {
      console.log(`Fetching product for barcode: ${barcode}`); // Debug message
      const response = await axios.get(`http://localhost:8000/api/products/${barcode}`, {
        timeout: 10000, // タイムアウトを10秒に設定
      });
      console.log("Product fetched:", response.data); // Debug message

      // 商品が存在しない場合の確認
      if (!response.data || !response.data.name || !response.data.price) {
        console.error("Product data is missing or incomplete");
        setProduct(null);
      } else {
        setProduct(response.data);
      }
    } catch (error) {
      console.error("Error fetching product:", error);
      setProduct(null); // Clear product information on error
    }
  };

  const addProductToList = () => {
    if (product) {
      console.log("Adding product to list:", product); // Debug message
      setPurchaseList([...purchaseList, product]);
      setProduct(null);
      setBarcode("");
    }
  };

  const handlePurchase = () => {
    console.log("Purchasing items:", purchaseList);
    // 購入処理をここに追加
    setPurchaseList([]);
  };

  return (
    <main className="flex flex-col items-center justify-center p-6 min-h-screen bg-gray-100">
      <div className="container">
        <div className="flex mb-4">
          <input value={barcode} onChange={(e) => setBarcode(e.target.value)} placeholder="商品コードを入力" className="flex-grow" />
          <button onClick={fetchProduct} className="ml-2 button-blue">
            商品コード読み込み
          </button>
        </div>
        {product && (
          <div className="product-info border p-4 rounded bg-gray-50">
            <div className="mb-2">
              <p>商品名: {product.name}</p>
            </div>
            <div className="mb-2">
              <p>価格: {product.price}円</p>
            </div>
            <button onClick={addProductToList} className="button-green">
              追加
            </button>
          </div>
        )}
        <h2 className="text-xl mb-2">購入リスト</h2>
        <div className="purchase-list">
          <ul className="list-disc pl-5">
            {purchaseList.map((item, index) => (
              <li key={index} className="purchase-item">
                {item.name} x 1 - {item.price}円
              </li>
            ))}
          </ul>
        </div>
        {purchaseList.length > 0 && (
          <button onClick={handlePurchase} className="button-red mt-4">
            購入
          </button>
        )}
      </div>
    </main>
  );
};

export default Home;
