import { format, parseISO } from 'date-fns'
import { formatInTimeZone } from 'date-fns-tz'

/**
 * UTC日時文字列を日本時間に変換してフォーマットする
 * @param dateString - ISO形式の日時文字列
 * @param formatStr - 出力形式 (デフォルト: 'yyyy/MM/dd HH:mm:ss')
 * @returns 日本時間にフォーマットされた日時文字列
 */
export const formatToJST = (
  dateString: string,
  formatStr: string = 'yyyy/MM/dd HH:mm:ss'
): string => {
  try {
    const date = parseISO(dateString)
    return formatInTimeZone(date, 'Asia/Tokyo', formatStr)
  } catch (error) {
    console.error('Error formatting date to JST:', error)
    return dateString
  }
}