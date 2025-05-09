"use client";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { itemApi } from "@/services/api";
import { ItemCreate } from "@/types/item";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState } from "react";

export default function CreateItemPage() {
  const router = useRouter();
  const [formData, setFormData] = useState<ItemCreate>({
    name: "",
    description: "",
    price: 0,
    stock: 0,
    image_url: "",
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    const { name, value } = e.target;

    // 数値型のフィールドを適切に変換
    if (name === "price" || name === "stock") {
      setFormData({ ...formData, [name]: Number(value) });
    } else {
      setFormData({ ...formData, [name]: value });
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      await itemApi.createItem(formData);
      router.push("/items");
    } catch (err: any) {
      console.error("Error creating item:", err);
      setError(
        err.response?.data?.detail || "Failed to create item. Please try again."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mx-auto p-6 max-w-2xl">
      <h1 className="text-3xl font-bold mb-6">新規商品登録</h1>

      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="space-y-2">
          <Label htmlFor="name">商品名</Label>
          <Input
            id="name"
            name="name"
            value={formData.name}
            onChange={handleChange}
            required
          />
        </div>

        <div className="space-y-2">
          <Label htmlFor="description">商品説明</Label>
          <textarea
            id="description"
            name="description"
            value={formData.description || ""}
            onChange={handleChange}
            className="w-full min-h-[100px] p-2 border rounded-md"
          />
        </div>

        <div className="space-y-2">
          <Label htmlFor="price">価格</Label>
          <Input
            id="price"
            name="price"
            type="number"
            min="0"
            step="0.01"
            value={formData.price}
            onChange={handleChange}
            required
          />
        </div>

        <div className="space-y-2">
          <Label htmlFor="stock">在庫数</Label>
          <Input
            id="stock"
            name="stock"
            type="number"
            min="0"
            value={formData.stock}
            onChange={handleChange}
            required
          />
        </div>

        <div className="space-y-2">
          <Label htmlFor="image_url">画像URL</Label>
          <Input
            id="image_url"
            name="image_url"
            value={formData.image_url || ""}
            onChange={handleChange}
          />
        </div>

        <div className="flex justify-between pt-4">
          <Link href="/items">
            <Button type="button" variant="outline">
              キャンセル
            </Button>
          </Link>
          <Button type="submit" disabled={loading}>
            {loading ? "登録中..." : "登録する"}
          </Button>
        </div>
      </form>
    </div>
  );
}
