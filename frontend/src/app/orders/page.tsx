"use client";

import { Button } from "@/components/ui/button";
import {
  Table,
  TableBody,
  TableCaption,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { orderApi, userApi } from "@/services/api";
import { Order, OrderStatus } from "@/types/order";
import { User } from "@/types/user";
import { formatToJST } from "@/utils/date";
import Link from "next/link";
import { useEffect, useState } from "react";

export default function OrdersPage() {
  const [orders, setOrders] = useState<Order[]>([]);
  const [users, setUsers] = useState<{ [key: string]: User }>({});
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
        const ordersData = await orderApi.getOrders();
        setOrders(ordersData);

        // ユーザーデータを取得
        const usersData = await userApi.getUsers();

        // ユーザーデータをIDをキーとしたオブジェクトに変換
        const usersMap = usersData.reduce((acc, user) => {
          acc[user.id] = user;
          return acc;
        }, {} as { [key: string]: User });

        setUsers(usersMap);
        setError(null);
      } catch (err) {
        console.error("Error fetching data:", err);
        setError("Failed to load orders. Please try again later.");
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const handleDelete = async (id: string) => {
    if (window.confirm("Are you sure you want to delete this order?")) {
      try {
        await orderApi.deleteOrder(id);
        setOrders(orders.filter((order) => order.id !== id));
      } catch (err) {
        console.error("Error deleting order:", err);
        alert("Failed to delete order. Please try again.");
      }
    }
  };

  if (loading)
    return <div className="container mx-auto p-6">Loading orders...</div>;
  if (error)
    return <div className="container mx-auto p-6 text-red-500">{error}</div>;

  return (
    <div className="container mx-auto p-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">注文リスト</h1>
        <Link href="/orders/create">
          <Button>新規注文作成</Button>
        </Link>
      </div>

      <Table>
        <TableCaption>システム内の全注文リスト</TableCaption>
        <TableHeader>
          <TableRow>
            <TableHead>注文者</TableHead>
            <TableHead>金額</TableHead>
            <TableHead>ステータス</TableHead>
            <TableHead>商品数</TableHead>
            <TableHead>注文日</TableHead>
            <TableHead>操作</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {orders.length === 0 ? (
            <TableRow>
              <TableCell colSpan={6} className="text-center">
                注文が見つかりませんでした
              </TableCell>
            </TableRow>
          ) : (
            orders.map((order) => (
              <TableRow key={order.id}>
                <TableCell className="font-medium">
                  {users[order.user_id]?.full_name || "不明なユーザー"}
                </TableCell>
                <TableCell>¥{order.total_amount.toLocaleString()}</TableCell>
                <TableCell>
                  <span
                    className={`px-2 py-1 rounded-full text-xs ${
                      statusColors[order.status]
                    }`}
                  >
                    {statusLabels[order.status]}
                  </span>
                </TableCell>
                <TableCell>{order.items.length}点</TableCell>
                <TableCell>{formatToJST(order.created_at)}</TableCell>
                <TableCell>
                  <div className="flex space-x-2">
                    <Link href={`/orders/${order.id}`}>
                      <Button variant="outline" size="sm">
                        詳細
                      </Button>
                    </Link>
                    <Link href={`/orders/edit/${order.id}`}>
                      <Button variant="outline" size="sm">
                        編集
                      </Button>
                    </Link>
                    <Button
                      variant="destructive"
                      size="sm"
                      onClick={() => handleDelete(order.id)}
                    >
                      削除
                    </Button>
                  </div>
                </TableCell>
              </TableRow>
            ))
          )}
        </TableBody>
      </Table>
    </div>
  );
}
