"use client";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { itemApi } from "@/services/api";
import { Item, ItemUpdate } from "@/types/item";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";

interface EditItemPageProps {
  params: {
    id: string;
  };
}

export default function EditItemPage({ params }: EditItemPageProps) {
  const router = useRouter();
  const itemId = params.id;
  const [item, setItem] = useState<Item | null>(null);
  const [formData, setFormData] = useState<ItemUpdate>({});
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchItem = async () => {
      try {
        setLoading(true);
        const data = await itemApi.getItem(itemId);
        setItem(data);
        setFormData({
          name: data.name,
          description: data.description,
          price: data.price,
          stock: data.stock,
          image_url: data.image_url,
        });
        setError(null);
      } catch (err) {
        console.error("Error fetching item:", err);
        setError("Failed to load item. Please try again later.");
      } finally {
        setLoading(false);
      }
    };

    fetchItem();
  }, [itemId]);

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
    setSaving(true);
    setError(null);

    try {
      await itemApi.updateItem(itemId, formData);
      router.push("/items");
    } catch (err: any) {
      console.error("Error updating item:", err);
      setError(
        err.response?.data?.detail || "Failed to update item. Please try again."
      );
    } finally {
      setSaving(false);
    }
  };

  if (loading)
    return <div className="container mx-auto p-6">Loading item...</div>;
  if (error && !item)
    return <div className="container mx-auto p-6 text-red-500">{error}</div>;
  if (!item) return <div className="container mx-auto p-6">Item not found</div>;

  return (
    <div className="container mx-auto p-6 max-w-2xl">
      <h1 className="text-3xl font-bold mb-6">商品編集</h1>

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
            value={formData.name || ""}
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
            value={formData.price || 0}
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
            value={formData.stock || 0}
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
          <Button type="submit" disabled={saving}>
            {saving ? "保存中..." : "保存する"}
          </Button>
        </div>
      </form>
    </div>
  );
}
