'use client'

import { useEffect, useState } from 'react'
import Link from 'next/link'
import { itemApi } from '@/services/api'
import { Item } from '@/types/item'
import { Button } from '@/components/ui/button'
import { 
  Table, 
  TableBody, 
  TableCaption, 
  TableCell, 
  TableHead, 
  TableHeader, 
  TableRow 
} from '@/components/ui/table'
import { formatToJST } from '@/utils/date'

export default function ItemsPage() {
  const [items, setItems] = useState<Item[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchItems = async () => {
      try {
        setLoading(true)
        const data = await itemApi.getItems()
        setItems(data)
        setError(null)
      } catch (err) {
        console.error('Error fetching items:', err)
        setError('Failed to load items. Please try again later.')
      } finally {
        setLoading(false)
      }
    }

    fetchItems()
  }, [])

  const handleDelete = async (id: string) => {
    if (window.confirm('Are you sure you want to delete this item?')) {
      try {
        await itemApi.deleteItem(id)
        setItems(items.filter(item => item.id !== id))
      } catch (err) {
        console.error('Error deleting item:', err)
        alert('Failed to delete item. Please try again.')
      }
    }
  }

  if (loading) return <div className="container mx-auto p-6">Loading items...</div>
  if (error) return <div className="container mx-auto p-6 text-red-500">{error}</div>

  return (
    <div className="container mx-auto p-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">商品リスト</h1>
        <Link href="/items/create">
          <Button>新規商品登録</Button>
        </Link>
      </div>

      <Table>
        <TableCaption>システム内の全商品リスト</TableCaption>
        <TableHeader>
          <TableRow>
            <TableHead>商品名</TableHead>
            <TableHead>価格</TableHead>
            <TableHead>在庫数</TableHead>
            <TableHead>作成日</TableHead>
            <TableHead>操作</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {items.length === 0 ? (
            <TableRow>
              <TableCell colSpan={5} className="text-center">商品が見つかりませんでした</TableCell>
            </TableRow>
          ) : (
            items.map((item) => (
              <TableRow key={item.id}>
                <TableCell className="font-medium">{item.name}</TableCell>
                <TableCell>¥{item.price.toLocaleString()}</TableCell>
                <TableCell>
                  <span className={`px-2 py-1 rounded-full text-xs ${
                    item.stock > 10 
                      ? 'bg-green-100 text-green-800' 
                      : item.stock > 0 
                        ? 'bg-yellow-100 text-yellow-800' 
                        : 'bg-red-100 text-red-800'
                  }`}>
                    {item.stock > 0 ? `${item.stock}点` : '在庫切れ'}
                  </span>
                </TableCell>
                <TableCell>{formatToJST(item.created_at)}</TableCell>
                <TableCell>
                  <div className="flex space-x-2">
                    <Link href={`/items/edit/${item.id}`}>
                      <Button variant="outline" size="sm">編集</Button>
                    </Link>
                    <Button 
                      variant="destructive" 
                      size="sm" 
                      onClick={() => handleDelete(item.id)}
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
  )
}