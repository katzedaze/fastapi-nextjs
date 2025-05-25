import factory
from factory import Faker

from app.factories.base import BaseSQLAlchemyModelFactory
from app.models.item import Item


class ItemFactory(BaseSQLAlchemyModelFactory):
    """Factory for Item model."""

    class Meta:
        model = Item

    name = Faker("word")
    description = Faker("text", max_nb_chars=200)
    price = Faker("pyfloat", positive=True, max_value=1000000, right_digits=2)
    stock = Faker("pyint", min_value=0, max_value=100)
    image_url = Faker("image_url")


class LaptopFactory(ItemFactory):
    """Factory for laptop items."""
    
    name = "ノートパソコン"
    description = "高性能なビジネス向けノートパソコン。16GBメモリ、512GB SSD搭載。"
    price = 125000.0
    stock = 10
    image_url = "https://example.com/images/laptop.jpg"


class EarphonesFactory(ItemFactory):
    """Factory for earphones items."""
    
    name = "ワイヤレスイヤホン"
    description = "ノイズキャンセリング機能付きの高音質ワイヤレスイヤホン。バッテリー持続時間8時間。"
    price = 15000.0
    stock = 25
    image_url = "https://example.com/images/earphones.jpg"


class SmartwatchFactory(ItemFactory):
    """Factory for smartwatch items."""
    
    name = "スマートウォッチ"
    description = "健康管理機能付きのスマートウォッチ。心拍数、睡眠管理、歩数計測が可能。"
    price = 22000.0
    stock = 15
    image_url = "https://example.com/images/smartwatch.jpg"


class DesktopFactory(ItemFactory):
    """Factory for desktop PC items."""
    
    name = "デスクトップPC"
    description = "ゲーミング用高性能デスクトップPC。RTX 3080搭載、水冷システム。"
    price = 250000.0
    stock = 5
    image_url = "https://example.com/images/desktop.jpg"


class SpeakerFactory(ItemFactory):
    """Factory for Bluetooth speaker items."""
    
    name = "Bluetoothスピーカー"
    description = "コンパクトで持ち運びに便利なBluetoothスピーカー。防水機能付き。"
    price = 8000.0
    stock = 30
    image_url = "https://example.com/images/speaker.jpg"