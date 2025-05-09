'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { orderApi } from '@/services/api'
import { Order, OrderStatus, OrderUpdate } from '@/types/order'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'

interface EditOrderPageProps {
  params: {
    id: string
  }
}

export default function EditOrderPage({ params }: EditOrderPageProps) {
  const router = useRouter()
  const orderId = params.id
  const [order, setOrder] = useState<Order | null>(null)
  const [formData, setFormData] = useState<OrderUpdate>({})
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState<string | null>(null)

  // 注文ステータスのオプション
  const statusOptions = [
    { value: OrderStatus.PENDING, label: '処理待ち' },
    { value: OrderStatus.PROCESSING, label: '処理中' },
    { value: OrderStatus.SHIPPED, label: '発送済み' },
    { value: OrderStatus.DELIVERED, label: '配達完了' },
    { value: OrderStatus.CANCELLED, label: 'キャンセル' },
  ]

  useEffect(() => {
    const fetchOrder = async () => {
      try {
        setLoading(true)
        const data = await orderApi.getOrder(orderId)
        setOrder(data)
        setFormData({
          status: data.status,
          shipping_address: data.shipping_address,
          notes: data.notes,
        })
        setError(null)
      } catch (err) {
        console.error('Error fetching order:', err)
        setError('Failed to load order. Please try again later.')
      } finally {
        setLoading(false)
      }
    }

    fetchOrder()
  }, [orderId])

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value } = e.target
    setFormData({ ...formData, [name]: value })
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setSaving(true)
    setError(null)

    try {
      await orderApi.updateOrder(orderId, formData)
      router.push(`/orders/${orderId}`)
    } catch (err: any) {
      console.error('Error updating order:', err)
      setError(err.response?.data?.detail || 'Failed to update order. Please try again.')
    } finally {
      setSaving(false)
    }
  }

  if (loading) return <div className="container mx-auto p-6">Loading order...</div>
  if (error && !order) return <div className="container mx-auto p-6 text-red-500">{error}</div>
  if (!order) return <div className="container mx-auto p-6">Order not found</div>

  return (
    <div className="container mx-auto p-6 max-w-2xl">
      <h1 className="text-3xl font-bold mb-6">注文編集</h1>

      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="space-y-2">
          <Label htmlFor="status">ステータス</Label>
          <select
            id="status"
            name="status"
            value={formData.status}
            onChange={handleChange}
            className="w-full p-2 border rounded-md"
          >
            {statusOptions.map(option => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
        </div>

        <div className="space-y-2">
          <Label htmlFor="shipping_address">配送先住所</Label>
          <textarea
            id="shipping_address"
            name="shipping_address"
            value={formData.shipping_address || ''}
            onChange={handleChange}
            className="w-full min-h-[100px] p-2 border rounded-md"
          />
        </div>

        <div className="space-y-2">
          <Label htmlFor="notes">備考</Label>
          <textarea
            id="notes"
            name="notes"
            value={formData.notes || ''}
            onChange={handleChange}
            className="w-full min-h-[100px] p-2 border rounded-md"
          />
        </div>

        <div className="flex justify-between pt-4">
          <Link href={`/orders/${orderId}`}>
            <Button type="button" variant="outline">キャンセル</Button>
          </Link>
          <Button type="submit" disabled={saving}>
            {saving ? '保存中...' : '保存する'}
          </Button>
        </div>
      </form>
    </div>
  )
}