"use client";

import { Button } from "@/components/ui/button";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { itemApi, orderApi, userApi } from "@/services/api";
import { Item } from "@/types/item";
import { Order, OrderStatus } from "@/types/order";
import { User } from "@/types/user";
import { formatToJST } from "@/utils/date";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";

interface OrderDetailPageProps {
  params: {
    id: string;
  };
}

export default function OrderDetailPage({ params }: OrderDetailPageProps) {
  const router = useRouter();
  const orderId = params.id;
  const [order, setOrder] = useState<Order | null>(null);
  const [user, setUser] = useState<User | null>(null);
  const [items, setItems] = useState<{ [key: string]: Item }>({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // 注文ステータスに対応する表示色を定義
  const statusColors: { [key in OrderStatus]: string } = {
    [OrderStatus.PENDING]: "bg-yellow-100 text-yellow-800",
    [OrderStatus.PROCESSING]: "bg-blue-100 text-blue-800",
    [OrderStatus.SHIPPED]: "bg-indigo-100 text-indigo-800",
    [OrderStatus.DELIVERED]: "bg-green-100 text-green-800",
    [OrderStatus.CANCELLED]: "bg-red-100 text-red-800",
  };

  // 注文ステータスの日本語表示
  const statusLabels: { [key in OrderStatus]: string } = {
    [OrderStatus.PENDING]: "処理待ち",
    [OrderStatus.PROCESSING]: "処理中",
    [OrderStatus.SHIPPED]: "発送済み",
    [OrderStatus.DELIVERED]: "配達完了",
    [OrderStatus.CANCELLED]: "キャンセル",
  };

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);

        // 注文データを取得
        const orderData = await orderApi.getOrder(orderId);
        setOrder(orderData);

        // ユーザーデータを取得
        const userData = await userApi.getUser(orderData.user_id);
        setUser(userData);

        // 商品データを取得
        const allItems = await itemApi.getItems();

        // 商品データをIDをキーとしたオブジェクトに変換
        const itemsMap = allItems.reduce((acc, item) => {
          acc[item.id] = item;
          return acc;
        }, {} as { [key: string]: Item });

        setItems(itemsMap);
        setError(null);
      } catch (err) {
        console.error("Error fetching data:", err);
        setError("Failed to load order details. Please try again later.");
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [orderId]);

  const handleDelete = async () => {
    if (window.confirm("Are you sure you want to delete this order?")) {
      try {
        await orderApi.deleteOrder(orderId);
        router.push("/orders");
      } catch (err) {
        console.error("Error deleting order:", err);
        alert("Failed to delete order. Please try again.");
      }
    }
  };

  if (loading)
    return (
      <div className="container mx-auto p-6">Loading order details...</div>
    );
  if (error)
    return <div className="container mx-auto p-6 text-red-500">{error}</div>;
  if (!order)
    return <div className="container mx-auto p-6">Order not found</div>;

  return (
    <div className="container mx-auto p-6 max-w-4xl">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">注文詳細</h1>
        <div className="flex space-x-2">
          <Link href="/orders">
            <Button variant="outline">戻る</Button>
          </Link>
          <Link href={`/orders/edit/${order.id}`}>
            <Button>編集</Button>
          </Link>
          <Button variant="destructive" onClick={handleDelete}>
            削除
          </Button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-xl font-semibold mb-4">注文情報</h2>
          <dl className="space-y-2">
            <div className="flex justify-between">
              <dt className="font-medium text-gray-500">注文ID:</dt>
              <dd>{order.id}</dd>
            </div>
            <div className="flex justify-between">
              <dt className="font-medium text-gray-500">注文日時:</dt>
              <dd>{formatToJST(order.created_at)}</dd>
            </div>
            <div className="flex justify-between">
              <dt className="font-medium text-gray-500">合計金額:</dt>
              <dd className="font-bold">
                ¥{order.total_amount.toLocaleString()}
              </dd>
            </div>
            <div className="flex justify-between">
              <dt className="font-medium text-gray-500">ステータス:</dt>
              <dd>
                <span
                  className={`px-2 py-1 rounded-full text-xs ${
                    statusColors[order.status]
                  }`}
                >
                  {statusLabels[order.status]}
                </span>
              </dd>
            </div>
          </dl>
        </div>

        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-xl font-semibold mb-4">顧客情報</h2>
          {user ? (
            <dl className="space-y-2">
              <div className="flex justify-between">
                <dt className="font-medium text-gray-500">名前:</dt>
                <dd>{user.full_name}</dd>
              </div>
              <div className="flex justify-between">
                <dt className="font-medium text-gray-500">メール:</dt>
                <dd>{user.email}</dd>
              </div>
              <div className="flex justify-between">
                <dt className="font-medium text-gray-500">ユーザーID:</dt>
                <dd>{user.id}</dd>
              </div>
            </dl>
          ) : (
            <p>ユーザー情報が見つかりません</p>
          )}
        </div>
      </div>

      <div className="bg-white p-6 rounded-lg shadow mb-6">
        <h2 className="text-xl font-semibold mb-4">配送情報</h2>
        <dl className="space-y-2">
          <div className="flex justify-between">
            <dt className="font-medium text-gray-500">配送先住所:</dt>
            <dd>{order.shipping_address || "未設定"}</dd>
          </div>
          <div className="flex justify-between">
            <dt className="font-medium text-gray-500">備考:</dt>
            <dd>{order.notes || "備考なし"}</dd>
          </div>
        </dl>
      </div>

      <div className="bg-white p-6 rounded-lg shadow">
        <h2 className="text-xl font-semibold mb-4">注文商品</h2>
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>商品名</TableHead>
              <TableHead className="text-right">単価</TableHead>
              <TableHead className="text-right">数量</TableHead>
              <TableHead className="text-right">小計</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {order.items.length === 0 ? (
              <TableRow>
                <TableCell colSpan={4} className="text-center">
                  商品が見つかりませんでした
                </TableCell>
              </TableRow>
            ) : (
              order.items.map((item) => {
                // APIが返したアイテムオブジェクトを使用します
                // 注文時点の価格と数量がないため、現在の価格を使用
                const price = item.price;
                const quantity = 1; // APIからquantityが取得できないため固定値
                const subtotal = price * quantity;

                return (
                  <TableRow key={item.id}>
                    <TableCell className="font-medium">{item.name}</TableCell>
                    <TableCell className="text-right">
                      ¥{price.toLocaleString()}
                    </TableCell>
                    <TableCell className="text-right">{quantity}</TableCell>
                    <TableCell className="text-right font-semibold">
                      ¥{subtotal.toLocaleString()}
                    </TableCell>
                  </TableRow>
                );
              })
            )}
            <TableRow>
              <TableCell colSpan={3} className="text-right font-bold">
                合計
              </TableCell>
              <TableCell className="text-right font-bold">
                ¥{order.total_amount.toLocaleString()}
              </TableCell>
            </TableRow>
          </TableBody>
        </Table>
      </div>
    </div>
  );
}
