"use client";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
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
import { OrderCreate, OrderStatus } from "@/types/order";
import { User } from "@/types/user";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";

export default function CreateOrderPage() {
  const router = useRouter();
  const [users, setUsers] = useState<User[]>([]);
  const [items, setItems] = useState<Item[]>([]);
  const [selectedItems, setSelectedItems] = useState<
    {
      itemId: string;
      quantity: number;
      price: number;
    }[]
  >([]);
  const [formData, setFormData] = useState<{
    userId: string;
    status: OrderStatus;
    shippingAddress: string;
    notes: string;
  }>({
    userId: "",
    status: OrderStatus.PENDING,
    shippingAddress: "",
    notes: "",
  });
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // 注文ステータスのオプション
  const statusOptions = [
    { value: OrderStatus.PENDING, label: "処理待ち" },
    { value: OrderStatus.PROCESSING, label: "処理中" },
    { value: OrderStatus.SHIPPED, label: "発送済み" },
    { value: OrderStatus.DELIVERED, label: "配達完了" },
    { value: OrderStatus.CANCELLED, label: "キャンセル" },
  ];

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);

        // ユーザーとアイテムデータを取得
        const [usersData, itemsData] = await Promise.all([
          userApi.getUsers(),
          itemApi.getItems(),
        ]);

        setUsers(usersData);
        setItems(itemsData);

        // 最初のユーザーを選択状態にする（存在する場合）
        if (usersData.length > 0) {
          setFormData((prev) => ({ ...prev, userId: usersData[0].id }));
        }

        setError(null);
      } catch (err) {
        console.error("Error fetching data:", err);
        setError("Failed to load data. Please try again later.");
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const handleChange = (
    e: React.ChangeEvent<
      HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement
    >
  ) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleItemSelect = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const itemId = e.target.value;
    if (!itemId) return;

    const item = items.find((i) => i.id === itemId);
    if (!item) return;

    // アイテムが既に選択されていないか確認
    if (selectedItems.some((si) => si.itemId === itemId)) {
      alert("この商品は既に追加されています");
      return;
    }

    setSelectedItems([
      ...selectedItems,
      { itemId, quantity: 1, price: item.price },
    ]);
  };

  const updateItemQuantity = (index: number, quantity: number) => {
    const newSelectedItems = [...selectedItems];
    newSelectedItems[index].quantity = Math.max(1, quantity);
    setSelectedItems(newSelectedItems);
  };

  const removeItem = (index: number) => {
    setSelectedItems(selectedItems.filter((_, i) => i !== index));
  };

  const calculateTotal = () => {
    return selectedItems.reduce((total, item) => {
      return total + item.price * item.quantity;
    }, 0);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (selectedItems.length === 0) {
      alert("少なくとも1つの商品を追加してください");
      return;
    }

    if (!formData.userId) {
      alert("ユーザーを選択してください");
      return;
    }

    setSaving(true);
    setError(null);

    const orderData: OrderCreate = {
      user_id: formData.userId,
      status: formData.status,
      shipping_address: formData.shippingAddress || null,
      total_amount: calculateTotal(),
      notes: formData.notes || null,
      items: selectedItems.map((item) => ({
        item_id: item.itemId,
        quantity: item.quantity,
        price_at_time: item.price,
      })),
    };

    try {
      const createdOrder = await orderApi.createOrder(orderData);
      router.push(`/orders/${createdOrder.id}`);
    } catch (err: any) {
      console.error("Error creating order:", err);
      setError(
        err.response?.data?.detail ||
          "Failed to create order. Please try again."
      );
    } finally {
      setSaving(false);
    }
  };

  if (loading)
    return <div className="container mx-auto p-6">Loading data...</div>;

  return (
    <div className="container mx-auto p-6 max-w-4xl">
      <h1 className="text-3xl font-bold mb-6">新規注文作成</h1>

      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-6">
        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-xl font-semibold mb-4">注文情報</h2>

          <div className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="userId">顧客</Label>
              <select
                id="userId"
                name="userId"
                value={formData.userId}
                onChange={handleChange}
                className="w-full p-2 border rounded-md"
              >
                {users.length === 0 ? (
                  <option value="">ユーザーがいません</option>
                ) : (
                  users.map((user) => (
                    <option key={user.id} value={user.id}>
                      {user.full_name} ({user.email})
                    </option>
                  ))
                )}
              </select>
            </div>

            <div className="space-y-2">
              <Label htmlFor="status">ステータス</Label>
              <select
                id="status"
                name="status"
                value={formData.status}
                onChange={handleChange}
                className="w-full p-2 border rounded-md"
              >
                {statusOptions.map((option) => (
                  <option key={option.value} value={option.value}>
                    {option.label}
                  </option>
                ))}
              </select>
            </div>

            <div className="space-y-2">
              <Label htmlFor="shippingAddress">配送先住所</Label>
              <textarea
                id="shippingAddress"
                name="shippingAddress"
                value={formData.shippingAddress}
                onChange={handleChange}
                className="w-full min-h-[100px] p-2 border rounded-md"
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="notes">備考</Label>
              <textarea
                id="notes"
                name="notes"
                value={formData.notes}
                onChange={handleChange}
                className="w-full min-h-[80px] p-2 border rounded-md"
              />
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-xl font-semibold mb-4">商品選択</h2>

          <div className="mb-4">
            <Label htmlFor="itemId">商品を追加</Label>
            <select
              id="itemId"
              onChange={handleItemSelect}
              value=""
              className="w-full p-2 border rounded-md"
            >
              <option value="">-- 商品を選択 --</option>
              {items.map((item) => (
                <option key={item.id} value={item.id}>
                  {item.name} (¥{item.price.toLocaleString()}) - 在庫:{" "}
                  {item.stock}
                </option>
              ))}
            </select>
          </div>

          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>商品名</TableHead>
                <TableHead>単価</TableHead>
                <TableHead>数量</TableHead>
                <TableHead>小計</TableHead>
                <TableHead>操作</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {selectedItems.length === 0 ? (
                <TableRow>
                  <TableCell colSpan={5} className="text-center">
                    商品が選択されていません
                  </TableCell>
                </TableRow>
              ) : (
                selectedItems.map((selectedItem, index) => {
                  const item = items.find((i) => i.id === selectedItem.itemId);
                  const subtotal = selectedItem.price * selectedItem.quantity;

                  return (
                    <TableRow key={index}>
                      <TableCell>{item?.name || "Unknown"}</TableCell>
                      <TableCell>
                        ¥{selectedItem.price.toLocaleString()}
                      </TableCell>
                      <TableCell>
                        <Input
                          type="number"
                          min="1"
                          value={selectedItem.quantity}
                          onChange={(e) =>
                            updateItemQuantity(
                              index,
                              parseInt(e.target.value) || 1
                            )
                          }
                          className="w-20"
                        />
                      </TableCell>
                      <TableCell>¥{subtotal.toLocaleString()}</TableCell>
                      <TableCell>
                        <Button
                          type="button"
                          variant="destructive"
                          size="sm"
                          onClick={() => removeItem(index)}
                        >
                          削除
                        </Button>
                      </TableCell>
                    </TableRow>
                  );
                })
              )}
              <TableRow>
                <TableCell colSpan={3} className="text-right font-bold">
                  合計
                </TableCell>
                <TableCell colSpan={2} className="font-bold">
                  ¥{calculateTotal().toLocaleString()}
                </TableCell>
              </TableRow>
            </TableBody>
          </Table>
        </div>

        <div className="flex justify-between">
          <Link href="/orders">
            <Button type="button" variant="outline">
              キャンセル
            </Button>
          </Link>
          <Button
            type="submit"
            disabled={saving || selectedItems.length === 0 || !formData.userId}
          >
            {saving ? "作成中..." : "注文を作成"}
          </Button>
        </div>
      </form>
    </div>
  );
}
